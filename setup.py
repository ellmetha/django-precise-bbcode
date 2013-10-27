from setuptools import setup, find_packages

setup(
    name='django-precise-bbcode',
    version='0.1',
    author='ellmetha',
    author_email='ell@metha.fr',
    package_dir={'': 'src'},
    packages=find_packages("src", exclude="example_project"),
    include_package_data=True,
    license='LICENSE.txt',
    description='A django BBCode integration..',
    long_description=open('README.rst').read(),
    zip_safe=False,
    install_requires=[
        "django>=1.5,<1.6",
        "south",
    ],
)
