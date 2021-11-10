from typing import Set, Callable, Dict

import jinja2
from docxtpl import DocxTemplate

from . import filters


__jinja_env = None  # noqa
def get_jinja_env():  # noqa
    global __jinja_env

    if __jinja_env is None:
        __jinja_env = jinja2.Environment(autoescape=False)
        for name in dir(filters):
            attr = getattr(filters, name)
            if callable(attr) and getattr(attr, '_is_filter', None):
                __jinja_env.filters[name] = attr

    return __jinja_env


def register_filter(name: str, func):
    env = get_jinja_env()
    env.filters[name] = func


def get_argumnets_from_docx(doc: DocxTemplate) -> Set[str]:
    xml = doc.get_xml()
    xml = doc.patch_xml(xml)
    xml = xml.replace(r'<w:p>', '\n<w:p>')

    env = get_jinja_env()
    ast = env.parse(xml)

    return jinja2.meta.find_undeclared_variables(ast)


def load_docxtpl_file(path: str) -> DocxTemplate:
    doc = DocxTemplate(path)

    return doc


def build_docx_context_from_cli(
        doc: DocxTemplate,
        prompt_func: Callable[[str], str] = input) -> Dict[str, str]:
    arguments = get_argumnets_from_docx(doc)

    context = {}
    for arg in arguments:
        arg_human_name = ' '.join(arg.split('_')).capitalize()
        value = prompt_func(f'Enter value for "{arg_human_name}": ')

        context[arg] = value

    return context


def save_rendered(doc: DocxTemplate, context: dict, path: str):
    doc.render(context, jinja_env=get_jinja_env())
    doc.save(path)
