from typing import Mapping

import yaml

from ecommerce import settings


class YAMLReader:
    @staticmethod
    def _get_config(path: str) -> Mapping:
        with open(path, 'r') as f:
            doc = yaml.load(f, Loader=yaml.FullLoader)
        return doc

    @classmethod
    def get_contact_info(cls) -> Mapping:
        a = cls._get_config(f'{settings.BASE_DIR}/settings/base.yml')
        return a
