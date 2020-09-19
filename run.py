import multiprocessing

from cerediratess import create_app

app = create_app()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app.run(host="0.0.0.0", port=7801, debug=True)
