from sqlalchemy import ForeignKey, Column, Table, create_engine
from typing import Optional, List
from sqlalchemy.orm import Mapped, Session, mapped_column, declarative_base, relationship

Base = declarative_base() 

# Join cards with their traits
card_traits = Table(
    'card_traits', 
    Base.metadata,
    Column('card_id', ForeignKey("cards.id"), primary_key=True),
    Column('trait_id', ForeignKey("traits.id"), primary_key=True)
)

class Asset_Uses(Base):
    __tablename__ = "asset_uses"
    
    # Relationships
    uses_id: Mapped[int] = mapped_column(ForeignKey("uses.id"), primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), primary_key=True)
    
    use: Mapped["Uses"] = relationship(back_populates="assets")
    asset: Mapped["Assets"] = relationship(back_populates="uses")
    
    num_uses: Mapped[int]
    
# Both investigator and player cards share some key traits
class Cards(Base):
    __tablename__ = "cards"

    # Relationships (Children)
    investigators: Mapped[List["Investigators"]] = relationship()
    player_cards: Mapped[List["Player_Cards"]] = relationship()
    
    # Relationship (Join Table)
    traits: Mapped[List["Traits"]] = relationship(
        secondary=card_traits, back_populates="cards"
    )

    # Mandatory Traits
    id : Mapped[int] = mapped_column(primary_key = True)
    type: Mapped[str] 
    name: Mapped[str]
    cycle: Mapped[str]
    card_pack: Mapped[str]
    collector_number: Mapped[int]
    artist: Mapped[str]

# Used to represent cards traits
class Traits(Base):
    __tablename__ = "traits"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Relationships (Join table)
    cards: Mapped[List["Cards"]] = relationship(
        secondary=card_traits, back_populates="traits"
    )
    
    trait: Mapped[str] # = mapped_column(unique=True)

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
    assets: Mapped[List["Assets"]] = relationship()

    # Mandatory Traits
    xp_cost: Mapped[int] = mapped_column(default=0)
    skill_willpower: Mapped[int] = mapped_column(default=0)
    skill_intellect: Mapped[int] = mapped_column(default=0)
    skill_combat: Mapped[int] = mapped_column(default=0)
    skill_agility: Mapped[int] = mapped_column(default=0)
    skill_wild: Mapped[int] = mapped_column(default=0)
    
    # Optional Fields
    is_weakness: Mapped[Optional[bool]]
    resource_cost: Mapped[Optional[int]]
    text: Mapped[Optional[str]]
    flavor_text: Mapped[Optional[str]]
    

class Assets(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(primary_key=True)

    # Parents
    player_card_id : Mapped[int] = mapped_column(ForeignKey("player_cards.id"))
    
    # Associations
    uses: Mapped[List[Asset_Uses]] = relationship(back_populates="asset")
    
    # Optional Fields
    slot: Mapped[Optional[str]]
    health: Mapped[Optional[int]]
    sanity: Mapped[Optional[int]] 

class Uses(Base):
    __tablename__ = "uses"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Associations
    assets: Mapped[List[Asset_Uses]] = relationship(back_populates="use")
    
    # Mandatory fields
    type: Mapped[str]
       
# Creates and returns an engine to interact with the database
def get_engine(reset):
    engine = create_engine("sqlite:///example.db")
    
    if reset:
        Base.metadata.drop_all(bind=engine)   
     
    Base.metadata.create_all(bind=engine, checkfirst=True)

    return engine
    