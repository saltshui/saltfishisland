﻿"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost ', '.saltfishisland.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pure_pagination',
    'haystack',
    'ckeditor',
    'blog',  
    'users',
    'comment',
    'notifications',
    'notice',
    'captcha',
    'mptt',
    'subscribe',
    'django_mathjax',
    'sendemail',
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

ROOT_URLCONF = 'saltfishisland.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'saltfishisland.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT  = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

#其他设置

#使用自定义用户模型
AUTH_USER_MODEL = 'users.User'
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

# 搜索设置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'blog.elasticsearch2_ik_backend.Elasticsearch2IkSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'saltfishisland',
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_CUSTOM_HIGHLIGHTER = 'blog.utils.Highlighter'


#允许同域页面展示
X_FRAME_OPTIONS = 'SAMEORIGIN'

#邮件设置

#将邮件发送至控制台
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = "saltfishisland@163.com" # 帐号
EMAIL_HOST_PASSWORD = ""  # 授权码（****）
DEFAULT_FROM_EMAIL = "鱼咸岛外籍大佬管理委员会 <saltfishisland@163.com>"

#邮件验证口令有效期设置（单位为秒）
TOKEN_EXPIRATION = 3600

#富文本编辑器设置（评论）
CKEDITOR_CONFIGS = {
    'default': {
        # 编辑器宽度自适应
        'width':'auto',
        'height':'250px',
        # tab键转换空格数
        'tabSpaces': 4,
        # 工具栏风格
        'toolbar': 'Custom',
        # 工具栏按钮
        'toolbar_Custom': [
            # 表情 代码块
            ['Smiley', 'CodeSnippet'],
            # 字体风格
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            # 字体颜色
            ['TextColor', 'BGColor'],
            # 链接
            ['Link', 'Unlink'],
            # 列表
            ['NumberedList', 'BulletedList'],
            # 最大化
            ['Maximize']
        ],
        # 加入代码块插件
        'extraPlugins': ','.join(['codesnippet',]),
    }
}

# django-pure-pagination 分页设置
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 4, # 分页条当前页前后应该显示的总页数（两边均匀分布），
    'MARGIN_PAGES_DISPLAYED': 2, # 分页条开头和结尾显示的页数
    'SHOW_FIRST_PAGE_WHEN_INVALID': True, # 当请求了不存在的页面，显示第一页
}

#验证码相关
#样式分别为输入框，图片和用于验证的隐藏框
CAPTCHA_FIELD_TEMPLATE = os.path.join(BASE_DIR, 'templates/captcha/field_template.html')
CAPTCHA_TEXT_FIELD_TEMPLATE = os.path.join(BASE_DIR, 'templates/captcha/text_template.html')
CAPTCHA_IMAGE_TEMPLATE = os.path.join(BASE_DIR, 'templates/captcha/image_template.html')
#CAPTCHA_HIDDEN_FIELD_TEMPLATE = os.path.join(BASE_DIR, 'templates/captcha/hidden_template.html')

# 噪点样式
CAPTCHA_NOISE_FUNCTIONS = (#'captcha.helpers.noise_null', # 没有样式
     'captcha.helpers.noise_arcs', # 线
     'captcha.helpers.noise_dots', # 点
)

# 验证码图片
#CAPTCHA_IMAGE_SIZE = (100, 25)
CAPTCHA_BACKGROUND_COLOR = '#ffffff'

#验证码样式
#CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge' #随机英文字母
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'    #数字表达式

#CAPTCHA_LENGTH = 4 # 字符个数
CAPTCHA_TIMEOUT = 1 # 超时(minutes)


MATHJAX_ENABLED=True
