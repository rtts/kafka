from .models import Config, Webtext

def get_config(parameter):
    '''Gets or creates the requested parameter.

    '''
    if parameter not in [t[0] for t in Config.TYPES]:
        raise ValueError('Invalid parameter requested')
    (c, created) = Config.objects.get_or_create(parameter=parameter)
    return c.content

def get_webtext(parameter):
    '''Gets or creates the requested parameter.

    '''
    if parameter not in [t[0] for t in Webtext.TYPES]:
        raise ValueError('Invalid parameter requested')
    (c, created) = Webtext.objects.get_or_create(parameter=parameter)
    return c.content
