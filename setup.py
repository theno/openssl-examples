"""pyopenssl-exmaples (Python part of https://github.com/theno/openssl-examples)
"""

import os
import shutil
from setuptools import setup, find_packages
from codecs import open


def create_readme_with_long_description():
    this_dir = os.path.abspath(os.path.dirname(__file__))
    readme_md = os.path.join(this_dir, 'README.md')
    readme = os.path.join(this_dir, 'README')
    if os.path.isfile(readme_md):
        if os.path.islink(readme):
            os.remove(readme)
        shutil.copy(readme_md, readme)
    try:
        import pypandoc
        long_description = pypandoc.convert(readme_md, 'rst')
        if os.path.islink(readme):
            os.remove(readme)
        with open(readme, 'w') as out:
            out.write(long_description)
    except(IOError, ImportError, RuntimeError):
        if os.path.isfile(readme_md):
            os.remove(readme)
            os.symlink(readme_md, readme)
        with open(readme, encoding='utf-8') as in_:
            long_description = in_.read()
    return long_description


description = __doc__.split('\n')[0]
long_description = create_readme_with_long_description()

setup(
    name='pyopenssl-examples',
    version='0.1.0',
    description=description,
    long_description=long_description,
    url='https://github.com/theno/openssl-examples',
    author='Theodor Nolte',
    author_email='openssl-examples@theno.eu',
    license='OpenSSL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='python development utilities library',
    packages=find_packages(exclude=[
        'contrib',
        'docs',
        'tests',
    ]),
    extras_require={
        'dev': ['pypandoc'],
    },
)
