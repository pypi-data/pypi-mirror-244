from setuptools import setup

setup(
    name='ssapi',
    version='1.1.2',
    author='zedr',
    package_dir={'': 'src'},
    packages=['ssapi'],
    py_modules=['ssapi'],
    scripts=['scripts/ssapi-web'],
    install_requires=[
        'bottle>=0.12.23,<0.13'
    ]
)
