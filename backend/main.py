from flask import Flask, request 
from flask_restful import Api, Resource, abort, marshal_with, reqparse, fields
from sqlalchemy import select
from models import Cycle, Cards
from db import SessionLocal

app = Flask(__name__)
api = Api(app)
db = SessionLocal()

cycle_fields = {
    'code' : fields.String,
    'name' : fields.String
}

cycle_list_fields = {
    'cycles' : fields.List(fields.Nested(cycle_fields))
}

card_fields = {
    'image_url' : fields.String
}

class CycleResource(Resource):
    @marshal_with(cycle_fields)
    def get(self, set_code = None):
        # Return specific cycle
        targetCycle = db.scalars((select(Cycle).where(Cycle.code == set_code))).one()
        if targetCycle is None:
            abort(404, "Requested cycle not found")
        return targetCycle  

    
class CycleListResource(Resource):
    @marshal_with(cycle_list_fields)
    def get(self):
        return { "cycles" : db.scalars((select(Cycle))).all() }
    
    
class CardResource(Resource):
    @marshal_with(card_fields)
    def get(self, card_id):
        return db.scalars((select(Cards).where(Cards.id == card_id))).one()
		

api.add_resource(CycleResource, "/cycle/<string:set_code>")
api.add_resource(CycleListResource, "/cycle-list/")
api.add_resource(CardResource, "/card/<int:card_id>")

if __name__ == "__main__":
    app.run(debug=True)