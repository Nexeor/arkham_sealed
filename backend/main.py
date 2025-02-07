from flask import Flask, request 
from flask_restful import Api, Resource, abort, marshal_with, reqparse, fields
from flask_cors import CORS
from sqlalchemy import select
from models import Cycle, Cards
from db import SessionLocal

app = Flask(__name__)
api = Api(app)
db = SessionLocal()
CORS(app)

cycle_fields = {
    'code' : fields.String,
    'name' : fields.String
}

cycle_list_fields = {
    'cycles' : fields.List(fields.Nested(cycle_fields))
}

card_fields = {
    'name' : fields.String,
    'type' : fields.String,
    'image_url' : fields.String,
    'faction': fields.String(attribute=lambda card: get_card_faction(card))
}

card_list_fields = {
    'cards' : fields.List(fields.Nested(card_fields))
}

def get_card_faction(card):
    """Retrieve the faction name for a given card."""
    if card.investigator:
        return card.investigator.faction.faction_name
    elif card.player_card:
        return card.player_card.faction.faction_name
    return "Neutral"

class CycleResource(Resource):
    @marshal_with(cycle_fields)
    def get(self, cycle_code = None):
        # Return specific cycle
        targetCycle = db.scalars((select(Cycle).where(Cycle.code == cycle_code))).one()
        if targetCycle is None:
            abort(404, "Requested cycle not found")
        return targetCycle  

    
class CycleListResource(Resource):
    @marshal_with(cycle_list_fields)
    def get(self):
        return { "cycles" : db.scalars((select(Cycle))).all() }
    
    
class CardResource(Resource):
    @marshal_with(card_fields)
    def get(self):
        card_id = request.args.get('id')
        if card_id:
            return db.scalars((select(Cards).where(Cards.id == card_id))).one()
        return db.scalars((select(Cards).where(Cards.id == 1))).one()
    
class CardsResource(Resource):
    @marshal_with(card_list_fields)
    def get(self):
        cycle_code = request.args.get('cycle_code')
        # If cycle_code provided, fetch the cycle then the cards
        if cycle_code:
            cycle = db.scalars(select(Cycle).where(Cycle.code == cycle_code)).one_or_none()
            if not cycle:
                abort(404, message=f"Cycle with code {cycle_code} not found")
            
            return {"cards" : db.scalars(select(Cards).where(Cards.cycle == cycle)).all()}
        
        cycle = db.scalars(select(Cycle).where(Cycle.code == "core")).one()
        print(cycle)
        cards = db.scalars((select(Cards).where(Cards.cycle == cycle))).all()
        print(cards)

        # Otherwise return core set
        return { "cards" : cards}

api.add_resource(CycleResource, "/cycle/<string:cycle_code>")
api.add_resource(CycleListResource, "/cycle-list/")
api.add_resource(CardResource, "/card/")
api.add_resource(CardsResource, "/cards/cycle/"), 

if __name__ == "__main__":
    app.run(debug=True)