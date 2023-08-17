DEBUG = False

ALLOWED_HOSTS = ['*']


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "cms_db",
        "USER": "cms_user",
        "PASSWORD": "maybeimaybeu",
        "HOST": "db",
        "PORT": "5432",
    }
}
