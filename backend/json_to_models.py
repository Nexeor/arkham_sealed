import json 
import sys
from models import get_engine, Cards, Investigators, Player_Cards, Assets, Traits
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
                    db_card = create_card(card, Cards)
                    session.add(db_card)
                    # session.commit()
                    
                    if "traits" in card:
                        trait_list = card['traits'].split(". ")
                        for trait in trait_list:
                            add_trait(trait, db_card, session)

                    if card['type_code'] == "investigator":
                        db_investigator = create_card(card, Investigators)

                        card_text, elder_sign = card["text"].split("\n[elder_sign] effect: ") 
                        db_investigator.card_text = card_text
                        db_investigator.elder_sign = elder_sign

                        db_card.investigators.append(db_investigator)
                        session.add(db_investigator)
                        session.commit()   

                    if card['type_code'] in ["asset", "event", "skill"]:
                        db_player_card = create_card(card, Player_Cards)
                        db_card.player_cards.append(db_player_card)
                        session.add(db_player_card)
                        session.commit()
                        
                        if card['type_code'] == 'asset':
                            db_asset_card = create_card(card, Assets)
                            db_player_card.assets.append(db_asset_card)
                            session.add(db_asset_card)
                            session.commit()
                        

def create_card(json_card, table):
    db_card = table()
    db_card = set_attr(json_card, db_card, table)      

    return db_card

def add_trait(trait_name, db_card, session):
    # In new trait, create and add to card
    db_trait = session.scalars(select(Traits).where(Traits.trait == trait_name)).first()
    if db_trait is None:
        print("New trait! ", trait_name)
        db_trait = Traits(trait = trait_name)
        session.add(db_trait)
    
    db_card.traits.append(db_trait)
    session.commit()
        

def set_attr(json_card, db_card, table):
    # Get the table's attributes
    db_attributes = dir(table)
    db_attributes = [attr for attr in db_attributes if attr[0] != "_"]
    
    for db_attr in db_attributes:
        print(db_attr)
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