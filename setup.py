from setuptools import setup

setup(
    name='theseus',
    version='1',
    packages=['Theseus', 'Theseus.Daedalus'],
    url='',
    license='',
    author='amias channer@iohk.io',
    author_email='amias channer@iohk.io',
    description='a system for orchestrating test scenarios with Daedalus and other IOHK projects',
    install_requires=['mnemonic', 'requests', 'urllib3'],
    zip_safe=True
)
# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs

try:
    codecs.lookup('mbcs')
except LookupError:
    ascii_codec = codecs.lookup('ascii')
    func = lambda name, enc=ascii_codec: {True: enc}.get(name == 'mbcs')
    codecs.register(func)

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'