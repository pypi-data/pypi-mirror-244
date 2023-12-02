# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['majormode']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.6,<2.0.0', 'perseus-core-library>=1.19,<2.0']

setup_kwargs = {
    'name': 'prosoponym',
    'version': '1.2.2',
    'description': 'Python library to manage personal names (in onomastic terminology also known as prosoponyms)',
    'long_description': '# Prosoponym Python Library\n\nPython library to format personal names (in onomastic terminology also known as prosoponyms).\n\nA personal name is the set of names by which an individual person is known, with the understanding that, taken together, they all relate to that one individual.  A personal name is generally composed of first names, middle names and last names, which order varies depending on the culture the personal name is related to (western or eastern lexical name orders).\n\n```python\n>>> from majormode.perseus.model.locale import Locale\n>>> from majormode.prosoponym import LexicalNameOrder\n>>> from majormode.prosoponym import format_first_name\n>>> from majormode.prosoponym import format_full_name\n>>> from majormode.prosoponym import format_last_name\n\n>>> format_first_name("Aline Maria")\n\'Aline Maria\'\n>>> format_last_name("caune ly")\n\'CAUNE LY\'\n\n>>> format_full_name("alfred thanh phuc", "pham", Locale(\'fra\'))\n\'Alfred Thanh Phuc PHAM\'\n>>> format_full_name("alfred thanh phuc", "pham", Locale(\'vie\'))\n\'PHAM Alfred Thanh Phuc\'\n\n>>> format_full_name("alfred", "pham", Locale(\'vie\'), full_name="pham thanh phuc")\nValueError: None of the first name words has been found in the full name\n>>> format_full_name("alfred phuc", "pham", Locale(\'fra\'), full_name="pham thanh phuc")\nValueError: The parts of the full name are not written in the expected order\n>>> format_full_name("alfred phuc", "pham", Locale(\'fra\'), full_name="alfred thanh phuc pham")\n\'Alfred Thanh Phuc PHAM\'\n>>> format_full_name("alfred phuc", "pham", Locale(\'vie\'), full_name="Phạm thanh phúc alfred")\n\'PHẠM Thanh Phúc Alfred\'\n\n>>> # If a last name is composed of two or more words, while the full name\n>>> # follows western lexical order, this two or more words SHOULD be \n>>> # in the full name (otherwise the function won\'t be able to determine\n>>> # included in the full name, but not necessary.\n>>> format_full_name("Aline", "Caune ly", Locale(\'fra\'), full_name="aline minh anh maria caune ly")  # OK\n\'Aline Minh Anh Maria CAUNE LY\'\n>>> format_full_name("Aline", "Caune", Locale(\'fra\'), full_name="aline minh anh maria caune ly")  # Still OK, even if incoherent input\n\'Aline Minh Anh Maria CAUNE LY\'\n\n>>> format_full_name("truc", "nguyen", Locale(\'vie\'), full_name="nguyen thi thanh truc maria")\n\'NGUYEN Thi Thanh Truc Maria\'\n\n>>> # If a last name is composed of two or more words, while the full name\n>>> # follows eastern lexical order, this two or more words MUST be included\n>>> # in the full name (otherwise the function won\'t be able to determine\n>>> # which parts of the name correspond to the last name or to the \n>>> # possible middle name).\n>>> format_full_name("Thao nguyen", "nguyen le", Locale(\'vie\'), "Nguyễn Lê thị Thảo Nguyên")\n\'NGUYỄN LÊ Thị Thảo Nguyên\'  # OK\n>>> format_full_name("Thao nguyen", "nguyen le", Locale(\'vie\'), "Nguyễn thị Thảo Nguyên")  # Still OK, even if incoherent input\n\'NGUYỄN Thị Thảo Nguyên\'\n>>> format_full_name("Thao nguyen", "nguyen", Locale(\'vie\'), "Nguyễn Lê thị Thảo Nguyên")  # Not OK! Part of the last name is missing.\n\'NGUYỄN Lê Thị Thảo Nguyên\'\n```',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel.caune@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/majormode/prosoponym-python-library',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
