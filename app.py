import os

import csv

import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from icecream import ic

from helpers import apology, login_required, lookup, usd
from datetime import datetime
import pytz

eastern_australia_tz = pytz.timezone('Australia/Sydney')
current_time = datetime.now(eastern_australia_tz)
# Configure application
app = Flask(__name__)

db = SQL("sqlite:///final.db")
RESULTS = {}

DOOR_FAULTS = db.execute("SELECT * FROM doorfixes")
LIGHT_FAULTS = db.execute("SELECT * FROM em_lightfixes")
FIREEX_FAULTS = db.execute("SELECT * FROM fireExfixes")
# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# Need to set up some other databases for the assests and the results of the inspections
db = SQL("sqlite:///final.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():


    return render_template("index.html")


#This is the register section from the CS50 project that I have used to register for fire inspection.
# The building that is being inspected is "registered" to a username to be able to keep it seperate from other buildings
# and to still be able to register other building that are saved to the same database.


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user _id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username does not already exist
        if len(rows) != 0:
            return apology("username already exists", 400)

        #Insert new user into database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                   request.form.get("username"), generate_password_hash(request.form.get("password")))

        # Query database for newly inserted user
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a line or via redirect)
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Remember the username
        session["username"] = request.form.get("username")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

    # Redirect user to login form
    return redirect("/")


# The doors function has been completed and works as expected. The other functions such as emergency lighting have
# yet to be completed. Tables of inspection criteria need to be produced. The results can still be put into the
# results table and will thus be seen in the final report.
@app.route("/doors", methods=["POST", "GET"])
def doors():
    door = request.form.get("door")
    door_fault = request.form.get("door_fault")
    comment = request.form.get("comment")
    #image_url = request.form.get("imageUrl").split(',')
    print(request.form)  # Logs the form data sent in the request
    print(door)  # Logs the door location
    #print(image_urls)  # Logs the list of image URLs
    fault = ''
    remedy = ''
    asset = door
    if request.method == "POST":
        RESULTS[door] = door_fault
        ic(door_fault)
        ic(type(door_fault))
        fault = ''
        remedy = ''
        faultDict = ()
        faultStr = {}

        remedyDict = ()
        remedyStr = {}

        # This is working as expected but I have kept the ic views which helped to solve the problem of getting
        # the strings for the faults and the remedies out of the selection results.
        fault=db.execute("SELECT fault FROM doorfixes WHERE fault_id = :door_fault",
                    door_fault=door_fault)
        remedy=db.execute("SELECT remedy FROM doorfixes WHERE fault_id = :door_fault",
                    door_fault=door_fault)
        ic(remedy)
        faultDict   = fault [0]
        faultStr = faultDict  ['fault']

        remedyDict = remedy [0]
        remedyStr= remedyDict  ['remedy']

        # The strings were saved into these variables to build the results table below. I have left some of the
        # "debugging tools" that I used to see what was being passed around.
        remedy = remedyStr
        fault = faultStr


        print(fault)
        print(remedy)

        ic(fault)
        ic(remedy)
        ic(type(fault))
        ic(type(remedy))

        from datetime import datetime

        # Insert a row into the results table
        db.execute("INSERT INTO results (user_id, asset, fault_id, fault, remedy, comment, timestamp) VALUES (:user_id, :asset, :fault_id, :fault, :remedy, :comment, :timestamp)",
                user_id=session["user_id"], asset=asset, fault_id=door_fault, fault=fault, remedy=remedy, comment=comment, timestamp=datetime.now(eastern_australia_tz))

        # Get the ID of the last inserted row
        result_id = db.execute("SELECT last_insert_rowid()")[0]["last_insert_rowid()"]

        # Get the imageUrl string from the form and split it into a list of URLs
        image_urls = request.form.get("imageUrl").split(';')

        print(f"result_id: {result_id}")  # Log the value of result_id
        print(f"image_urls: {image_urls}")  # Log the value of image_urls

        for image_url in image_urls:
            print(f"image_url: {image_url}")  # Log the value of image_url
            try:
                print("Inside the try block")  # Log a message
                db.execute("INSERT INTO images (result_id, image_url) VALUES (:result_id, :image_url)",
                        result_id=result_id, image_url=image_url)
            except Exception as e:
                print(f"An error occurred while inserting into the images table: {e}")

        return redirect("/results")
        
    else:
        return render_template("doors.html",  door_faults=DOOR_FAULTS)

