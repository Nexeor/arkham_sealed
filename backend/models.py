from sqlalchemy import ForeignKey, Column, Table, create_engine
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship

Base = declarative_base() 

class Cycle(Base):
    __tablename__ = "cycle"
    id: Mapped[int] = mapped_column(primary_key = True)
    
    # Children: One to many
    # Each cycle (parent) has many cards (child)
    cycle_cards: Mapped[List['Cards']] = relationship(back_populates="cycle")
    
    # Traits
    code: Mapped[str]
    name: Mapped[str]
    
    def __repr__(self):
        # Create a list to hold the core information
        cycle_info = [
            f"Code: {self.code}",
            f"Name: '{self.name}'",
        ]
        
        # Join all the information together
        return f"Cycle({', '.join(cycle_info)})"

# Many-to-Many between cards and traits 
# A card can have many traits, and a single trait can be associated with many cards 
card_traits = Table(
    'card_traits', 
    Base.metadata,
    Column('card_id', ForeignKey("cards.id"), primary_key=True),
    Column('trait_id', ForeignKey("traits.id"), primary_key=True)
)

# Both investigator and player cards share some key traits
class Cards(Base):
    __tablename__ = "cards"

    # Children: One to One
    # Each card is either an investigator card, player card, or treachery card
    investigator: Mapped['Investigators'] = relationship(back_populates='card')
    player_card: Mapped['Player_Cards'] = relationship(back_populates='card')
    treachery: Mapped['Treacheries'] = relationship(back_populates="card")
    
    # Children: Many to Many (join table)
    traits: Mapped[List["Traits"]] = relationship(
        secondary=card_traits, back_populates="cards"
    )
    
    # Parents: Many to One
    # Any number of cards (child) can belong to a single set (parent)
    cycle_id: Mapped[int] = mapped_column(ForeignKey('cycle.id'))
    cycle: Mapped['Cycle'] = relationship(back_populates='cycle_cards')

    # Traits
    id : Mapped[int] = mapped_column(primary_key = True)
    type: Mapped[str] 
    name: Mapped[str]
    card_pack: Mapped[str]
    collector_number: Mapped[int]
    artist: Mapped[str]
    image_url: Mapped[str]
    
    # Optional Fields
    subname: Mapped[Optional[str]]
    flavor_text: Mapped[Optional[str]]
    
    def __repr__(self):
        # Create a list to hold the core information
        card_info = [
            f"ID: {self.id}",
            f"Type: {self.type}",
            f"Name: '{self.name}'",
            f"Subname: '{self.subname}'",
            f"Cycle: '{self.cycle}'",
            f"Card Pack: '{self.card_pack}'",
            f"Collector Number: {self.collector_number}",
            f"Artist: '{self.artist}'"
        ]
        
        # Join all the information together
        return f"Cards({', '.join(card_info)})"
    

# Traits only held by investigators
class Investigators(Base):
    __tablename__ = "investigator_cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Parents: One to One
    # Each investigator (child) belongs to a card (parent)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    card: Mapped['Cards'] = relationship(back_populates='investigator')
    # Each investigator (child) belongs to a faction (parent)
    faction_id: Mapped[int] = mapped_column(ForeignKey("factions.id"))
    faction: Mapped['Factions'] = relationship(back_populates='investigators')
    
    # Children: One to Many 
    # Each investigator (parent) can have many deckbuilding options (child)
    deckbuilding_options: Mapped[List['Deckbuilding_Options']] = relationship(back_populates="investigator")
    # Each investigator (parent) can have many required player_cards (child)
    required_player_cards: Mapped[List['Player_Cards']] = relationship(back_populates='investigator')
    
    # Children: One to One
    # Each investigator has a special weakness card
    weakness: Mapped['Treacheries'] = relationship(back_populates="investigator")
    
    # Mandatory Fields
    nickname: Mapped[str]
    card_text: Mapped[str]
    card_text_back: Mapped[str]
    elder_sign: Mapped[str]
    willpower: Mapped[int]
    intellect: Mapped[int]
    combat: Mapped[int]
    agility: Mapped[int]
    health: Mapped[int]
    sanity: Mapped[int]
    deck_size: Mapped[int]
    deckbuilding_options_text: Mapped[str]
    deckbuilding_requirements_text: Mapped[str]
    flavor_back: Mapped[str]
    


# Traits only held by player cards
class Player_Cards(Base):
    __tablename__ = "player_cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Parents: One to One
    # Each player card (child) belongs to a card (parent)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    card: Mapped['Cards'] = relationship(back_populates='player_card')

    # Parents: One to Many
    # Any number of player cards (child) may belong to an investigator (parent)
    investigator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("investigator_cards.id"))
    investigator: Mapped[Optional['Investigators']] = relationship(back_populates='required_player_cards')
    # Any number of player cards (child) may belong to a faction (parent)
    faction_id: Mapped[int] = mapped_column(ForeignKey('factions.id'))    
    faction: Mapped['Factions'] = relationship(back_populates='player_cards')
    
    # TODO: Add secondary join path for secondary faction

    # Children: One to One
    # Each player card (parent) may contain a single asset (child)
    asset: Mapped[Optional['Assets']] = relationship(back_populates='player_card')

    # Mandatory Traits
    xp_cost: Mapped[int] = mapped_column(default=0)
    skill_willpower: Mapped[int] = mapped_column(default=0)
    skill_intellect: Mapped[int] = mapped_column(default=0)
    skill_combat: Mapped[int] = mapped_column(default=0)
    skill_agility: Mapped[int] = mapped_column(default=0)
    skill_wild: Mapped[int] = mapped_column(default=0)
    is_weakness: Mapped[bool] = mapped_column(default=False)
    
    # Optional Fields
    resource_cost: Mapped[Optional[int]]
    text: Mapped[Optional[str]]

