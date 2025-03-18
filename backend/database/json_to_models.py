import json 
import sys
import re
from backend.database.models import get_engine, Cards, Investigators, Player_Cards, Assets, Traits, Uses, Asset_Uses, Factions, Deckbuilding_Options, Treacheries, Cycle
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

# 1) Read entire set file
# 2) Iterate through cards one by one
# 3) For each card, start with adding a "card entry"
# 4) Methods here handle converting to a python dict, then pass to models functions
# to add to the database
# 5) Then detect if player or investigator card and fill out corresponding entry
# 6) Add relevant deckbuilding options, card traits, factions, uses, symbols, etc.

valid_types = ["investigator", "asset", "event", "skill", "treachery"]

# Takes a bulk JSON file of a set from ArkhamDB and converts it to the
# correct models
def convert_bulk_json(json_file, debug):
    print("Converting Set:", json_file)
    with open(json_file, 'r') as file:
        # Load the set as a python dict
        set = json.load(file)
        engine = get_engine(rebuild=True, debug=debug)

        with Session(engine) as session:
            add_factions(session)
            add_cycles(session)
            for card in set:
                if card['type_code'] in valid_types:
                    create_card(card, session)     
                
            connect_investigator_cards(session)   

def create_card(json_card, session):
    db_card = Cards()
    db_card = set_attr(json_card, db_card, Cards, session)     
    session.add(db_card)
    
    if "traits" in json_card:
        trait_list = json_card['traits'].split(". ")
        for trait in trait_list:
            add_trait(trait, db_card, session) 
    
    if json_card['type_code'] == "investigator":
        db_investigator = Investigators()
        db_investigator = set_attr(json_card, db_investigator, Investigators, session) 
        
        # Parse front text
        db_investigator.card_text, db_investigator.elder_sign = json_card['text'].split("\n[elder_sign] effect: ")
        
        # Parse back text
        sections = json_card['back_text'].split("<b>")
        db_investigator.deck_size = sections[1].split("</b>:")[1].strip().split("\n")[0].strip(" .")
        db_investigator.deckbuilding_options_text = sections[2].split("</b>:")[1].strip().split("\n")[0]
        db_investigator.deckbuilding_requirements_text = sections[3].split("</b>")[1].strip().replace("(do not count toward deck size):", "").strip()
        
        # TODO: Create "deckbuilding_options" here
        
        db_card.investigator = db_investigator
        session.add(db_investigator)
    
    elif json_card['type_code'] in ["asset", "event", "skill"]:
        db_player_card = Player_Cards()
        db_player_card = set_attr(json_card, db_player_card, Player_Cards, session)
        db_card.player_card = db_player_card
        session.add(db_player_card)
        
        # Indicate weakness
        if "subtype_code" in json_card and json_card['subtype_code'] == "weakness":
            print("New weakness")
            db_player_card.is_weakness = True
        
        if json_card['type_code'] == 'asset':
            print("Creating new asset:", json_card['name'])
            db_asset_card = Assets()
            db_asset_card = set_attr(json_card, db_asset_card, Assets, session)
            db_player_card.asset = db_asset_card
            session.add(db_asset_card)
                
            if 'text' in json_card:
                match = re.search(r"Uses \((\d+) (\w+)\)", json_card['text'])
                if match:
                    add_uses(match.group(2), int(match.group(1)), db_asset_card, session)
    
    elif json_card['type_code'] == 'treachery':
        print(f"Creating new treachery: {json_card['name']}")
        db_treachery = Treacheries()
        db_treachery = set_attr(json_card, db_treachery, Treacheries, session)
        
        if "subtype_code" in json_card and json_card['subtype_code'] in ["weakness", "basicweakness"]:
            db_treachery.encounter_set = "investigator weakness"
            
        db_treachery.card = db_card
        session.add(db_treachery)
    
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
        
