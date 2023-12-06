from setuptools import setup, find_packages

setup(
    name='LLM_keyword_extractor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'transformers',
        'langchain',
        'torch',
        'einops',
        'accelerate',
        'bitsandbytes',
        # Add any other dependencies your package needs
    ],
    description='This is a python package to extract keywords from a given text using LLMs',
    author='Sandeep Chataut',
    author_email='sandeepkesh52@gmail.com',
)
