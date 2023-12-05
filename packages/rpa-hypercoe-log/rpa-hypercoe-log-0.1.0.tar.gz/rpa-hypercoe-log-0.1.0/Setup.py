from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='rpa-hypercoe-log',
    version='0.1.0',
    license='MIT License',
    author='Joao Buso',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author_email='developer@hypercoe.com',
    keywords='rpa hypercoe log tria software',
    description=u'Repositorio para a utilização da API de Log do HyperCoe',
    packages=['rpa_hypercoe_log'],
    install_requires=['requests'],)