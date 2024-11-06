import json 
import sys
from models import get_engine, Cards, Investigators, Player_Cards, Asset_Card, Skill_Card, Event_Card
from sqlalchemy.orm import Session

# 1) Read entire set file
# 2) Iterate through cards one by one
# 3) For each card, start with adding a "card entry"
# 4) Methods here handle converting to a python dict, then pass to models functions
# to add to the database
# 5) Then detect if player or investigator card and fill out corresponding entry
# 6) Add relevant deckbuilding options, card traits, factions, uses, symbols, etc.


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
                if card['type_code'] in ["investigator", "asset", "event", "skill"]:
                    db_card = create_card_v2(card, Cards)
                    session.add(db_card)
                    session.commit()

                    if card['type_code'] == "investigator":
                        db_investigator = create_card_v2(card, Investigators)

                        card_text, elder_sign = card["text"].split("\n[elder_sign] effect: ") 
                        db_investigator.card_text = card_text
                        db_investigator.elder_sign = elder_sign

                        db_card.investigators.append(db_investigator)
                        session.add(db_investigator)
                        session.commit()   

                    if card['type_code'] in ["asset", "event", "skill"]:
                        db_player_card = create_card_v2(card, Player_Cards)
                        db_card.player_cards.append(db_player_card)
                        session.add(db_player_card)
                        session.commit()
                        
                        if card['type_code'] == 'asset':
                            db_asset_card = create_card_v2(card, Asset_Card)
                            db_player_card.assets.append(db_asset_card)
                            session.add(db_asset_card)
                            session.commit()

                        if card['type_code'] == 'event':
                            db_event_card = create_card_v2(card, Event_Card)
                            db_player_card.assets.append(db_event_card)
                            session.add(db_event_card)
                            session.commit()
                        
                        if card['type_code'] == 'skill':
                            db_skill_card = create_card_v2(card, Skill_Card)
                            db_player_card.assets.append(db_skill_card)
                            session.add(db_skill_card)
                            session.commit()
                        



def create_card_v2(json_card, table):
    db_card = table()
    db_card = set_attr(json_card, db_card, table)      

    return db_card
        

def set_attr(json_card, db_card, table):
    # Get the table's attributes
    db_attributes = dir(table)
    db_attributes = [attr for attr in db_attributes if attr[0] != "_"]
    
    for db_attr in db_attributes:
        # If JSON attribute is different, translate
        json_attr = ATTRIBUTE_DB_TO_JSON.get(db_attr, db_attr)

        if json_attr in json_card:
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