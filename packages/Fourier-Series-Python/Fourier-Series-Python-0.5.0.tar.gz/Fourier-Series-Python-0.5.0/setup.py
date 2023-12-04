from setuptools import setup, find_packages

setup(
    name='Fourier-Series-Python',
    version='0.5.0',
    author='Abbass Srour',
    author_email='abbasss@umich.edu',
    packages=find_packages(include=['Fourier.py','FunctionDefinitions.py','FunctionOperations.py','Generate.py','modules.py','Plot.py']),
    install_requires=[
        'plotly','numpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
