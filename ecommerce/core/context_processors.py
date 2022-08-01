from typing import Mapping

from django.core.handlers.wsgi import WSGIRequest

from ecommerce.core.readers import YAMLReader


def contact_info_processor(request: WSGIRequest) -> Mapping:
    return {'contact_info': YAMLReader.get_contact_info()['contact-info']}
