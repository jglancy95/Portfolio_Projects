"""An online shop using Flask and Python"""

from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

# Load in security key
KEY = os.environ.get("security_key")


def current_year():
    """Returns the current year"""
    
    # Convert current date to a string
    jgl_date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    # Grab only the year
    jgl_current_year = jgl_date_str[:4]
    
    return jgl_current_year

def social_links():
    """Returns the social media links"""
    
    github = os.environ.get("github")
    linkedin = os.environ.get("linkedin")
    discord = os.environ.get("discord")
    fiverr = os.environ.get("fiverr")
    email = os.environ.get("email")
    youtube = os.environ.get("youtube")
    
    socials = {
        "github_link": github,
        "linkedin_link": linkedin,
        "discord_link": discord,
        "fiverr_link": fiverr,
        "email_address": email,
        "youtube_link": youtube
        }
    
    return socials

JGL_CURRENT_YEAR = current_year()
JGL_SOCIALS = social_links()

@app.route("/", methods=["GET", "POST"])
def home():
    """Shows homepage with a current copyright date"""
    

    
    return render_template("index.html",
                           date=JGL_CURRENT_YEAR,
                           socials=JGL_SOCIALS)

@app.route("/products", methods=["GET", "POST"])
def products():
    """Showcases a list of products to buy"""
    
    return render_template("products.html", 
                           date=JGL_CURRENT_YEAR,
                           socials=JGL_SOCIALS)

@app.route("/products/<int:product_id>", methods=["GET", "POST"])
def for_sale_info():
    """Provides more info on each product"""
    
    return render_template("product_page.html",
                           date=JGL_CURRENT_YEAR,
                           socials=JGL_SOCIALS)