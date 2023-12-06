from setuptools import setup, find_packages

setup(
    name='cswizards',
    version='0.1',
    author="CS Wizards",
    author_email="ballisticmoo143@gmail.com",
    description='library for stocks price prediction',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'tensorflow',
        'scikit-learn',
        'matplotlib',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
