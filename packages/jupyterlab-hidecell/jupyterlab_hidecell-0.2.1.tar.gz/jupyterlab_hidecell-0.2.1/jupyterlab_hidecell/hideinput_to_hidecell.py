"""
a command line tool for en masse migration of notebooks
from the former classic notebook extension 'hideinput' to
the new JupyterLab extension 'hidecell'

limitations: this assumes jupytext
"""

from argparse import ArgumentParser

import jupytext


def migrate_notebook(notebook):
    print(f'migrating {notebook}')
    with open(notebook, 'r') as f:
        incoming = jupytext.read(f)
    for cell in incoming['cells']:
        for put in ('input', 'output'):
            if cell.get('metadata', {}).get(f'hide_{put}', None) is not None:
                del cell['metadata'][f'hide_{put}']
                if 'tags' not in cell['metadata']:
                    cell['metadata']['tags'] = []
                if f'hide-{put}' not in cell['metadata']['tags']:
                    cell['metadata']['tags'].append(f'hide-{put}')
    # rewrite in same location
    jupytext.write(incoming, notebook)


def main():
    parser = ArgumentParser(
        description='migrate notebooks from (classic)-hide_input to (lab)-hidecell')
    parser.add_argument('notebooks', nargs='+', help='notebooks to migrate')
    args = parser.parse_args()
    for notebook in args.notebooks:
        migrate_notebook(notebook)
    return 0


if __name__ == '__main__':
    exit(main())