# These following functions could be completed as per the doors method above, however, since hearing about OOP
# it maybe better to write app.py having classes producing the objects.
@app.route("/em_lights", methods=["POST", "GET"])
def em_lights():
    light = request.form.get("light")
    light_fault = request.form.get("light_fault")
    comment = request.form.get("comment")
    #image_url = request.form.get("imageUrl").split(',')
    print(request.form)  # Logs the form data sent in the request
    print(light)  # Logs the light location
    #print(image_urls)  # Logs the list of image URLs
    fault = ''
    remedy = ''
    asset = light
    if request.method == "POST":
        RESULTS[light] = light_fault
        ic(light_fault)
        ic(type(light_fault))
        fault = ''
        remedy = ''
        faultDict = ()
        faultStr = {}

        remedyDict = ()
        remedyStr = {}

        # This is working as expected but I have kept the ic views which helped to solve the problem of getting
        # the strings for the faults and the remedies out of the selection results.
        fault=db.execute("SELECT fault FROM em_lightfixes WHERE fault_id = :light_fault",
                    light_fault=light_fault)
        remedy=db.execute("SELECT remedy FROM em_lightfixes WHERE fault_id = :light_fault",
                    light_fault=light_fault)
        ic(remedy)
        faultDict   = fault [0]
        #print(faultDict)
        faultStr = faultDict  ['fault']

        remedyDict = remedy [0]
        remedyStr= remedyDict  ['remedy']

        # The strings were saved into these variables to build the results table below. I have left some of the
        # "debugging tools" that I used to see what was being passed around.
        remedy = remedyStr
        fault = faultStr


        print(fault)
        print(remedy)

        ic(fault)
        ic(remedy)
        ic(type(fault))
        ic(type(remedy))

        from datetime import datetime

        # Insert a row into the results table
        db.execute("INSERT INTO results (user_id, asset, fault_id, fault, remedy, comment, timestamp) VALUES (:user_id, :asset, :fault_id, :fault, :remedy, :comment, :timestamp)",
                user_id=session["user_id"], asset=asset, fault_id=light_fault, fault=fault, remedy=remedy, comment=comment, timestamp=datetime.now(eastern_australia_tz))

        # Get the ID of the last inserted row
        result_id = db.execute("SELECT last_insert_rowid()")[0]["last_insert_rowid()"]

        # Get the imageUrl string from the form and split it into a list of URLs
        image_urls = request.form.get("imageUrl").split(';')

        print(f"result_id: {result_id}")  # Log the value of result_id
        print(f"image_urls: {image_urls}")  # Log the value of image_urls

        for image_url in image_urls:
            print(f"image_url: {image_url}")  # Log the value of image_url
            try:
                print("Inside the try block")  # Log a message
                db.execute("INSERT INTO images (result_id, image_url) VALUES (:result_id, :image_url)",
                        result_id=result_id, image_url=image_url)
            except Exception as e:
                print(f"An error occurred while inserting into the images table: {e}")

        return redirect("/results")
        
    else:
        return render_template("em_lights.html",  light_faults=LIGHT_FAULTS)


# These following functions could be completed as per the doors method above, however, since hearing about OOP
# it maybe better to write app.py having classes producing the objects.


