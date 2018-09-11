from setuptools import setup
from Theseus.version import __version__, __build__

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs

try:
    codecs.lookup('mbcs')
except LookupError:
    ascii_codec = codecs.lookup('ascii')
    func = lambda name, enc=ascii_codec: {True: enc}.get(name == 'mbcs')
    codecs.register(func)

setup(
    name='theseus',
    version=__version__,
    build=__build__,
    packages=['Theseus', 'Theseus.Daedalus', 'Theseus.Protocols'],
    url='',
    license='',
    author='amias.channer@iohk.io',
    author_email='amias.channer@iohk.io',
    description='a system for orchestrating test scenarios with Daedalus and other IOHK projects',
    install_requires=['mnemonic', 'requests', 'urllib3', 'paramiko', 'unittest2','sphinx_autodoc-typehints','sphinx-autodoc-napoleon-typehints','sphinx-autodoc-annotation'],
    zip_safe=True
)

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
