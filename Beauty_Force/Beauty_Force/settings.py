from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(os.getenv('SECRET_KEY'))

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'project.apps.ProjectConfig',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Beauty_Force.urls'

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

WSGI_APPLICATION = 'Beauty_Force.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'project.Users'
AUTHENTICATION_BACKENDS = ['project.backends.EmailBackend']

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30
SESSION_COOKIE_SECURE = True
CART_SESSION_ID = 'cart'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = str(os.getenv('EMAIL_HOST'))
EMAIL_HOST_USER = str(os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_HOST_PASSWORD'))
EMAIL_PORT = str(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS = str(os.getenv('EMAIL_USE_TLS'))

IMPORT_EXPORT_USE_TRANSACTIONS = True

JAZZMIN_SETTINGS = {
    "site_title": "Beauty Force Admin",
    "site_header": "Beauty Force",
    "site_brand": "Beauty Force Admin",
    "site_logo": "images/admin-logo.png",
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Войти в админ-панель Beauty Force",
    "copyright": "Design & development by © BeautyForce™",
    "user_avatar": None,
    "usermenu_links": [
        {"name": "Связаться с разработчиком", "new_window": True},
        {"model": "auth.user"}
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "show_ui_builder": True,
    "custom_css": "css/admin.css",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-teal",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": True,
    "theme": "darkly",
    "dark_mode_theme": "superhero",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": False,
}
