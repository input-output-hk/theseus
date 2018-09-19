import setuptools
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
    packages=['Theseus','Theseus.Protocols', 'Theseus.Common', 'Theseus.Daedalus', 'Theseus.Cardano', 'Theseus.Tests'],
    url='https://github.com/input-output-hk/theseus',
    license='MIT',
    author='amias.channer@iohk.io',
    author_email='amias.channer@iohk.io',
    description='a system for orchestrating tests for IOHK projects',
    install_requires=['typing', 'mnemonic', 'requests', 'urllib3', 'paramiko', 'unittest2', 'sphinx-autodoc-annotation'],
    zip_safe=True
)

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
