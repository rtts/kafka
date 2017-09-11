try:
    import uwsgi
    DEBUG = False
except ImportError:
    DEBUG = True

import kafka, os
SASS_PROCESSOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(kafka.__file__)), 'static')

SECRET_KEY = 'u+b$tbcq@)8242b*++rt$cetp3b301pqqc7mrh@8!ib(4-59)c'
ALLOWED_HOSTS = ['localhost', 'kafka.created.today']
ROOT_URLCONF = 'kafka.urls'
WSGI_APPLICATION = 'project.wsgi.application'

LANGUAGE_CODE = 'nl'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = '/srv/kafka/static'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/srv/kafka/media'

INSTALLED_APPS = [
    'kafka',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sass_processor',
    'jquery',
    'ckeditor',
]

CKEDITOR_CONFIGS = {
    'default': {
        'removePlugins': 'elementspath',
        # 'contentsCss': STATIC_URL + 'ckeditor.css',
        'width': '100%',
        'toolbar': 'Custom',
        'allowedContent': True, # this allows iframes, embeds, scripts, etc...
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ['Link', 'Unlink'],
            ['Source'],
        ]
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE += ['tidy.middleware.TidyMiddleware']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'kafka',
        'NAME': 'kafka',
    }
}
