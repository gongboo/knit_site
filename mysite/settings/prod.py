#production setting
from .base import *

ALLOWED_HOSTS = [
    ".ap-northeast-2.compute.amazonaws.com",
    ".knitvibe.com"
    ] 


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'USER': '',
        # 'PASSWORD': ''
    }
}