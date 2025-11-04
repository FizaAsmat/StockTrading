from .settings import *

# Override database settings for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',   # or BASE_DIR / 'test_db.sqlite3'
    }
}
