from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    author='Group 5',
    packages=find_packages(include=['clv', 'clv.*']),
    url='https://github.com/yeranosyanvahan/ma_group_project',
    description='CLV prediction',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specify the format
    name='SocraCLV',
    version='0.9.9',
)
