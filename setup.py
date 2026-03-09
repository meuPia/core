import os
from setuptools import setup, find_packages

# Lê o conteúdo do README.md para usar como descrição longa na página do PyPI
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="meupia-core",
    version="1.1.9",
    author="Henry Hamon",
    author_email="henryhamon@gmail.com",
    description="Compilador modular de Portugol para Python focado em educação.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meupia/core",
    packages=find_packages(),
    
    # Dependências de execução (vazio, pois o Core é nativo)
    install_requires=[],
    
    # Dependências de desenvolvimento e testes
    extras_require={
        "dev": ["pytest>=7.0.0"],
    },
    
    entry_points={
        'console_scripts': [
            'mpgp=meuPia.tools.mpgp:main',
            'meupia=meuPia.compiler:main',
        ],
    },
    
    # Classificadores ajudam os usuários a filtrarem a busca no PyPI
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License", # Ou GPLv3 se preferir
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    
    # Exige Python 3.8 ou superior (boa prática hoje em dia)
    python_requires='>=3.8',
)