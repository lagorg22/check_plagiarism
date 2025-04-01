BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-_5==wkw81y3@jys4ocyy^m6$)a1zm+lki)v91tr^vcml!j1v&v'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'rest_framework',
'drf_yasg',
'django_filters',
'products',
'users',
'rest_framework_simplejwt.token_blacklist',  # <-- Added for JWT token blacklisting
'cart',
'orders',
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
ROOT_URLCONF = 'MyShop.urls'
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
WSGI_APPLICATION = 'MyShop.wsgi.application'
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'myshop',
'USER': 'postgres',
'PASSWORD': 'lashaL001',
'HOST': 'localhost',
'PORT': '5432',
}
}
REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': (
'rest_framework_simplejwt.authentication.JWTAuthentication',
),
'DEFAULT_PERMISSION_CLASSES': (
'rest_framework.permissions.AllowAny',
),
'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}
SWAGGER_SETTINGS = {
'USE_SESSION_AUTH': False,
'SECURITY_DEFINITIONS': {
'Bearer': {
'type': 'apiKey',
'name': 'Authorization',
'in': 'header'
}
},
'SECURITY': [
{
'Bearer': []
}
],
'PERSIST_AUTH': True,
'REFETCH_SCHEMA_WITH_AUTH': True,
'REFETCH_SCHEMA_ON_LOGOUT': True,
'OPERATIONS_SORTER': 'alpha',
'TAGS_SORTER': 'alpha',
'DOC_EXPANSION': 'none',
'DEFAULT_MODEL_RENDERING': 'model',
'DEFAULT_INFO': {
'contact': {
'name': 'API Support',
'url': 'http://www.example.com/support',
'email': 'support@example.com'
},
'license': {},
'version': '1.0.0',
},
}
SIMPLE_JWT = {
'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
'ROTATE_REFRESH_TOKENS': False,
'BLACKLIST_AFTER_ROTATION': True,
'UPDATE_LAST_LOGIN': False,
'ALGORITHM': 'HS256',
'SIGNING_KEY': SECRET_KEY,
'VERIFYING_KEY': None,
'AUDIENCE': None,
'ISSUER': None,
'AUTH_HEADER_TYPES': ('Bearer',),
'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
'USER_ID_FIELD': 'id',
'USER_ID_CLAIM': 'user_id',
'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
'TOKEN_TYPE_CLAIM': 'token_type',
'JTI_CLAIM': 'jti',
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'products', 'media')