from setuptools import setup, find_packages

setup(
    name='monkey',
    version='25.02.2',
    packages=find_packages(),
    author="Kristopher Gindlesperger",
    author_email="kristopher.gindlesperger@gmail.com",
    entry_points={
        'console_scripts': [
            'monkey = monkey.main:main'
        ]
    },
    install_requires=[
        'click',
        'chroma',
        'langchain',
        'langchain-chroma',
        'langchain-ollama',
        'langchain-text-splitters',
        'langchain-community',
        'esprima',
        'tree_sitter_languages',
        'tree_sitter',
        'joblib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Linux',
        'License :: OSI :: MIT License'
    ]
)