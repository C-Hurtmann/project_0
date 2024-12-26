import logging
import logging.config


logging.config.dictConfig(
    {
        'version': 1,
        'formatters': {
            'standard': {
                '()': 'colorlog.ColoredFormatter',
                'format': (
                    '%(log_color)s%(asctime)s - %(levelname)-8s:: %(message)s'
                ),
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'log_colors': {
                    'DEBUG': 'yellow',
                    'INFO': 'white',
                    'ERROR': 'red',
                },
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            }
        }
    }
)

Logger = logging.getLogger(__name__)
