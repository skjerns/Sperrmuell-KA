""" Build index from directory listing

make_index.py </path/to/directory> [--header <header text>]
"""

INDEX_TEMPLATE = r"""
<html>
<body>
<h2>${header}</h2>
<p>
% for name in names:
    <li><a href="${name}">${name}</a></li>
% endfor
</p>
</body>
</html>
"""

EXCLUDED = ['index.html', '.git']
import ospath
import os

# May need to do "pip install mako"
from mako.template import Template


def main(root):
    folders = ospath.list_folders(root, subfolders=True, add_parent=True)
    folders = [f for f in folders if not '.git' in f]
    for folder in folders:
        if '.git' in folder: continue
        html = index(folder)
        with open(folder + '/index.html', 'w') as f:
            f.write(html)

def index(folder):
    files = ospath.list_files(folder, relative=True)
    fnames = [fname for fname in sorted(files) if fname not in EXCLUDED]
    header = os.path.basename(folder)
    html = Template(INDEX_TEMPLATE).render(names=fnames, header=header)
    return html

if __name__ == '__main__':
    main('.')