@app.route("/fire_ext", methods=["POST", "GET"])
def fire_ext():
    fireEx = request.form.get("fireEx")
    fireEx_fault = request.form.get("fireEx_fault")
    comment = request.form.get("comment")
    #image_url = request.form.get("imageUrl").split(',')
    print(request.form)  # Logs the form data sent in the request
    print(fireEx)  # Logs the fireEx location
    #print(image_urls)  # Logs the list of image URLs
    fault = ''
    remedy = ''
    asset = fireEx 
    if request.method == "POST":
        RESULTS[fireEx] = fireEx_fault
        ic(fireEx_fault)
        ic(type(fireEx_fault))
        fault = ''
        remedy = ''
        faultDict = ()
        faultStr = {}

        remedyDict = ()
        remedyStr = {}

        # This is working as expected but I have kept the ic views which helped to solve the problem of getting
        # the strings for the faults and the remedies out of the selection results.
        fault=db.execute("SELECT fault FROM fireEXfixes WHERE fault_id = :fireEx_fault",
                    fireEx_fault=fireEx_fault)
        remedy=db.execute("SELECT remedy FROM fireEXfixes WHERE fault_id = :fireEx_fault",
                    fireEx_fault=fireEx_fault)
        ic(remedy)
        faultDict   = fault [0]
        faultStr = faultDict  ['fault']

        remedyDict = remedy [0]
        remedyStr= remedyDict  ['remedy']

        # The strings were saved into these variables to build the results table below. I have left some of the
        # "debugging tools" that I used to see what was being passed around.
        remedy = remedyStr
        fault = faultStr


        print(fault)
        print(remedy)

        ic(fault)
        ic(remedy)
        ic(type(fault))
        ic(type(remedy))

        from datetime import datetime

        # Insert a row into the results table
        db.execute("INSERT INTO results (user_id, asset, fault_id, fault, remedy, comment, timestamp) VALUES (:user_id, :asset, :fault_id, :fault, :remedy, :comment, :timestamp)",
                user_id=session["user_id"], asset=asset, fault_id=fireEx_fault, fault=fault, remedy=remedy, comment=comment, timestamp=datetime.now(eastern_australia_tz))

        # Get the ID of the last inserted row
        result_id = db.execute("SELECT last_insert_rowid()")[0]["last_insert_rowid()"]

        # Get the imageUrl string from the form and split it into a list of URLs
        image_urls = request.form.get("imageUrl").split(';')

        print(f"result_id: {result_id}")  # Log the value of result_id
        print(f"image_urls: {image_urls}")  # Log the value of image_urls

        for image_url in image_urls:
            print(f"image_url: {image_url}")  # Log the value of image_url
            try:
                print("Inside the try block")  # Log a message
                db.execute("INSERT INTO images (result_id, image_url) VALUES (:result_id, :image_url)",
                        result_id=result_id, image_url=image_url)
            except Exception as e:
                print(f"An error occurred while inserting into the images table: {e}")

        return redirect("/results")
        
    else:
        return render_template("fire_ext.html",  fireEx_faults=FIREEX_FAULTS)



@app.route("/report")
@login_required
def report():
    """Show report of results for the building"""
    # Query database for user's results, ordered by the most recent first. Maybe need to put a time cut off when printing this report.
    results = db.execute(
        """
        SELECT results.*, images.image_url 
        FROM results 
        LEFT JOIN images ON results.id = images.result_id 
        WHERE results.user_id = :user_id 
        ORDER BY results.timestamp DESC 
        LIMIT 10
        """, 
        user_id=session["user_id"]
    )

    # Group results by result_id, each result will have a list of image_urls
    grouped_results = {}
    for result in results:
        if result['id'] not in grouped_results:
            grouped_results[result['id']] = result
            grouped_results[result['id']]['image_urls'] = []
        grouped_results[result['id']]['image_urls'].append(result['image_url'])

    # Render history page with defects
    return render_template("report.html", results=grouped_results.values(), username=session['username'])

@app.route("/results")
@login_required
def results():
    # Check if 'username' is in the session
    if 'username' not in session:
        # If not, redirect to the login page
        return redirect(url_for('login'))
    results = db.execute(
        "SELECT * FROM results WHERE user_id = :user_id ORDER BY timestamp DESC", user_id=session["user_id"]
    )

    # Get the image URLs for each result
    for result in results:
        images = db.execute(
            "SELECT image_url FROM images WHERE result_id = :result_id", result_id=result["id"]
        )
        result["images"] = [image["image_url"] for image in images]

    return render_template("results.html", results=results, username=session['username'])
