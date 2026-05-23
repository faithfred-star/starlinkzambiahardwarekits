import os
from pathlib import Path

# 📂 Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Security Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'starlinkzambiahardwarekits.onrender.com',
    'localhost',
    '127.0.0.1'
]

# 📦 Installed Application Definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'orders',  # Main business logic application folder
]

# ⚙️ Middleware Pipeline (With optimized WhiteNoise setup)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must sit directly beneath SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🔗 Root Routing Options
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

# 🎨 Template Engines Layout
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

# 🗄️ Database Configurations (Persistent SQLite standard for basic Render instance builds)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔒 Account Security & Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Localization & Region Rules (Fully Synced for Zambia Ecosystem)
LANGUAGE_CODE = 'en-zm'            # Formats dates, values, and language settings to Zambia (English)
TIME_ZONE = 'Africa/Lusaka'        # Sets administrative and creation clock to Central Africa Time (CAT)
USE_I18N = True
USE_TZ = True

# 📁 Static Files Asset Pipeline (Engineered for Render High-Tolerance)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ✅ Django 4.2+ Storage Routing Model
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # CompressedStaticFilesStorage safeguards production builds against missing image runtime 500 crashes
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# 🧱 Structural Default Identity Model
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🤖 Automated Bot Notifications (With production fail-safe default values)
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'NENHUM_TOKEN_CONFIGURADO')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'NENHUM_ID_CONFIGURADO')