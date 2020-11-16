import multiprocessing

from ceredira_tess import create_app
from config import Config

app = create_app()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    if Config.SERVER_HTTPS:
        app.run(host=Config.SERVER_HOST, port=Config.SERVER_PORT, debug=Config.DEBUG,
                ssl_context=(Config.SERVER_CERT, Config.SERVER_KEY), threaded=True)
    else:
        app.run(host=Config.SERVER_HOST, port=Config.SERVER_PORT, debug=Config.DEBUG, threaded=True)
