import os
from setuptools import setup, find_packages

PREFIX = 'qualimens'


def get_version():
    setup_py_dir = os.path.dirname(__file__)
    version_module_path = os.path.join(setup_py_dir, 'src', 'qualimens', '__version__.py')

    about = {}

    with open(version_module_path) as f:
        exec(f.read(), about)  # noqa

    return about['__version__']


def setup_package():
    setup(
        name='qualimens',
        version=get_version(),
        author='kizill',
        packages=find_packages('src'),
        package_dir={'': 'src'},
        description='Python-package for qualimens mlops service',
        include_package_data=True,
        install_requires=[
        ],
        python_requires='>=3.7.0',
        keywords=['ml', 'mlops'],
    )


if __name__ == '__main__':
    setup_package()
