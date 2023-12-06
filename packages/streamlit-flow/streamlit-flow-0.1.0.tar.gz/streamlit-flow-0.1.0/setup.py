from setuptools import setup, find_packages

setup(
    name='streamlit-flow',
    version='0.1.0',
    author='Hans Then',
    author_email='hans.then@gmail.com',
    description='Create multipage streamlit applications',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
