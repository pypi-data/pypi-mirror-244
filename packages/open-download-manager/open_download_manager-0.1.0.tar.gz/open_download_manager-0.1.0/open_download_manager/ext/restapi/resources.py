from flask import abort, jsonify, request
from flask_restful import Resource
from flask_simplelogin import login_required

from open_download_manager.ext.database import db
from open_download_manager.models import Product, Download

class ProductResource(Resource):
    def get(self):
        products = Product.query.all() or abort(204)
        return jsonify(
            {"products": [product.to_dict() for product in products]}
        )

    @login_required(basic=True, username="admin")
    def post(self):
        """
        Creates a new product.

        Only admin user authenticated using basic auth can post
        Basic takes base64 encripted username:password.

        # curl -XPOST localhost:5000/api/v1/product/ \
        #  -H "Authorization: Basic Y2h1Y2s6bm9ycmlz" \
        #  -H "Content-Type: application/json"
        """
        return NotImplementedError(
            "Someone please complete this example and send a PR :)"
        )


class ProductItemResource(Resource):
    def get(self, product_id):
        product = Product.query.filter_by(id=product_id).first() or abort(404)
        return jsonify(product.to_dict())

class DownloadItemResource(Resource):
    def get(self, download_id):
        product = Download.query.filter_by(id=download_id).first() or abort(404)
        return jsonify(product.to_dict())
    
    def put(self, download_id):
        content = request.json
        db.session.query(Download).filter(Download.id==download_id).update({Download.running: content["action"]})
        db.session.commit()
        return jsonify({"status": "ok"})
    
    def delete(self, download_id):
        download = Download.query.filter_by(id=download_id).first() or abort(404)
        db.session.delete(download)
        db.session.commit()
        return jsonify({"status": "ok"})

class DownloadResource(Resource):
    def get(self):
        downloads = Download.query.all() or abort(204)
        return jsonify(
            {"downloads": [download.to_dict() for download in downloads]}
        )

    def post(self):
        """
        Creates a new download.

        # curl -XPOST localhost:5000/api/v1/download/ \
        #  -H "Content-Type: application/json"
        """
        content = request.json
        new_download = Download(url=content["url"], status=float(), path=content["path"], content_length=-1, running=False)
        db.session.add(new_download)
        db.session.commit()
        print("test")
        result = download.delay(content["url"])

        print("Task ID: ", result.id)

        return {
            "task_id": result.id,
        }, 201