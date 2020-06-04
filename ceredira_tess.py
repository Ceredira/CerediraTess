import json
import logging.config
import sys
from functools import partial

from CerediraTess.agents_locker import AgentsLocker
from CerediraTess.server import ThreadingSimpleServer, Handler
from CerediraTess.utility import decode_complex

USE_HTTPS = False
list_of_agents = None
list_of_users = None


if __name__ == '__main__':
    try:
        with open('agents.json') as agents_config:
            list_of_agents = json.loads(agents_config.read(), object_hook=decode_complex)

        with open('users.json') as users_config:
            list_of_users = json.loads(users_config.read(), object_hook=decode_complex)

        agents_locker = AgentsLocker(list_of_agents)

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
                myHandler = partial(Handler, list_of_agents, list_of_users, agents_locker)
                server = ThreadingSimpleServer(('0.0.0.0', 4444), myHandler)
                if USE_HTTPS:
                    import ssl

                    logger.info('Using HTTPS')
                    server.socket = ssl.wrap_socket(server.socket, keyfile='./key.pem', certfile='./cert.pem',
                                                    server_side=True)
                else:
                    logger.info('Does not using HTTPS')

                server.serve_forever()
                logger.info('Starting server, use <Ctrl-C> to stop')
            except KeyboardInterrupt:
                logger.info('Server stopped')
        else:
            logger.info('Supporting only Windows OS.')

    except Exception as ex:
        print(ex)
