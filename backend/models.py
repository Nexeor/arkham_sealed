from sqlalchemy import ForeignKey, create_engine
from typing import Optional, List
from sqlalchemy.orm import Mapped, Session, mapped_column, declarative_base, relationship

Base = declarative_base() 

# Both investigator and player cards share some key traits
class Cards(Base):
    __tablename__ = "cards"

    # Relationships (Children)
    investigators: Mapped[List["Investigators"]] = relationship()
    player_cards: Mapped[List["Player_Cards"]] = relationship()

    # Mandatory Traits
    id : Mapped[int] = mapped_column(primary_key = True)
    type: Mapped[str] 
    name: Mapped[str]
    cycle: Mapped[str]
    card_pack: Mapped[str]
    collector_number: Mapped[int]
    artist: Mapped[str]


# Traits only held by investigators
class Investigators(Base):
    __tablename__ = "investigator_cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships (Parents)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))

    # Relationships (Children)
    related_cards: Mapped[List["Cards"]] = relationship()
    
    # Mandatory Fields
    nickname: Mapped[str]
    card_text: Mapped[str]
    elder_sign: Mapped[str]
    willpower: Mapped[int]
    intellect: Mapped[int]
    combat: Mapped[int]
    agility: Mapped[int]
    health: Mapped[int]
    sanity: Mapped[int]
    flavor_back: Mapped[str]
    
    # Optional Fields
    flavor_front: Mapped[Optional[str]]

# Traits only held by player cards
class Player_Cards(Base):
    __tablename__ = "player_cards"
    id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships (Parents)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    investigator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("investigator_cards.id"))

    # Relationships (Children)
    assets: Mapped[List["Asset_Card"]] = relationship()
    events: Mapped[List["Event_Card"]] = relationship()
    skills: Mapped[List["Skill_Card"]] = relationship()

    # Mandatory Traits
    xp_cost: Mapped[int] = mapped_column(default=0)
    skill_willpower: Mapped[int] = mapped_column(default=0)
    skill_intellect: Mapped[int] = mapped_column(default=0)
    skill_combat: Mapped[int] = mapped_column(default=0)
    skill_agility: Mapped[int] = mapped_column(default=0)
    
    # Optional Fields
    text: Mapped[Optional[str]]
    flavor_text: Mapped[Optional[str]]

class Asset_Card(Base):
    __tablename__ = "asset_cards"
    id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships (Parents)
    player_card_id : Mapped[int] = mapped_column(ForeignKey("player_cards.id"))
    
    # Mandatory Fields
    resource_cost: Mapped[int]
    
    # Optional Fields
    slot: Mapped[Optional[str]]
    health: Mapped[Optional[int]]
    sanity: Mapped[Optional[int]] 

class Event_Card(Base):
    __tablename__ = "event_cards"
    id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships (Parents)
    player_card_id : Mapped[int] = mapped_column(ForeignKey("player_cards.id"))

    # Mandatory Fields
    resource_cost: Mapped[int]


class Skill_Card(Base):
    __tablename__ = "skill_cards"
    id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships (Parents)
    player_card_id : Mapped[int] = mapped_column(ForeignKey("player_cards.id"))


class Deckbuilding_Options(Base):
    __tablename__ = "deckbuilding_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    investigator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("investigator_cards.id"))
    # Must draw from a cardpool, either the faction, types of uses, or trait
    faction: Mapped[Optional[str]]
    trait: Mapped[Optional[str]]
    uses: Mapped[Optional[str]]
    min_xp: Mapped[int]
    max_xp: Mapped[int]
    max_num: Mapped[int]
    # Use this field to define a group of forbidden cards
    allowed: Mapped[bool]    


# Used to represent cards traits
class Card_Traits(Base):
    __tablename__ = "card_traits"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("player_cards.id"))
    trait: Mapped[str]


# Used to represent "uses" on cards (charges, supplies, ammo)
class Card_Uses(Base):
    __tablename__ = "card_uses"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("player_cards.id"))
    type: Mapped[str]
    num_uses: Mapped[int]   

# Creates and returns an engine to interact with the database
def get_engine(reset):
    engine = create_engine("sqlite:///example.db", echo=True)
    
    if reset: 
        Base.metadata.drop_all(bind=engine)
        
    Base.metadata.create_all(bind=engine, checkfirst=False)

    return engine
    