"""A Todo List website that helps the user keep track of tasks
they need to get done throughout the week"""

from clickable_calendar import ClickableHTMLCalendar
from datetime import date, datetime, time
from flask import Flask, flash, jsonify, redirect, \
    render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_login import current_user, login_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
from helpers import format_time, load_priorities, str_to_time, task_lookup
from task_tracking import db, Users, Tasks
import os
from werkzeug.exceptions import NotFound
from werkzeug.security import check_password_hash, generate_password_hash


# --------------------------- App Setup --------------------------- #

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

# Load in security key
API_KEY = os.environ.get("KEY")
app.config["SECRET_KEY"] = API_KEY

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Register the functions as filters for Jinja to use
app.jinja_env.filters['str_to_time'] = str_to_time
app.jinja_env.filters['format_time'] = format_time

# ---------------------- Configure Database ----------------------- #

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks_todo.db"
db.init_app(app)


with app.app_context():
    db.create_all()
    
# User loader function
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# -------------------------- App Routes --------------------------- #

@app.route("/", methods=["GET", "POST"])
def home():
    """Loads in the calendar for the current month"""
    
    c = ClickableHTMLCalendar()
    
    # Get the calendar for the current month
    today = date.today()
    
    try: 
        # Gets the user's current ID
        user_id = current_user.id
        
        # If a user has a preferred starting day of the week, set it
        c.set_user_first_weekday(user_id)
        
    except Exception as e:
        print(f"Can't set a custom first day of the week. Exception: {e}")
        print("Loading default calendar...")
    finally:
        print("Loading calendar...")
        try:
            print(f"Year: {today.year}, Month: {today.month}")
            calendar_html = c.formatmonth(today.year, today.month, withyear=True)
        except Exception as e:
            print(f"Error generating calendar HTML: {e}")
        calendar_html = c.formatmonth(today.year, today.month, withyear=True)
    

    return render_template("index.html", calendar=calendar_html, current_user=current_user)

@app.route("/day_view/<month>/<day>/<year>", methods=["GET", "POST"])
def day(month, day, year):
    """Loads in the view of the selected day"""
    
    try:
        
        # Check today's date
        today = date.today()
        
        # Pad the date with 0s if it's within the first 10 days of the month
        day_date = f"{year}-{int(month):02d}-{int(day):02d}"
        
        # Convert day_date string to a datetime object
        selected_date = datetime.strptime(day_date, "%Y-%m-%d").date()
        
        if selected_date == today:
            
            # If the selected date matches today's date, redirect to /today
            print("Today's date")
            return redirect(url_for("today", current_user=current_user))
        
        # Format the date to a string that represents the locale's appropriate date representation
        day_date_formatted = selected_date.strftime("%x")
        print(day_date_formatted)

    except Exception as e:
        flash(f"Can't find dates. Exception: {e}")
        day_date_formatted = None
        
    try:
        print(current_user.id)
        
        # Look for existing tasks in the database
        tasks = task_lookup(month, day, year)
        
        # Print detailed information about each task
        for task in tasks:
            print(f"Task ID: {task.task_id}")
            print(f"User ID: {task.user_id}")
            print(f"Task Name: {task.task_name}")
            print(f"Task Date: {task.task_date}")
            print(f"Task Time: {task.task_time}")
            print(f"Description: {task.description}")
            print(f"Priority Level: {task.priority_level}")
            print(f"Task Color: {task.task_color}")
            print("___________")
          
        # Load priority list
        priorities = load_priorities(month, day, year)  
        
    except Exception as e:
        flash(f"Can't load task list, exception {e}")

    return render_template("day.html", date=day_date_formatted,
                           day=day,
                           current_user=current_user,
                           tasks=tasks,
                           priorities=priorities,
                           api=API_KEY)
    
    
@app.route("/today", methods=["GET", "POST"])
def today():
    """Loads in the view of the current day"""
    
    tasks = []
    
    # Find today's date
    try:
        today_date = date.today()
        today_date_full = today_date.strftime("%x")
        
        today = "Today"
        print(f"Today's day: {today_date.day}")
        print(f"today's month: {today_date.month}")
    except Exception as e:
        flash(f"Can't find dates. Exception: {e}")
        today_date_full = None
    print(today_date_full)
    
    try:
                
        # Look for existing tasks in the database
        tasks = task_lookup(today_date.month, today_date.day, today_date.year)
    
        # Load priority list
        priorities = load_priorities(today_date.month, today_date.day, today_date.year)  
    
    except Exception as e:
        flash(f"Can't load task list, exception {e}")


    return render_template("day.html", date=today,
                           day=today_date.day,
                           current_user=current_user,
                           tasks=tasks,
                           priorities=priorities,
                           api=API_KEY)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs an existing user in"""
        
    # Checks if the user's data is validated 
    if request.method == "POST":

        # Check username and hashed password against the database
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            
            user_lookup = db.session.execute(db.select(Users).where(Users.username == username))
            user = user_lookup.scalar()
            
            if user == None:
                flash("Username not found.")
                return redirect(url_for('login'))
        
            # Ensure username exists and password is correct
            elif not check_password_hash(user.password, password):
                flash("Invalid password.")
                return redirect(url_for('login', current_user=current_user))
            
            else:
                flash(f"Logged in as {username}!")
                
                # Remember which user has logged in
                login_user(user)
                return redirect(url_for("home"))
        except Exception as e:
            flash(f"Can't log in. Exception: {e}")
            return redirect(url_for('login', current_user=current_user))
     
    return render_template("login.html", current_user=current_user)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registers a new user"""
    
    if request.method == "POST":
        
        try:
            # Check user against info in the database
            find_user = db.session.execute(db.select(Users).where(Users.username == request.form.get("username")))
            user = find_user.scalar()
            
            print(f"User: {user}")
            # Check if username exists already in the database
            if user is not None:
                flash("That username already taken.")
                return redirect(url_for("register", current_user=current_user))
            # Check if the user's password matches the password verification
            elif request.form.get("password") != request.form.get("confirm_password"):
                flash("Passwords must match.")
                return redirect(url_for("register", current_user=current_user))

            # If all checks pass, hash password
            hashed_password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        except Exception as e:
            flash(f"Can't register new user, exception: {e}")
            return redirect(url_for("register", current_user=current_user))
        else:
            # Insert data if all checks pass
            try:
                print(f"Username: {request.form.get("username")}", f"Password: {hashed_password}")
                # Insert new info into database
                add_user = Users(
                    username=request.form.get("username"),
                    password=hashed_password
                )
                
                db.session.add(add_user)
                db.session.commit()  
                
                # Remember which user has logged in
                login_user(add_user)
                                    
                # Upon registering, redirect the user to the calendar settings page
                return redirect(url_for("preferences", current_user=current_user, user_id=add_user.id))
        
            except Exception as e:    
                flash(f"Can't insert new user into database, exception: {e}")
                return redirect(url_for("register", current_user=current_user))
                

    return render_template("register.html", current_user=current_user)


