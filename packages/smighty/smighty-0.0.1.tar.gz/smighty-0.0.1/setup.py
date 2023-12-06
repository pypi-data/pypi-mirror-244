# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smighty', 'smighty.app', 'smighty.app.cli', 'smighty.app.ui', 'smighty.tests']

package_data = \
{'': ['*'], 'smighty': ['notebooks/*']}

modules = \
['py']
install_requires = \
['openapi[all]>=1.1.0,<2.0.0']

extras_require = \
{'cli': ['typer[all]>=0.9.0,<0.10.0'], 'ui': ['gradio>=4.7.1,<5.0.0']}

setup_kwargs = {
    'name': 'smighty',
    'version': '0.0.1',
    'description': 'Small, yet powerful conversational agent framework',
    'long_description': ' # Small and Mighty Conversational Agent Framework\n\nThis is an experimental project to develop next generation of conversational\nagents that can connect the world of unconstrained generation of Large Language\nModels (LLM) to the world of structured data sources. Our goal is to build a\nmodular and configurable framework to seamlessly integrate language agents with \ndata sources to build conversational experiences for next generation of digital\nsystems.\n\n> THIS PROJECT IS IN ACTIVE DEVELOPMENT. PROCEED WITH CAUTION!\n\n---\n\n[![Test](https://github.com/alywonder/smighty/actions/workflows/run-tests.yml/badge.svg)](https://github.com/alywonder/smighty/actions/workflows/run-tests.yml)\n[![Python](https://img.shields.io/badge/python-3.10%7C3.11-blue)](https://www.python.org/downloads/release/python-3100/)\n\n\n\n## The Big Idea about Small Things\n\nTo achieve our goals, we are pursuing two fundamental ideas:\n1. _Sequence to structure: Convert sequence to sequence models to sequence to \nstructure extraction ones._\nThis is about extracting the structure of information required to properly\nfulfill a user request from her natural language utterances.\n2. Structure Informed Generation: Generate responses that combine both\nunstructured and structured information.\n\n<span style="font-size:8pt;">Copyright &copy; 2023 Weavers @ Eternal Loom. All rights reserved.</span>\n',
    'author': 'Al Wonder',
    'author_email': 'al@yiwonder.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
