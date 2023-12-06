
from setuptools import setup
import os


# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    name = 'cptec-model',
    version = '0.1.0',
    author = 'Framework CPTEC',
    author_email = 'frameworkcptec@gmail.com',
    packages = ['cptecmodel'],
    install_requires = ['numpy','pandas','matplotlib', 'pycurl==7.45.2', 'cfgrib', 'netCDF4',  'xarray', 'dask', 'scipy', 'xesmf'],
    description = 'Módulo para distribuição de Modelos Numéricos do CPTEC.',
    long_description="""Framework CPTEC

Descrição
É um pacote in Python para a distribuição de dados brutos dos Modelos Numéricos de forma segmentada/particionada. Com esse pacote o usuário não necessita fazer o Download de todo o volume bruto o pacote auxilia a manipular somente a sua necessidade.

support Python >= 3.10.

Documentação 
https://cptec-model.readthedocs.io/en/latest/index.html

    \n""",
    long_description_content_type='text/markdown',
    url = 'https://github.com/felipeodorizi/pclima',
    project_urls = {
        'Código fonte': 'https://github.com/framework-CPTEC/',
        'Download': 'https://github.com/framework-CPTEC/'
    },
    license = 'MIT',
    keywords = 'recuperação de dados climáticos',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    python_requires='>=3.10',
)
