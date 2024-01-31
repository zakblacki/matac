import os
from django.utils.translation import gettext_lazy as _

# ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')


# DEBUG = os.getenv('DEBUG','True') == 'True'
DEBUG = True
 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY ='-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
ALLOWED_HOSTS =["matacor.com","www.matacor.com","207.154.249.107"]



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'whitenoise.runserver_nostatic',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',  
    'django_recaptcha',
    
    "social_django",
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',
    'crispy_forms',
    'django_countries',
    'core',
    'mathfilters',
    'rest_framework',
    
   
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.template.context_processors.i18n'
            ],
        },
    },
]

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Africa/Algiers'
USE_I18N = True
USE_L10N = True
# USE_TZ = True

WSGI_APPLICATION = "demo.wsgi.application"
# static files (CSS, JS, Image)

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env'),"/var/www/static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')


# DATABASE_URL = os.getenv("DATABASE_URL",None)

DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "demo1",
            "USER": "dbuser1",
            "PASSWORD": "dbpassword1",
            "HOST": "localhost",
            "PORT": "5432",
            "OPTIONS":{"sslmode":"require"}
            
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR  , 'db.sqlite3'),
#     }
# }

if DEBUG == False:
    DEBUG = False
    # SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



# Auth
AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)
SOCIAL_AUTH_URL_NAMESPACE = 'social'
# SITE_ID = 1
LOGIN_REDIRECT_URL = 'https://matacor.com'

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '573181579663-4uv8b6cmcjotc921km9f7deuv1tinmsl.apps.googleusercontent.com',
            'secret': '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',
            'key': 'AIzaSyABGlrFljxbQ-bGVZPaVCZEmCRXYXpHj2g'
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

 
 
# CRISPY FORM
 
CRISPY_TEMPLATE_PACK = 'bootstrap4'

STRIPE_PUBLIC_KEY = 'pk_test_lX3r6OMjOU2yzFsNSHq6belT00EY82kZmH'
STRIPE_SECRET_KEY = 'sk_test_tn0CTDaIJHUJyAqhsf39cfsC00LNjsqDnb'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SITE_ID=1
SILENCED_SYSTEM_CHECKS = ['models.E006','admin.E108',"fields.E301"]
 
DATA_UPLOAD_MAX_NUMBER_FILES=50000

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = 'https://matacor.com'
SOCIALACCOUNT_QUERY_EMAIL =True
SOCIALACCOUNT_AUTO_SIGNUP=True
SOCIALACCOUNT_EMAIL_VERIFICATION ="none"
SOCIALACCOUNT_STORE_TOKENS = False
SOCIAL_AUTH_FACEBOOK_KEY  = '1332074261038830'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '9e57419d03907e57fbe2fe2e1d05392a'  # 

#  <!-- <a href="{% url 'social:begin' 'facebook' %}">Login with Facebook</a> -->
 
LANGUAGE_CODE = 'fr'
LANGUAGES = [
    # ('en', _('English')),
    ('fr', _('French')),
    # ('ar', _('Arabic')),
]

LOCALE_PATHS=[
    os.path.join(BASE_DIR,'local')
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Correct SMTP server for Gmail
EMAIL_PORT = 587  # Correct port for Gmail
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'joesdevil10@gmail.com'  # Your Gmail email
EMAIL_HOST_PASSWORD = 'aoud gvmn kpqn auja'  # Your Gmail password
DEFAULT_FROM_EMAIL = 'joesdevil10@gmail.com'


RECAPTCHA_PUBLIC_KEY = "6Ld8xDgpAAAAAE8eMIHSImHYCVc-U4DFfFkyl-BE"
RECAPTCHA_PRIVATE_KEY = "6Ld8xDgpAAAAACDyv6GOLXqvVRIWwkjyQfd6QwLS"