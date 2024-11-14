import json 
import sys
import re
from models import get_engine, Cards, Investigators, Player_Cards, Assets, Traits, Uses, Asset_Uses
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# 1) Read entire set file
# 2) Iterate through cards one by one
# 3) For each card, start with adding a "card entry"
# 4) Methods here handle converting to a python dict, then pass to models functions
# to add to the database
# 5) Then detect if player or investigator card and fill out corresponding entry
# 6) Add relevant deckbuilding options, card traits, factions, uses, symbols, etc.

valid_types = ["investigator", "asset", "event", "skill"]

# Takes a bulk JSON file of a set from ArkhamDB and converts it to the
# correct models
def convert_bulk_json(json_file):
    print("Converting Set:", json_file)
    with open(json_file, 'r') as file:
        # Load the set as a python dict
        set = json.load(file)
        engine = get_engine(True)

        with Session(engine) as session:
            for card in set:
                if card['type_code'] in valid_types:
                    create_card(card, session)                        

def create_card(json_card, session):
    db_card = Cards()
    db_card = set_attr(json_card, db_card, Cards)     
    session.add(db_card)
    
    if "traits" in json_card:
        trait_list = json_card['traits'].split(". ")
        for trait in trait_list:
            add_trait(trait, db_card, session) 
    
    if json_card['type_code'] == "investigator":
        db_investigator = Investigators()
        db_investigator = set_attr(json_card, db_investigator, Investigators) 
        
        db_investigator.card_text, db_investigator.elder_sign = json_card['text'].split("\n[elder_sign] effect: ")

        # TODO: Create "deckbuilding_options" here
        
        db_card.investigators.append(db_investigator)
        session.add(db_investigator)
    
    elif json_card['type_code'] in ["asset", "event", "skill"]:
        db_player_card = Player_Cards()
        db_player_card = set_attr(json_card, db_player_card, Player_Cards)
        db_card.player_cards.append(db_player_card)
        session.add(db_player_card)
        
        if json_card['type_code'] == 'asset':
            db_asset_card = Assets()
            db_asset_card = set_attr(json_card, db_asset_card, Assets)
            db_player_card.assets.append(db_asset_card)
            session.add(db_asset_card)
            
            if 'text' in json_card:
                match = re.search("Uses \((\d+) (\w+)\)", json_card['text'])
                if match:
                    add_uses(match.group(2), int(match.group(1)), db_asset_card, session)
    
    session.commit()

def add_trait(trait_name, parent_card, session):
    # If new trait, create it and add to card
    db_trait = session.scalars(select(Traits).where(Traits.trait == trait_name)).first()
    if db_trait is None:
        print("New trait! ", trait_name)
        db_trait = Traits(trait = trait_name)
        session.add(db_trait)
    
    parent_card.traits.append(db_trait)


def add_uses(type, total_uses, child_asset, session):
    # In new use type, create it and add to card
    db_uses = session.scalars(select(Uses).where(Uses.type == type)).first()
    if db_uses is None:
        print("New use type! ", type)
        db_uses = Uses(type = type)
        session.add(db_uses)
    
    # Add uses and asset to the association table
    asset_uses = Asset_Uses(num_uses = total_uses)
    asset_uses.asset = child_asset
    db_uses.assets.append(asset_uses)
    session.add(asset_uses)
        
        
"""
Maps attributes from a JSON object to a database model instance.

This function iterates over the public attributes of a given database model
(specified by `table`) and sets the corresponding attributes in the `db_card`
instance based on the `json_card` dictionary. If a mapping exists in the 
`ATTRIBUTE_DB_TO_JSON` dictionary, it uses the mapped JSON attribute name;
otherwise, it uses the attribute name directly. The function skips any 
attribute named "traits".

Parameters:
- json_card (dict): The source data in JSON format with attributes to map.
- db_card (object): The database model instance where attributes will be set.
- table (class): The database model class, used to retrieve its attribute names.

Returns:
- db_card (object): The updated database model instance with attributes set.
"""
def set_attr(json_card, db_card, table):
    # Get the table's attributes
    db_attributes = dir(table)
    db_attributes = [attr for attr in db_attributes if attr[0] != "_"]
    
    for db_attr in db_attributes:
        # If JSON attribute is different, translate
        json_attr = ATTRIBUTE_DB_TO_JSON.get(db_attr, db_attr)

        if json_attr in json_card and json_attr != "traits":
            setattr(db_card, db_attr, json_card[json_attr])
            
    
    print("New Card:", db_card)
    return db_card    


ATTRIBUTE_DB_TO_JSON = {
    'cycle' : 'pack_name',
    'card_pack' : 'pack_name',
    'collector_number' : 'position',
    'artist' : 'illustrator',
    'nickname' : 'subname',
    'willpower' : 'skill_willpower',
    'intellect' : 'skill_intellect',
    'combat' : 'skill_combat',
    'agility' : 'skill_agility',
    'flavor_back' : 'back_flavor',
    'flavor_front' : 'flavor',
    'type' : 'type_code',
    'resource_cost' : 'cost',
}


if __name__ == "__main__":
    filename = sys.argv[1]
    convert_bulk_json(filename)