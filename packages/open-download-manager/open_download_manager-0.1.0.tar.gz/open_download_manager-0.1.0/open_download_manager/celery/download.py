import requests
import logging
import os
from celery import shared_task

from open_download_manager.models import Download
from open_download_manager.ext.database import db

@shared_task(ignore_result=False)
def download(dl_id: int) -> int:
    """Celery Process to download a file from a URL."""

    dl = Download.query.filter_by(id=dl_id).first()

    if dl is None:
        logging.error("Download not found in db, id='%s'", id)
        return -1

    file_name = f"temp_content/{dl_id}"
    try:
        with open(file_name, "wb") as f:
            response = requests.get(dl.url, stream=True)
            total_length = response.headers.get('content-length')
            written = 0
            if total_length is None: # no content length header
                f.write(response.content)
            else:
                total_length = int(total_length)
                db.session.query(Download).filter(Download.id==dl_id).update({Download.content_length: total_length})
                db.session.query(Download).filter(Download.id==dl_id).update({Download.running: True})
                db.session.commit()
                for data in response.iter_content(chunk_size=4096):
                    written += len(data)
                    db.session.query(Download).filter(Download.id==dl_id).update({Download.status: float(written/total_length*100)})
                    db.session.commit()
                    f.write(data)
        
        os.rename(file_name, dl.path)

    except Exception as e: # pylint: disable=broad-except
        logging.error("Error downloading file, id='%s', error='%s'", id, e)
        return -1