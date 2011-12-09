# Django settings for the sample OAuth 2.0 authorization server project.
import os


# Custom settings
PROJECT_PATH = os.path.dirname(__file__)
SHARED_PATH = os.path.join(PROJECT_PATH, '..', 'shared')
STATIC_PATH = os.path.join(SHARED_PATH, 'static')


# Django settings
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Elliot Cameron', 'elliot.cameron@covenanteyes.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': ':main:',                # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Detroit'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Used by CommonMiddleware for URL normalization. If APPEND_SLASH is true, URLs
# in the urlconf that don't end with a slash will redirect to URLs that do.
# PREPEND_WWW redirects URLs without `www.` to the same URL, but with the `www.`
APPEND_SLASH = True
PREPEND_WWW = False

# Additional locations of static files
STATICFILES_DIRS = (
    STATIC_PATH,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x6!g(f$$e+p@084ysz!g3&3fe*)u#)ksjr#z5bwb^xov**qrhv'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
    os.path.join(SHARED_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'authorize',
    'clients',
    'scopes',
)


#--TESTING-- Add directory for pauth so we can import it later on.
import sys
sys.path.append('../..')

from pauth import conf


class Middleware(conf.PauthMiddleware):
    def adapt_request(self, cls, request):
        return cls(request.method,
                   self.get_standard_headers(request.META),
                   request.GET if request.method == 'GET' else request.POST)

    def adapt_response(self, response):
        from django.http import HttpResponse
        new_response = HttpResponse(content=response.content,
                                    status=response.status,
                                    content_type=response.content_type)

        for header, value in response.headers.items():
            new_response[header] = value

        return new_response

    def client_is_authorized(self, client, credentials=None):
        return False if credentials is None else client.secret == credentials.secret

    def client_is_registered(self, client):
        return True

    def client_has_scope(self, client, scope):
        return scope in client.allowed_scopes.all()

    def get_client(self, id):
        from clients.models import Client
        try:
            return Client.objects.get(id=id)
        except Client.DoesNotExist:
            return None

    def get_scope(self, scope):
        from scopes.models import Scope
        try:
            return Scope.objects.get(id=scope)
        except Scope.DoesNotExist:
            return None

    def get_standard_headers(self, meta):
        exceptions = ('CONTENT_LENGTH', 'CONTENT_TYPE')
        prefix = 'HTTP_'

        headers = {}
        for field, value in meta.items():
            header = None
            if field.startswith(prefix):
                header = field[len(prefix):]
            elif field in exceptions:
                header = field

            if header is not None:
                header = field.replace('_', '-')
                headers[header] = value

        return headers


conf.initialize(Middleware())
conf.set_default_credentials_readers()
