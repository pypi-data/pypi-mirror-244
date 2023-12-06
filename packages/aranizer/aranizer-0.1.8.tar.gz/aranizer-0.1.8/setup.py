from setuptools import setup, find_packages

# read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aranizer',
    version='0.1.8',
    packages=find_packages(),
    url='https://github.com/omarnj-lab/aranizer',
    license='MIT',
    author='omar najar',
    author_email='onajar@psu.edu.sa',
    description='Aranizer: A Custom Tokenizer for Enhanced Arabic Language Processing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'transformers',
        'sentence_transformers'
    ],
    include_package_data=True
)
