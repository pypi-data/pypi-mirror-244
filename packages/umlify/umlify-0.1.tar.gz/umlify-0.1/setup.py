from setuptools import setup, find_packages

setup(
    name='umlify',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    description='A Python library to generate plantUML diagrams from code.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Adeline Sharla',
    author_email='adelinesharla@duck.com',
    url='https://github.com/adelinesharla/UMLfy',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
