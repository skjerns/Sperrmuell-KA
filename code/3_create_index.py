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

EXCLUDED = ['index.html', '.git', 'joblib', '__pycache__']
import ospath
import os

# May need to do "pip install mako"
from mako.template import Template


def main(root):
    folders = ospath.list_folders(root, subfolders=True, add_parent=True)
    folders = [f for f in folders if not any([exc in f for exc in EXCLUDED])]
    for folder in folders:
        print(f'index for {folder}')
        if '.git' in folder: continue
        if 'joblib' in folder: continue
        html = index(folder)
        with open(folder + '/index.html', 'w') as f:
            f.write(html)

def index(folder):
    folders  = ospath.list_folders(folder)
    folders = [f for f in folders if not any([x in f for x in EXCLUDED])]
    files = folders + ospath.list_files(folder, relative=True)
    fnames = [fname for fname in sorted(files) if fname not in EXCLUDED]
    header = os.path.basename(folder)
    html = Template(INDEX_TEMPLATE).render(names=fnames, header=header)
    return html

if __name__ == '__main__':
    main('..')
    
    #manually fix to make interactive map on top
    with open('../index.html', 'r') as f:
        lines = f.readlines()
    lines[3] = '<h2>Sperrmüllkalender Karlsruhe nach Datum</h2>'
    lines.insert(4, '<li><a href="./interactive_map.html"><b>-->> Interaktive Karte</b></a></li>')
    
    html = '\n'.join(lines)
    html = html.replace('..', '.')
    
    with open('../index.html', 'w') as f:
        f.writelines(html)
        