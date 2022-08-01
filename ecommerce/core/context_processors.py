from ecommerce.core.readers import YAMLReader


def contact_info_processor(request):
    return {'contact_info': YAMLReader.get_contact_info()['contact-info']}
