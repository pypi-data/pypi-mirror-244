from setuptools import setup, find_packages

VERSION = '0.1.3'
DESCRIPTION = "Kaggle dataset connector for Streamlit"

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setup(
    name="st_kaggle_connector",
    version=VERSION,
    author="Oleksandr Arsentiev",
    author_email="<arsentiev9393@gmail.com>",
    description=DESCRIPTION,
    long_description=f"{readme}",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['streamlit', 'pandas', 'kaggle'],
    keywords=['streamlit', 'custom', 'component', 'kaggle', 'dataset', 'connector'],
    license="MIT",
    url="https://github.com/arsentievalex/kaggle-streamlit-data-connector/tree/main",
)