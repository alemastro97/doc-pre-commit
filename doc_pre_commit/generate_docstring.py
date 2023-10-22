from __future__ import annotations
import argparse
import os
from typing import Sequence
import ast
import openai
import re
import astor
prompt = """
{}
Please provide the docstring for the function using Python's best practices without rewriting the code, only the docstring
"""


def getDocFromGPT(f):
    # response = openai.Completion.create(model='gpt-3.5-turbo-instruct',
    #     prompt=prompt.format(f), temperature=0.9, max_tokens=150, top_p=1,
    #     frequency_penalty=0, presence_penalty=0.6, stop=[' Human:', ' AI:'])
    # pattern = '"""(.*?)"""'
    # matches = re.findall(pattern, response.choices[0].text, re.DOTALL)
    # if len(matches) == 0:
    return 'ADD Docstring...'
    # return matches[0].strip()


def add_docstrings(node):
    if isinstance(node, ast.FunctionDef):
        if not node.body:
            node.body = [ast.Expr(value=ast.Str(s=getDocFromGPT(astor.
                to_source(node))))]
        elif not any(isinstance(stmt, ast.Expr) for stmt in node.body):
            node.body.insert(0, ast.Expr(value=ast.Str(s=getDocFromGPT(
                astor.to_source(node)))))


def _generate_doc(filename):
    with open(filename, 'r') as file:
        code = file.read()
    tree = ast.parse(code)
    for node in ast.walk(tree):
        add_docstrings(node)
    modified_code = astor.to_source(tree)
    with open(filename, 'w') as file:
        file.write(modified_code)
    return True


def main(argv: (Sequence[str] | None)=None) ->int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-markdown-linebreak-ext', action='store_true',
        help=argparse.SUPPRESS)
    parser.add_argument('--markdown-linebreak-ext', action='append',
        default=[], metavar='*|EXT[,EXT,...]', help=
        'Markdown extensions (or *) to not strip linebreak spaces.  default: %(default)s'
        )
    parser.add_argument('--chars', help=
        'The set of characters to strip from the end of lines.  Defaults to all whitespace characters.'
        )
    parser.add_argument('--api-key', help='Your OpenAi API key')
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)
    if args.no_markdown_linebreak_ext:
        print('--no-markdown-linebreak-ext now does nothing!')
    md_args = args.markdown_linebreak_ext
    if '' in md_args:
        parser.error('--markdown-linebreak-ext requires a non-empty argument')
    all_markdown = '*' in md_args
    api_key = os.environ.get('OPENAI_API_KEY')
    
    openai.api_key = api_key if args.api_key is None else args.api_key
    print("My api key:",api_key)
    print("My ARGS api key:",args.api_key)
    md_exts = [('.' + x.lower().lstrip('.')) for x in ','.join(md_args).
        split(',')]
    for ext in md_exts:
        if any(c in ext[1:] for c in './\\:'):
            parser.error(
                f"""bad --markdown-linebreak-ext extension {ext!r} (has . / \\ :)
  (probably filename; use '--markdown-linebreak-ext=EXT')"""
                )
    chars = None if args.chars is None else args.chars.encode()
    print(args.filenames)
    return_code = 0
    for filename in args.filenames:
        print('=' * 100, filename)
        _, extension = os.path.splitext(filename.lower())
        md = all_markdown or extension in md_exts
        if extension == '.py' and _generate_doc(filename):
            print(f'Fixing {filename}')
    return return_code


if __name__ == '__main__':
    raise SystemExit(main())
