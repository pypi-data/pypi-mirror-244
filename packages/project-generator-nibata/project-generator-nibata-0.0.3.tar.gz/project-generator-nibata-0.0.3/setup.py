from setuptools import setup, find_packages

setup(
    name='project-generator-nibata',
    version='v0.0.3',
    packages=find_packages(),
    package_data={'project_generator': ['templates/*.mako']},
    include_package_data=True,
    install_requires=[
        'typer',
        'mako',
    ],
    entry_points={
        'console_scripts': [
            'test-api-gen = project_generator.main:app',
        ],
    },
    author='Nicolás Bacquet',
    author_email='nibata@gmail.com',
    description='A CLI application for generating project scaffolding using Typer and Mako.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nibata/api-projects-cli-tool',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)