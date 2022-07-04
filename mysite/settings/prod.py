#production setting
from .base import *

ALLOWED_HOSTS = [".ap-northeast-2.compute.amazonaws.com"] #고정 아이피 넣으랬는데 고정 아이피는 공개해도 되는 건지 몰라서 일단 전체 공개함


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'USER': '',
        # 'PASSWORD': ''
    }
}