def connect_investigator_cards(session):
    new_investigators = session.scalars(select(Investigators))
    
    for investigator in new_investigators:
        # Search for the player_cards that match our deckbuilding_requirements and establishing a relationship
        # 1) Split deckbuilding_requirements
        required_card_names = investigator.deckbuilding_requirements_text.split(",")
        # 2) For each name
        for required_card_name in required_card_names:
            # 3) Find the matching card
            required_card_name = required_card_name.strip(" .")
            required_card_subname = None
            if '(' in required_card_name and ')' in required_card_name:
                parts = required_card_name.split('(')
                required_card_name = parts[0].strip()
                required_card_subname = parts[1].split(')')[0]
            
            if not required_card_name == "1 random basic weakness":
                required_card = find_card(required_card_name, session, required_card_subname)
                # Establish a relationship
                if required_card is not None:
                    investigator.required_player_cards.append(required_card.player_card)

        deckbuilding_options = investigator.deckbuilding_options_text.split(", ")
        for deckbuilding_option in deckbuilding_options:    
            db_deckbuilding_option = Deckbuilding_Options()  
            # Get the 'group' of cards (faction, trait, or uses)
            group_search = re.search(r'\[(.*?)\]|Neutral', deckbuilding_option)
            if group_search:                
                group = group_search.group(1) if group_search.group(1) else group_search.group().lower()

                faction_search = session.scalars(select(Factions).where(Factions.faction_name == group)).first()
                if faction_search:
                    db_deckbuilding_option.faction = faction_search

                ''' 
                trait_search = session.scalars(select(Traits).where(Traits.trait == group)).first()
                if trait_search:
                    db_deckbuilding_option.trait = trait_search
                
                use_search = session.scalars(select(Uses).where(Uses.type == group)).first()
                if use_search:
                    db_deckbuilding_option.uses = trait_search
                '''

            # Get the min/max XP
            xp_search = re.search(r'level\s*(\d+)-(\d+)', deckbuilding_option)
            if xp_search:
                db_deckbuilding_option.min_xp, db_deckbuilding_option.max_xp = xp_search.group(1), xp_search.group(2)
            
            # Make connections
            db_deckbuilding_option.investigator = investigator
            session.add(db_deckbuilding_option)

    session.commit()


def find_card(card_name, session, subname=None):
    if subname is not None:
        target = session.scalars(select(Cards)
            .where(Cards.name == card_name)
            .where(Cards.subname == subname)).first()
    else:
        target = session.scalars(select(Cards).where(Cards.name == card_name)).first()
    
    return target

        
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
def set_attr(json_card, db_card, table, session):
    # Get the table's attributes
    db_attributes = dir(table)
    db_attributes = [attr for attr in db_attributes if attr[0] != "_"]
    
    for db_attr in db_attributes:
        # If JSON attribute is different, translate
        json_attr = ATTRIBUTE_DB_TO_JSON.get(db_attr, db_attr)

        if json_attr in json_card and json_attr != "traits":
            setattr(db_card, db_attr, json_card[json_attr])
        
    if "faction_code" in json_card:
        db_card.faction = get_faction(faction_name=json_card['faction_code'], session=session)     
    
    if "pack_code" in json_card:
        db_card.cycle = get_cycle(cycle_code=json_card['pack_code'], session=session)
    
    print("New Card:", db_card, " with attributes ", db_attributes)
    return db_card    

def get_faction(session: Session, faction_name: str):
    try:
        # Query the Faction table to find a faction with the given name
        faction = session.query(Factions).filter(Factions.faction_name == faction_name).one()
        return faction
    except NoResultFound:
        # If no matching faction is found, handle the exception as needed
        print(f"Faction with name '{faction_name}' not found.")
        return None

def get_cycle(session: Session, cycle_code: str):
    try: 
        cycle = session.query(Cycle).filter(Cycle.code == cycle_code).one()
        return cycle
    except NoResultFound:
        # If no matching faction is found, handle the exception as needed
        print(f"Cycle with code '{cycle_code}' not found.")
        return None

def add_factions(session):
    for faction in ["guardian", "seeker", "rogue", "survivor", "mystic", "neutral", "mythos"]:
        new_faction = Factions(faction_name = faction)
        session.add(new_faction)
    
    session.commit()

def add_cycles(session):
    with open("cycles.json") as file:
        data = json.load(file)
        for cycle in data:
            new_cycle = Cycle( code = cycle['code'], name = cycle['name'])
            session.add(new_cycle)
    
    session.commit()

ATTRIBUTE_DB_TO_JSON = {
    'card_pack' : 'pack_name',
    'collector_number' : 'position',
    'artist' : 'illustrator',
    'nickname' : 'subname',
    'willpower' : 'skill_willpower',
    'intellect' : 'skill_intellect',
    'combat' : 'skill_combat',
    'agility' : 'skill_agility',
    'flavor_back' : 'back_flavor',
    'flavor_text' : 'flavor',
    'type' : 'type_code',
    'resource_cost' : 'cost',
    'card_text' : 'text',
    'card_text_back' : 'back_text',
    'encounter_set' : 'encounter_name',
    'image_url' : 'imagesrc'
}


if __name__ == "__main__":
    filename = sys.argv[1]
    # If we include any non-zero integer as a debug-flag, run in echo mode
    debug = False
    try: 
        debug_flag = sys.argv[2]
        if debug_flag:
            debug = True
        print("Starting with echo")
    except: 
        print("Starting without echo")
    convert_bulk_json(filename, debug)