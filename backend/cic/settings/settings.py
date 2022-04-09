from .base import *  # noqa: F401,F403
from opensearchpy.connection import RequestsHttpConnection
from opensearchpy import OpenSearch

ENVIRONMENT = os.getenv('CIC_ENVIRONMENT')

if ENVIRONMENT == 'dev':
    from .dev import * 
elif ENVIRONMENT == 'prod':
    from .prod import *  # noqa: F403
    
AWS_S3_BUCKET_AUTH_STATIC = True
STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_S3_BUCKET_NAME_STATIC  # noqa: F405
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
STATIC_URL = "https://%s.s3.amazonaws.com/" % AWS_S3_BUCKET_NAME_STATIC

OPENSEARCH_URL = os.getenv('OPENSEARCH_URL')

OPENSEARCH = OpenSearch([OPENSEARCH_URL])

OPENSEARCH_DSL = {
    'default': {
        'hosts': OPENSEARCH_URL,
        'port': 443,
        'use_ssl': True,
        'verify_certs': True,
        'connection_class': RequestsHttpConnection,
        'headers': {'Content-Type': 'application/json'}
    },
}

OPENSEARCH_INDEX_NAMES = {
    'apis.documents.grant': 'grant_index',
}
