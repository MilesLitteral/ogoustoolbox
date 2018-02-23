# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
#CDN_DOMAIN = 'cdn.ogous/'
#CDN_TIMESTAMP = False

SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/ogous?user=postgres&password=Getter77'
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'f=l#6@awducftk0cjf2(4kh8v6fyj7$#4$pfxq8c797t@)x3q8'
DROPBOX_KEY = '9XRZVbmMaVwAAAAAAAABeXFnZ0cRf-cI61_W9ORnJRrfS-E5r9gICDjFm_1_KBAR'
#	2z8npgia1mm9wkc
DROPBOX_SECRET = '74onftjmr0axp68'
DROPBOX_ACCESS_TYPE = 'app_folder'

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
#SASORIZERO
CSRF_SESSION_KEY = "c24745ca4af85a86be52f88faceb9268"

# Secret key for signing cookies
#DEIDARA
SECRET_KEY = "4F24CADBF86ED8AA93B910FEBA73EB593EAD9A02B0ECEEF9927B3B3D4E707C90"