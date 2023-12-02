from flask import abort, render_template, request, redirect
from flask_simplelogin import login_required

from open_download_manager.models import Product, Download
from open_download_manager.ext.database import db
from open_download_manager.celery.download import download

def index():
    downloads = Download.query.filter(Download.status != 100.0).all()
    return render_template("index.html", downloads=downloads)


def product(product_id):
    product = Product.query.filter_by(id=product_id).first() or abort(
        404, "produto nao encontrado"
    )
    return render_template("product.html", product=product)

def create_download():
    if request.method == "GET":
        return render_template("create_download.html")
    else:
        new_download = Download(url=request.form["url"], running=False, status=0, path=request.form["path"])
        db.session.add(new_download)
        db.session.commit()
        result = download.delay(new_download.id)
        print(f"Task ID: {result.id} created")

        return redirect("/")

def delete_download():
    download_id = request.form["id"]
    download = Download.query.filter_by(id=download_id).first() or abort(
        404, "download doesn't exist"
    )
    db.session.delete(download)
    db.session.commit()
    return redirect("/")

@login_required
def secret():
    return "This can be seen only if user is logged in"


@login_required(username="admin")
def only_admin():
    return "only admin user can see this text"
