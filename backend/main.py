from flask import Flask, request 
from flask_restful import Api, Resource, abort, marshal_with, reqparse, fields
from sqlalchemy import select
from models import Cycle
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
        print(db.scalars((select(Cycle))).all())
        return { "cycles" : db.scalars((select(Cycle))).all() }
		

api.add_resource(CycleResource, "/cycle/<string:set_code>")
api.add_resource(CycleListResource, "/cycle-list/")

if __name__ == "__main__":
    app.run(debug=True)