from typing import Set, Callable, Dict

import jinja2
from docxtpl import DocxTemplate


def get_argumnets_from_docx(doc: DocxTemplate) -> Set[str]:
    xml = doc.get_xml()
    xml = doc.patch_xml(xml)
    xml = xml.replace(r'<w:p>', '\n<w:p>')

    env = jinja2.Environment(autoescape=False)
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
    doc.render(context)
    doc.save(path)
