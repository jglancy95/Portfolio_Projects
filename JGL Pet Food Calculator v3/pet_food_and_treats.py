"""Imports pet_foods_and-treats.db and allows queries"""

from sqlalchemy import create_engine, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Define database URI
PET_FOODS_AND_TREATS_URI = "sqlite:///pet_foods_and_treats.db"

# Create engine for the database
pet_food_treat_engine = create_engine(PET_FOODS_AND_TREATS_URI)

# Create session for the database
PetFoodSession = sessionmaker(bind=pet_food_treat_engine)
PET_FOOD_SESSION = PetFoodSession()

class Base(DeclarativeBase):
    pass

# Define modules that map to the tables in the existing database
class AAFCOStatements(Base):
    __tablename__ = "AAFCOStatements"
    statement_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    aafco_statement = Column(String, unique=True)
    
class FoodForms(Base):
    __tablename__ = "FoodForms"
    form_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    food_form = Column(String, unique=True)
    
class LifeStages(Base):
    __tablename__ = "LifeStages"
    life_stage_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    life_stage = Column(String, unique=True)
    
class PackageSizes(Base):
    __tablename__ = "PackageSizes"
    size_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    package_size = Column(String, unique=True)
    
class ProteinSources(Base):
    __tablename__ = "ProteinSources"
    protein_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    protein_source = Column(String, unique=True)
    protein_type = Column(String)
    
    def __repr__(self):
        return f"<ProteinSources(protein_id={self.protein_id}, protein_source='{self.protein_source}', protein_type='{self.protein_type}')>"

class PetFoods(Base):
    __tablename__ = "PetFoods"
    food_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    food_name = Column(String, unique=True)
    food_form = Column(String, ForeignKey("FoodForms.form_id"))
    life_stage = Column(String, ForeignKey("LifeStages.life_stage_id"))
    description = Column(String)
    size = Column(String, ForeignKey("PackageSizes.size_id"))
    aafco_statement = Column(Integer, ForeignKey("AAFCOStatements.statement_id"))
    kcal_per_kg = Column(Integer)
    kcal_per_cup_can_pouch = Column(Integer)
    first_protein_source = Column(Integer, ForeignKey("ProteinSources.protein_id"))
    second_protein_source = Column(Integer, ForeignKey("ProteinSources.protein_id"))
    third_protein_source = Column(Integer, ForeignKey("ProteinSources.protein_id"))
    ingredient_list = Column(String)
    date_added = Column(DateTime)
    date_updated = Column(DateTime)