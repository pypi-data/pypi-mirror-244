# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aoa_torch']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aoa-torch',
    'version': '0.0.1',
    'description': 'Attention on Attention - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Attention on Attention Implementation\nThis is a practice implementation after randomly finding it on Lucidrain\'s repo, I\'m implementing the model architecture just for practice!\n\nBasically the architecture is:\nx => q, k, v -> multihead attn with residual q -> concat -> 2 linear projects\n->sigmoid -> mult -> add -> norm -> ffn -> add -> norm with residual of first add and norm\n\n<img src="./saoa.png"></img>\n\n# Install\n`pip3 install `\n\n\n## Usage\n\n### `AoA` Module\n```python\n\nimport torch\n\nfrom aoa.main import AoA\n\nx = torch.randn(1, 10, 512)\nmodel = AoA(512, 8, 64, 0.1)\nout = model(x)\nprint(out.shape)\n\n\n```\n\n### `AoATransformer`\n```python\nimport torch \nfrom aoa.main import AoATransformer\n\n\nx = torch.randint(0, 100, (1, 10))\nmodel = AoATransformer(512, 1, 100)\nout = model(x)\nprint(out.shape)\n\n\n```\n\n\n\n\n\n## Citations\n\n```bibtex\n@misc{rahman2020improved,\n    title   = {An Improved Attention for Visual Question Answering}, \n    author  = {Tanzila Rahman and Shih-Han Chou and Leonid Sigal and Giuseppe Carenini},\n    year    = {2020},\n    eprint  = {2011.02164},\n    archivePrefix = {arXiv},\n    primaryClass = {cs.CV}\n}\n```\n\n```bibtex\n@misc{huang2019attention,\n    title   = {Attention on Attention for Image Captioning}, \n    author  = {Lun Huang and Wenmin Wang and Jie Chen and Xiao-Yong Wei},\n    year    = {2019},\n    eprint  = {1908.06954},\n    archivePrefix = {arXiv},\n    primaryClass = {cs.CV}\n}\n```\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/AoA-torch',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
