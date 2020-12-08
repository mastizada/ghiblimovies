from pathlib import Path

import environ
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # default setting values
    DEBUG=(bool, False),
    SECRET_KEY=(str, "NotSo@Secret"),
    ALLOWED_HOSTS=(list, ["127.0.0.1"]),
    DATABASE_URL=(str, f"sqlite:///{BASE_DIR}/db.sqlite3"),
    TIME_ZONE=(str, "UTC"),
    USE_I18N=(bool, True),
    USE_L10N=(bool, True),
    USE_TZ=(bool, True),
    CACHE_URL=(str, "dummycache://"),
    CELERY_CACHE_BACKEND=(str, "django-cache"),
    CELERY_BROKER_URL=(str, "memory://"),
    CELERY_TASK_ALWAYS_EAGER=(bool, True),
    SENTRY_DSN=(str, None),
    MOVIES_API_BASE=(str, "https://ghibliapi.herokuapp.com/"),
)

# read the environment file
environ.Env.read_env(env_file=f"{BASE_DIR}/.env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
    "user",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    "actor",
    "movie",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ghiblimovies.urls"

# Templates
template_loaders = ["django.template.loaders.filesystem.Loader", "django.template.loaders.app_directories.Loader"]

# use template caching in production
if not DEBUG:
    template_loaders = [("django.template.loaders.cached.Loader", template_loaders)]  # pragma: no cover

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": template_loaders,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ghiblimovies.wsgi.application"
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644
APPEND_SLASH = True
AUTH_USER_MODEL = "user.User"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {"default": env.db()}

# Cache
CACHES = {
    "default": env.cache(),
}

# Celery settings
CELERY_CACHE_BACKEND = env("CELERY_CACHE_BACKEND")
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_TASK_ALWAYS_EAGER = env("CELERY_TASK_ALWAYS_EAGER")

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGES = (("en", _("English")),)
LANGUAGE_CODE = "en-us"
LOCALE_PATHS = (BASE_DIR / "locale",)

TIME_ZONE = env("TIME_ZONE")
CELERY_TIMEZONE = env("TIME_ZONE")
USE_I18N = env("USE_I18N")
USE_L10N = env("USE_L10N")
USE_TZ = env("USE_TZ")

# Sentry integration
if env("SENTRY_DSN"):
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        integrations=[DjangoIntegration(), CeleryIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=False,
    )

# Logger settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {
        "level": "WARNING",
        "handlers": ["sentry"],
    },
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"},
        "default": {
            "format": "{0}: %(asctime)s %(name)s:%(levelname)s %(message)s: "
            "%(pathname)s:%(lineno)s %(module)s".format("ghiblimovies"),
        },
    },
    "filters": {
        "only_error_levels": {
            "()": "ghiblimovies.utils.ErrorOnlyLogFilter",
        }
    },
    "handlers": {
        "sentry": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "default",
            "filters": ["only_error_levels"],
        },
        "console": {
            "level": "DEBUG" if DEBUG else "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": [] if DEBUG else ["only_error_levels"],
        },
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "gfront": {
            "level": "WARNING",
            "handlers": ["console", "sentry"],
            "propagate": False,
        },
        "gtasks": {
            "level": "INFO",
            "handlers": ["console", "sentry"],
            "propagate": False,
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "{base}/{static}".format(base=BASE_DIR, static=STATIC_URL.strip("/"))

MEDIA_URL = "/media/"
MEDIA_ROOT = "{base}/{static}".format(base=BASE_DIR, static=MEDIA_URL.strip("/"))

# Default admin details
DEFAULT_ADMIN_USERNAME = env("DEFAULT_ADMIN_USERNAME", default=None)
DEFAULT_ADMIN_EMAIL = env("DEFAULT_ADMIN_EMAIL", default=None)
DEFAULT_ADMIN_PASS = env("DEFAULT_ADMIN_PASS", default=None)

# External API
MOVIES_API_BASE = env("MOVIES_API_BASE")
