from typing import Type

from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models import Advertisement, DSN, Base
from schema import validate, CreateAdvertisementSchema, HttpError, PatchAdvertisementSchema

engine = create_engine(DSN)
Session = sessionmaker(bind=engine)


def get_by_id(item_id: int, orm_model: Type[Advertisement], session):
    orm_item = session.query(orm_model).get(item_id)
    if orm_item is None:
        raise HttpError(404, "item not found")
    return orm_item


class AdvertisementView(MethodView):

    @staticmethod
    def get(advertisement_id: int):
        with Session() as session:
            advertisement = get_by_id(advertisement_id, Advertisement, session)
            return jsonify(
                {
                    "title": advertisement.title,
                    "owner": advertisement.owner,
                    "created_at": advertisement.created_at.isoformat(),
                }
            )

    @staticmethod
    def post():
        json_data = request.json
        with Session() as session:
            new_advertisement = Advertisement(**validate(json_data, CreateAdvertisementSchema))
            session.add(new_advertisement)
            session.commit()
            return jsonify({'status': "ok", 'id': new_advertisement.id})

    @staticmethod
    def patch(advertisement_id: int):
        data_to_patch = validate(request.json, PatchAdvertisementSchema)
        with Session() as session:
            advertisement = get_by_id(advertisement_id, Advertisement, session)
            for field, value in data_to_patch.items():
                setattr(advertisement, field, value)
            session.commit()
            return jsonify({"status": "success"})

    @staticmethod
    def delete(advertisement_id: int):
        with Session() as session:
            advertisement = get_by_id(advertisement_id, Advertisement, session)
            session.delete(advertisement)
            session.commit()
            return jsonify({"advertisement_delete": "success"})


Base.metadata.create_all(engine)
