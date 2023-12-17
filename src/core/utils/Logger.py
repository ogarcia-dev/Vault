import os
import logging
import logging.config
from datetime import datetime



LOGGING_DIR = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log"),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'uvicorn': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'fastapi': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'tortoise': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)