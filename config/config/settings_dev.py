DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neft-system-4',
        'USER': 'postgres',
        'PASSWORD': '20010508',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# SMS_CODE_ACTIVE = False
# ESKIZ_TOKEN = ''
# MAPS_API_KEY = ''

# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = '' 
# SERVER_EMAIL = EMAIL_HOST_USER
# DEFAULT_FROM_EMAIL = ''