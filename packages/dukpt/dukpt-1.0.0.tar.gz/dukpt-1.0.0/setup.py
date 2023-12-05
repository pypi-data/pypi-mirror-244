from distutils.core import setup

setup(
    name = 'dukpt',
    version = '1.0.0',
    py_modules = ['dukpt'],
    long_description = open('README.md').read(),
    install_requires=["bitstring==3.1.5", "pycryptodome==3.14.1"],
    python_requires=">=3.2",
)