@app.route("/logout")
def logout():
    """Logs user out"""
    
    # Clears the user_id
    session.clear()
    
    # Redirect to home
    return redirect(url_for("home", current_user=current_user))


@app.route("/preferences/<int:user_id>", methods=["GET", "POST"])
def preferences(user_id):
    """Set week view preferences"""
    
    if request.method == "POST":
        starting_day = request.form.get("start_day")
        
        print(f"Starting day: {starting_day}")
        try:
            # Find user in the database
            found_user = Users.query.get(user_id)
            
            if found_user:
                # Update preferred starting day
                found_user.pref_starting_day = starting_day
                
                # Update the database
                db.session.commit()
            
                print("Preferred starting day updated")
            else:
                flash("User not found")
                
            return redirect(url_for("home", current_user=current_user))
        except Exception as e:
            # Revert if there is an error
            db.session.rollback()
            flash(f"Can't update starting day, exception: {e}")
        
    return render_template("user_preferences.html", current_user=current_user)

@app.route("/new_task", methods=["GET", "POST"])
def add_task():
    """Allows the user to add a new task to the calendar"""
    
    if request.method == "POST":
        task = request.form.get("task_name")
        task_date = request.form.get("task_date")
        task_time = request.form.get("time")
        description = request.form.get("task_description")
        priority = request.form.get("priority_level")
        color = request.form.get("task_color")
        print(color, task, description, task_date, task_time, priority)
        
        time = datetime.strptime(task_time, "%H:%M").strftime("%I:%M %p")
        print(time)
        
        try:
            
            add_task = Tasks(
                user_id=current_user.id,
                task_name=task,
                task_date=task_date,
                task_time=time,
                description=description,
                priority_level=priority,
                task_color=color
            )
                
            db.session.add(add_task)
            db.session.commit()  
            
            return redirect(url_for("home", current_user=current_user))
        except Exception as e:
            
            flash(f"Unable to add task, exception: {e}")
            return redirect(url_for("add_task", current_user=current_user))
                
    return render_template("add_task.html", current_user=current_user)


@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    """Allows a user to edit their tasks"""
    
    if request.method == "POST":
        print("POSTING!")
        
        task_name = request.form.get("task_name")
        task_description = request.form.get("task_description")
        task_color = request.form.get("task_color")
        task_date = request.form.get("task_date")
        time = request.form.get("time")
        priority_level = request.form.get("priority_level")
        
        try:   
            # Look up task by ID for modification
            task_to_edit_found = db.session.query(Tasks).filter_by(task_id=task_id).first()
            
            if task_to_edit_found:
                # Update information
                task_to_edit_found.task_name = task_name
                task_to_edit_found.description = task_description
                task_to_edit_found.task_color = task_color
                task_to_edit_found.task_date = task_date
                task_to_edit_found.task_time = time
                task_to_edit_found.priority_level = priority_level
                
                # Commit changes
                db.session.commit()
                return redirect(url_for("home"))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Unable to edit task. Excepiton: {e}")
        
    try:
        task_query = db.session.execute(
            db.select(Tasks).where(Tasks.task_id == task_id)
            )
        task = task_query.scalars().first()
        
        if task.task_time:
            # Convert time back to 24 hour format
            task_24hr = datetime.strptime(task.task_time, "%I:%M %p").strftime("%H:%M")
            task_time = task_24hr
            
        return render_template("edit.html", task=task, task_time=task_time)
    
    except Exception as e:
        flash(f"Can't find task. Exception: {e}")
        
    return render_template("edit.html")


@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """Deletes the task that matches the ID"""
    
    if request.form.get("method") == "DELETE" and request.form.get("api_key") == API_KEY:
        try:
            task = db.get_or_404(Tasks, task_id)
            
            # Mark task for deletion if found
            db.session.delete(task)
                
            # Commit changes
            db.session.commit()
            print("Successfully deleted from the database!")
            return redirect(url_for("home"))
        except NotFound:
            return jsonify(error={"Not Found": "Sorry, a task with that id was not found in the database"}), 404
    else:
        return jsonify(error={"Not Found": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
    