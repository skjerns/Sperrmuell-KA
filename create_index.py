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
    for folder in folders:
        if folder=='.git': continue
        html = index(folder)
        with open(folder + '/index.html', 'w') as f:
            f.write(html)

def index(folder):

    fnames = [fname for fname in sorted(folder)   if fname not in EXCLUDED]
    header = os.path.basename(folder)
    html = Template(INDEX_TEMPLATE).render(names=fnames, header=header)
    return html

if __name__ == '__main__':
    main('.')