class Treacheries(Base):
    __tablename__ = "treacheries"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Parents: One to One
    # Each treachery (child) belongs to a single player card (parent)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    card: Mapped['Cards'] = relationship(back_populates="treachery")
    # Each treachery (child) may belong to an investigator (parent)
    investigator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("investigator_cards.id"))
    investigator: Mapped[Optional['Investigators']] = relationship(back_populates="weakness")
    
    # Mandatory Fields
    encounter_set: Mapped[str]
    card_text: Mapped[str]

class Assets(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(primary_key=True)

    # Parents: One to One
    # Each asset (child) belongs to a player card (parent)
    player_card_id: Mapped[int] = mapped_column(ForeignKey("player_cards.id"))
    player_card: Mapped['Player_Cards'] = relationship(back_populates="asset")
    
    # Associations
    uses: Mapped[List['Asset_Uses']] = relationship(back_populates="asset")
    
    # Optional Fields
    slot: Mapped[Optional[str]]
    health: Mapped[Optional[int]]
    sanity: Mapped[Optional[int]] 

class Asset_Uses(Base):
    __tablename__ = "asset_uses"
    
    # Relationships
    uses_id: Mapped[int] = mapped_column(ForeignKey("uses.id"), primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), primary_key=True)
    
    use: Mapped["Uses"] = relationship(back_populates="assets")
    asset: Mapped['Assets'] = relationship(back_populates="uses")
    
    num_uses: Mapped[int]

# Used to represent cards traits
class Traits(Base):
    __tablename__ = "traits"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships (Join table)
    cards: Mapped[List["Cards"]] = relationship(
        secondary=card_traits, back_populates="traits"
    )
    
    # Children: One to Many 
    # Each trait (parent) can have many deckbuilding options (child)
    deckbuilding_options: Mapped[List['Deckbuilding_Options']] = relationship(back_populates="trait")
    
    trait: Mapped[str] # = mapped_column(unique=True)

class Deckbuilding_Options(Base):
    __tablename__ = "deckbuilding_options"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Parents: One to Many
    # Any number of deckbuilding options (child) can belong to one investigator (parent)
    investigator_id: Mapped[int] = mapped_column(ForeignKey('investigator_cards.id'))
    investigator: Mapped['Investigators'] = relationship(back_populates='deckbuilding_options')
    # Any number of deckbuilding options (child) can belong to one faction
    faction_id: Mapped[Optional[int]] = mapped_column(ForeignKey("factions.id"))
    faction: Mapped[Optional['Factions']] = relationship(back_populates='deckbuilding_options')
    # Any number of deckbuilding options (child) can belong to one trait
    trait_id: Mapped[Optional[int]] = mapped_column(ForeignKey("traits.id"))
    trait: Mapped[Optional['Traits']] = relationship(back_populates='deckbuilding_options')
    # Any number of deckbuilding options (child) can belong to one use type
    uses_id: Mapped[Optional[int]] = mapped_column(ForeignKey("uses.id"))
    uses: Mapped[Optional['Uses']] = relationship(back_populates='deckbuilding_options')
    
    # Mandatory Fields
    min_xp: Mapped[int]
    max_xp: Mapped[int]
    # True if disallowing these cards (ex: no "fortune" cards, mark illegal as true)
    illegal: Mapped[bool] = mapped_column(default=0) 

    # Optional Fields
    max_num: Mapped[Optional[int]] 


class Factions(Base):
    __tablename__ = "factions"
    id: Mapped[int] = mapped_column(primary_key=True)
     
    # Children: One to Many
    # Each Faction (parent) may have any number of player/investigator/deckbuilding (child)
    player_cards: Mapped[List['Player_Cards']] = relationship(back_populates='faction')
    investigators: Mapped[List['Investigators']] = relationship(back_populates='faction')
    deckbuilding_options: Mapped[List['Deckbuilding_Options']] = relationship(back_populates='faction')

    # Mandatory Fields
    faction_name: Mapped[str]

class Uses(Base):
    __tablename__ = "uses"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Associations
    assets: Mapped[List[Asset_Uses]] = relationship(back_populates="use")
    
    # Children: One to Many 
    # Each investigator (parent) can have many deckbuilding options (child)
    deckbuilding_options: Mapped[List['Deckbuilding_Options']] = relationship(back_populates="uses")
    
    # Mandatory fields
    type: Mapped[str]
       
# Creates and returns an engine to interact with the database
def get_engine(rebuild, debug):
    engine = create_engine("sqlite:///example.db", echo=debug)
    
    if rebuild:
        Base.metadata.drop_all(bind=engine)   
     
    Base.metadata.create_all(bind=engine, checkfirst=True)

    return engine
    