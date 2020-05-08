import logging.config
import sys

from CerediraTess.server import ThreadingSimpleServer, Handler

USE_HTTPS = False


def run():
    dictLogConfig = {
        "version": 1,
        "handlers": {
            'console': {
                'class': 'logging.StreamHandler',
                "formatter": "myFormatter",
                'level': 'DEBUG',
            },
            "fileHandler": {
                "class": "logging.FileHandler",
                "formatter": "myFormatter",
                "filename": "log.log"
            }
        },
        "loggers": {
            "CerediraTess": {
                "handlers": ["fileHandler", "console"],
                "level": "DEBUG",
            }
        },
        "formatters": {
            "myFormatter": {
                # "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                'format': '%(asctime)s %(levelname)s: %(process)d %(thread)d %(name)s %(message)s'
            }
        }
    }

    logging.config.dictConfig(dictLogConfig)
    logger = logging.getLogger('CerediraTess')

    if sys.platform.startswith('win32'):
        logger.info('Starting on Windows OS')
        try:
            logger.info('Using port: 4444')
            server = ThreadingSimpleServer(('0.0.0.0', 4444), Handler)
            if USE_HTTPS:
                import ssl
                logger.info('Using HTTPS')
                server.socket = ssl.wrap_socket(server.socket, keyfile='./key.pem', certfile='./cert.pem', server_side=True)
            else:
                logger.info('Does not using HTTPS')

            server.serve_forever()
            logger.info('Starting server, use <Ctrl-C> to stop')
        except KeyboardInterrupt:
            logger.info('Server stopped')
    else:
        logger.info('Supporting only Windows OS.')


if __name__ == '__main__':
    run()
