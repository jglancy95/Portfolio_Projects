"""Contains additional checks and decorators (i.e. is user logged in, login decorator)"""

from cs50 import SQL
from flask import request, session, flash

# Configure CS50 Library to use SQLite database (for login checks)
db = SQL("sqlite:///pet_food_calculator.db")

def login_check_for_species():
    """Checks if user is logged in, then assigns species"""
    # Conditional rewrite suggested by CoPilot 
    
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        species_result = db.execute(
            "SELECT species FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if species_result:
            species = species_result[0]["species"]
            print(species)
        else:
            species = session["species"]
            print(f"Non-db species: {species}") 
            
    else:
        # If a user isn't logged in, grab species variable
        species = session["species"]
        
        if species == None:
            species = request.args.get("species")
        print(f"Non-db species: {species}") 
    
    # Return whatever species variable ends up being found 
    return species   

def der_factor():
    """Finds the latest der_factor set, if applicable"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        pet_info = db.execute(
            "SELECT species, canine_der_factor_id, feline_der_factor_id FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if pet_info:
            species = pet_info[0]["species"]
            if species == "Canine":
                der_factor_id = pet_info[0]['canine_der_factor_id']
            elif species == "Feline":
                der_factor_id = pet_info[0]['feline_der_factor_id']
                
            print(f"species: {species}, der_factor_id: {der_factor_id}")
        else:
            species = session["species"]
            der_factor_id = session["der_factor_id"]
            print(f"Non-db species: {species}, der_factor_id: {der_factor_id}") 
            
    else:
        # If a user isn't logged in, grab  variable
        der_factor_id = session["der_factor_id"]
    
    # Return whatever DER factor id variable ends up being found 
    return der_factor_id  

def check_if_pregnant():
    """Checks if the pet is pregnant"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        pregnancy_result = db.execute(
            "SELECT is_pregnant FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if pregnancy_result:
            is_pregnant = pregnancy_result[0]['is_pregnant']
            print(is_pregnant)
        else:
            is_pregnant = session["pregnancy_status"]
            print(f"Non-db pregnancy status: {is_pregnant}") 
            
    else:
        # If a user isn't logged in, grab session variable
        is_pregnant = session["pregnancy_status"]
        
        print(f"Non-db pregnancy status: {is_pregnant}") 
    
    # Return whatever pregnancy variable ends up being found 
    return is_pregnant  

def check_if_nursing():
    """Checks if the pet is pregnant"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        nursing_result = db.execute(
            "SELECT is_nursing FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if nursing_result:
            is_nursing = nursing_result[0]['is_nursing']
            print(is_nursing)
        else:
            is_nursing = session["lactation_status"]
            print(f"Non-db nursing status: {is_nursing}") 
            
    else:
        # If a user isn't logged in, grab session variable
        is_nursing = session["lactation_status"]
        
        print(f"Non-db nursing status: {is_nursing}") 
    
    # Return whatever nursing status variable ends up being found 
    return is_nursing  


def check_litter_size():
    """Checks if the pet is pregnant"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        litter_result = db.execute(
            "SELECT litter_size FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if litter_result:
            litter_size = litter_result[0]["litter_size"]
            print(litter_size)
        else:
            litter_size = session["litter_size"]
            print(f"Non-db litter size: {litter_size}") 
            
    else:
        # If a user isn't logged in, grab session variable
        is_pregnant = session["litter_size"]
        
        print(f"Non-db litter size: {litter_size}") 
    
    # Return whatever litter size variable ends up being found 
    return litter_size  

def find_repro_status():
    """Returns the reproductive status of the pet"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        species_result = db.execute(
            "SELECT sex FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if species_result:
            pet_sex = species_result[0]["sex"]
            print(pet_sex)
        else:
            pet_sex = session["pet_sex"]
            print(f"Non-db repro status: {pet_sex}") 
            
    else:
        # If a user isn't logged in, grab session variable
        pet_sex = session["pet_sex"]
        
        print(f"Non-db repro status: {pet_sex}") 
    
    # Return whatever reproductive status variable ends up being found 
    return pet_sex    

def calculcate_rer():
    """Calculates the minimum number of calories a pet needs at rest per day"""
    if session["user_id"] != None:
        # If the user is logged in, verify table variables 
        pet_info = db.execute(
            "SELECT weight, units FROM pets WHERE owner_id = ? AND name = ?", 
            session["user_id"], session["pet_name"]
        )
            
        print(pet_info)
            
        weight = pet_info[0]["weight"]
        units = pet_info[0]["units"]
    else:
        # If a user isn't logged in, grab session variables
        weight = session["weight"]
        units = session["units"]
        
    print(weight, units)
        
    # Convert lbs weighs to kgs
    if units == "lbs":
        weight = weight / 2.2
        units = "kgs"
        
    print(weight, units)
        
    rer = 0
    # If pet weighs more than 2kg and less than 45kg, use 30 × (BW kg) + 70 = RER
    if weight >= 2 and weight < 45:
        rer = round((30 * weight) + 70, 2)
            
    # If pet weighs less than 2kg or more than 45kg, use 70 × (BW kg)^0.75 = RER
    if weight < 2 or weight >= 45:
        rer = round(70 * weight**0.75, 2)
            
    print(rer) 
    session["rer"] = rer
     
    return rer

def find_breed_id():
    """Returns the breed of the pet"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        species = login_check_for_species()
        
        breed_result = db.execute(
            "SELECT canine_breed_id, feline_breed_id FROM pets WHERE owner_id = ? AND name = ?",
            session["user_id"], session["pet_name"]
        )
        

        if breed_result:
            if species == "Canine":
                breed_id = breed_result[0]["canine_breed_id"]
            if species == "Feline":
                breed_id = breed_result[0]["feline_breed_id"]

            print(breed_id)
   
    else:
        # If a user isn't logged in, grab breed ID variable
        breed_id = session["breed_id"]
        
        print(f"Non-db breed ID: {breed_id}") 
    
    # Return whatever breed ID variable ends up being found 
    return breed_id 

def convert_decimal_to_volumetric(partial_amount):
    """Convert partial volume amount from decimal to cups"""
    
    # Volume table source: https://amazingribs.com/more-technique-and-science/more-cooking-science/important-weights-measures-conversion-tables/
    
    partial_volumetric = ""
    if partial_amount > "0" and partial_amount <= "03":
        partial_volumetric = "1/2 tablespoon"
    elif partial_amount > "03" and partial_amount <= "06":
        partial_volumetric = "1/16"
    elif partial_amount > "06" and partial_amount <= "13":
        partial_volumetric = "1/8"
    elif partial_amount > "13" and partial_amount <= "25":
        partial_volumetric = "1/4"
    elif partial_amount > "25" and partial_amount <= "40":
        partial_volumetric = "1/3"
    elif partial_amount > "40" and partial_amount <= "55":
        partial_volumetric = "1/2"
    elif partial_amount > "55" and partial_amount <= "67":
        partial_volumetric = "2/3"
    elif partial_amount > "67" and partial_amount <= "85":
        partial_volumetric = "3/4"
    else:
        # If partial volume is more than 0.86 cups, add to whole volume
        partial_volumetric = "1"
        
    return partial_volumetric

def find_food_form():
    """Find the form of the pet's current diet"""
    
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        food_result = db.execute(
            "SELECT current_food_form FROM pets WHERE owner_id = ? AND name = ?", 
            session["user_id"], session["pet_name"]
        )
        

        if food_result:
            current_food_form = food_result[0]['current_food_form']
            print(current_food_form)
        else:
            current_food_form = session["current_food_form"]
            print(f"Non-db current_food_form: {current_food_form}") 
            
    else:
        # If a user isn't logged in, grab food form variable
        current_food_form = session["current_food_form"]
        
        print(f"Non-db current_food_form: {current_food_form}")
    
    # Return whatever form variable ends up being found 
    return current_food_form 

def pet_data_dictionary():
        # Use login check from helpers.py to verify species
    species = login_check_for_species()
    
    # If user is logged in, use SQL query
    if session["user_id"] != None:
        pet_data = db.execute(
            "SELECT * FROM pets WHERE owner_id = :user_id AND name = :pet_name",
            user_id=session["user_id"], pet_name=session["pet_name"]
        )       
            
        print(pet_data)
        
    # Otherwise, pass session variables
    else:
        pet_data = [{'name': session["pet_name"],
                     'age_in_years': session["pet_age_years"],
                     'age_in_months': session["age_in_months"],
                     'species': session["species"],
                     'breed': session["breed"],
                     'sex': session["pet_sex"],
                     'bcs': session["bcs"],
                     'weight': session["weight"],
                     'units': session["units"],
                     'activity_level': session["activity_level"],
                     'rer': session["rer"],
                     'der': session["der"],
                     'der_modifier': session["der_modifier"],
                     'current_food_amt_rec': session["daily_amount_to_feed_cur_food"],
                     'current_food_kcal': session["current_food_kcal"],
                     'current_food_form': session["current_food_form"],
                     'meals_per_day': session["meals_per_day"],
                     'is_pregnant': None,
                     'weeks_gestating': None,
                     'is_nursing': None,
                     'litter_size': None,
                     'weeks_nursing': None}]
        
        if session["pregnancy_status"] != None:
            pet_data[0]['is_pregnant'] = session["pregnancy_status"]
        elif session["number_weeks_pregnant"] != None:
            pet_data[0]["weeks_gestating"] = session["number_weeks_pregnant"]
        elif session["lactation_status"] != None:
            pet_data[0]['is_nursing'] = session["lactation_status"]
        elif session['litter_size'] != None:
            pet_data[0]['litter_size'] = session['litter_size']
        elif session["duration_of_nursing"] != None:
            pet_data[0]['weeks_nursing'] = session["duration_of_nursing"]
            
    return pet_data

def check_obesity_risk():
    """Checks if a pet's breed has a predisposed risk to obesity"""
    
    # Use helpers.py to check for breed ID
    breed_id = find_breed_id()
    
    # Use login check from helpers.py to verify species
    species = login_check_for_species()
    
    if species == "Canine":
        # Check if pet breed is predisposed to obesity
            breed_obesity_data = db.execute(
                "SELECT ObeseProneBreed FROM dog_breeds WHERE BreedID = :breed_id",
                breed_id=breed_id
            )
            
            if breed_obesity_data:
                obese_prone_breed = breed_obesity_data[0]["ObeseProneBreed"]
                  
    elif species == "Feline":
        # Check if pet breed is predisposed to obesity
            breed_obesity_data = db.execute(
                "SELECT ObeseProneBreed FROM cat_breeds WHERE BreedID = :breed_id",
                breed_id=breed_id
            )
            
            if breed_obesity_data:
                obese_prone_breed = breed_obesity_data[0]["ObeseProneBreed"]
                
    return obese_prone_breed


def check_if_pediatric():
    """Checks if the pet is pediatric"""
    
    if session["user_id"] != None:
        # If user isn logged in, query the database
            
        try:
            check_peds_status = db.execute(
                "SELECT is_pediatric FROM pets WHERE name = :pet_name AND owner_id = :user_id",
                pet_name=session["pet_name"], user_id=session["user_id"]
            )
        except Exception as e:
            flash(f"Unable to find pediatric status, Exception: {e}")
        else:
            is_pediatric = check_peds_status[0]["is_pediatric"]
    else:
        # If the user isn't logged in, grab session variables
        is_pediatric = session["is_pediatric"]
            
    print(f"Is Pediatric? {is_pediatric}")
    
    return is_pediatric