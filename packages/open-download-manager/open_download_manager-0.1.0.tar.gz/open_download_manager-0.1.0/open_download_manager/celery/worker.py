from open_download_manager import create_app_wsgi

app = create_app_wsgi()  # noqa
celery_app = app.extensions["celery"]  # noqa

def main():
    celery_app.Worker().start()