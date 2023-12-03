# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplified_transformers']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'local-attention', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'simplified-transormer-torch',
    'version': '0.0.1',
    'description': 'Paper - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# SimplifiedTransformers\nThe author presents an implementation for Simplifying Transformer Blocks. The standard transformer blocks are complex and can lead to architecture instability. In this work, the author investigates how the standard transformer block can be simplified. Through signal propagation theory and empirical observations, the author proposes modifications that remove several components without sacrificing training speed or performance. The simplified transformers achieve the same training speed and performance as standard transformers, while being 15% faster in training throughput and using 15% fewer parameters.\n\n\n# Install\n```\n\n\n```\n\n--------\n\n## Usage\n```python\n\nimport torch\nfrom simplified_transformers.main import SimplifiedTransformers\n\nmodel = SimplifiedTransformers(\n    dim=4096,\n    depth=6,\n    heads=8,\n    num_tokens=20000,\n)\n\nx = torch.randint(0, 20000, (1, 4096))\n\nout = model(x)\nprint(out.shape)\n\n```\n\n\n\n\n\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/SimplifiedTransformers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
