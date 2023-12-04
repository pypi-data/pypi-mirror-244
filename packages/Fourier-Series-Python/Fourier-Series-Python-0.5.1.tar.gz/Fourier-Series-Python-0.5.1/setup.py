from setuptools import setup, find_packages
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='Fourier-Series-Python',
    version='0.5.1',
    author='Abbass Srour',
    author_email='abbasss@umich.edu',
    include_package_data=True,
    packages=find_packages(include=['Fourier.py','FunctionDefinitions.py','FunctionOperations.py','Generate.py','modules.py','Plot.py']),
    install_requires=[
        'plotly','numpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    description='A Fourier Series and Signal Generation Libary to generate coefficients to function',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
