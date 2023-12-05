
import pathlib
from setuptools import setup
from pyutplugins import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="pyutplugins",
    version=__version__,
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Pyut Plugins',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/pyutplugins",
    package_data={
        'pyutplugins':                       ['py.typed'],
        'pyutplugins.common':                ['py.typed'],
        'pyutplugins.common.ui':             ['py.typed'],
        'pyutplugins.common.ui,preferences': ['py.typed'],
        'pyutplugins.exceptions':                    ['py.typed'],
        'pyutplugins.ioplugins':                      ['py.typed'],
        'pyutplugins.ioplugins.dtd':                  ['py.typed'],
        'pyutplugins.ioplugins.gml':                  ['py.typed'],
        'pyutplugins.ioplugins.java':                 ['py.typed'],
        'pyutplugins.ioplugins.mermaid':              ['py.typed'],
        'pyutplugins.ioplugins.pdf':                  ['py.typed'],
        'pyutplugins.ioplugins.python':               ['py.typed'],
        'pyutplugins.ioplugins.python.pyantlrparser': ['py.typed'],
        'pyutplugins.ioplugins.wximage':              ['py.typed'],
        'pyutplugins.plugininterfaces':               ['py.typed'],
        'pyutplugins.plugintypes':                    ['py.typed'],
        'pyutplugins.preferences':                    ['py.typed'],
        'pyutplugins.toolplugins':                    ['py.typed'],
        'pyutplugins.toolplugins.orthogonal':         ['py.typed'],
        'pyutplugins.toolplugins.sugiyama':           ['py.typed'],
    },
    packages=[
        'pyutplugins', 'pyutplugins.common', 'pyutplugins.common.ui', 'pyutplugins.common.ui.preferences',
        'pyutplugins.exceptions',
        'pyutplugins.ioplugins', 'pyutplugins.ioplugins.dtd', 'pyutplugins.ioplugins.gml',  'pyutplugins.ioplugins.java',
        'pyutplugins.ioplugins.mermaid', 'pyutplugins.ioplugins.pdf', 'pyutplugins.ioplugins.python', 'pyutplugins.ioplugins.python.pyantlrparser',
        'pyutplugins.ioplugins.wximage',
        'pyutplugins.plugininterfaces',
        'pyutplugins.plugintypes',
        'pyutplugins.preferences',
        'pyutplugins.toolplugins', 'pyutplugins.toolplugins.orthogonal', 'pyutplugins.toolplugins.sugiyama',
    ],
    install_requires=['pyutmodel==1.5.1', 'ogl==1.0.0', 'untanglepyut==1.3.2', 'oglio==1.2.2', 'codeallybasic~=0.5.2', 'codeallyadvanced~=0.5.2', 'pyumldiagrams==3.1.0',
                      'wxPython~=4.2.1',
                      'antlr4-python3-runtime==4.11.1',
                      'networkx==3.0',
                      'orthogonal==1.2.0',
                      ]
)
