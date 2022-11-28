from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema, TagAndItemSchema

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import TagModel, StoreModel, ItemModel

blp = Blueprint("Tags", __name__, description = "Operations on tags")

@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many = True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id).first():
            abort(400, message = "A tag with that name already exists in that store.")

        tag = TagModel(**tag_data, store_id = store_id)

        try:
            db.session.add(tag)
            db.session.commit()
            return tag
        except SQLAlchemyError as e:
            abort(500, message = str(e))

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return {"message": "Tag deleted!"}, 200

@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
            return tag
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")


