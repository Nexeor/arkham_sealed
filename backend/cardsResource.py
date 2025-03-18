from flask_restful import Resource, fields, marshal
from models import Cards
from sqlalchemy import select
from db import db

card_fields = {
    'name' : fields.String,
    'type' : fields.String,
    'image_url' : fields.String,
    'faction': fields.String(attribute=lambda card: get_card_faction(card))
}

def get_card_faction(card):
    """Retrieve the faction name for a given card."""
    if card.investigator:
        return card.investigator.faction.faction_name
    elif card.player_card:
        return card.player_card.faction.faction_name
    return "Neutral"

class CardsResource(Resource):
    # Return all cards in DB
    # TODO: Param filtering
    def get(self):
        result = db.scalars((select(Cards).where(Cards.type == "asset"))).all()
        return [marshal(card, card_fields) for card in result]