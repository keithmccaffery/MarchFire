import os

import csv
import requests
from PIL import Image as PilImage
from reportlab.platypus import PageBreak
from reportlab.platypus import BaseDocTemplate, Paragraph, Spacer, Frame, PageTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import json
import pyodbc
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from MsSql import MsSql

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_file, Response, jsonify
from flask import session as flask_session
from flask_session import Session as FlaskSession
from werkzeug.security import check_password_hash, generate_password_hash
from icecream import ic

from helpers import apology, login_required, lookup, usd
from datetime import datetime
import pytz
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SqlAlchemySession
from sqlalchemy import text
import logging
logging.basicConfig(level=logging.ERROR)

eastern_australia_tz = pytz.timezone('Australia/Sydney')
current_time = datetime.now(eastern_australia_tz)
# Configure application
import os

app = Flask(__name__)
app.secret_key = 'mandy'

# Set up Azure Key Vault client
#keyVaultName = "Coogee"
#KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://Coogee.vault.azure.net/", credential=credential)
#client = SecretClient(vault_url=KVUri, credential=credential)

# Retrieve connection string from Key Vault
odbc_conn_str = client.get_secret("DbConnectionString").value

# Convert to SQLAlchemy format
sqlalchemy_conn_str = urllib.parse.quote_plus(odbc_conn_str)
sqlalchemy_conn_str = "mssql+pyodbc:///?odbc_connect={}".format(sqlalchemy_conn_str)

# Configure MSSQL
engine = create_engine(sqlalchemy_conn_str)
# Configure MSSQL
#db = SQL(connection_string)
RESULTS = {}

try:
    with engine.connect() as conn:
        DOOR_FAULTS = conn.execute(text("SELECT * FROM doorfixes")).fetchall()
        LIGHT_FAULTS = conn.execute(text("SELECT * FROM em_lightfixes")).fetchall()
        FIREEX_FAULTS = conn.execute(text("SELECT * FROM fireExfixes")).fetchall()
except Exception as e:
    print(f"Failed to connect to the database: {e}")
# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
FlaskSession(app)

# Configure CS50 Library to use SQLite database
# Need to set up some other databases for the assests and the results of the inspections
#db = SQL("sqlite:///final.db")



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
            return apology("passwords do not match", 400)

        # Query database for username
        try:
            with engine.connect() as conn:
                query = text("SELECT * FROM users WHERE username = :username")
                result_proxy = conn.execute(query.params(username=request.form.get("username")))
        except Exception as e:
            print(f"Failed to execute query: {e}")

        if result_proxy.rowcount > 0:
            rows = result_proxy.fetchall()
        else:
            rows = []

        # Ensure username does not already exist
        if len(rows) != 0:
            return apology("username already exists", 400)

        # Generate hashed password
        hashed_password = generate_password_hash(request.form.get("password"))

        # Insert new user into database
        try:
            with engine.begin() as conn:
                query = text("INSERT INTO users (username, hash) VALUES(:username, :hashed_password)")
                conn.execute(query.params(username=request.form.get("username"), hashed_password=hashed_password))
        except Exception as e:
            print(f"Failed to insert new user: {e}")

        # Query database for newly inserted user
        try:
            with engine.connect() as conn:
                query = text("SELECT * FROM users WHERE username = :username")
                result_proxy = conn.execute(query.params(username=request.form.get("username")))
                rows = result_proxy.fetchall()
                print(f"Query results: {rows}")
        except Exception as e:
            print(f"Failed to execute query: {e}")
            return apology("registration failed", 500)

        if len(rows) == 0:
            print("No user found with the specified username.")
        else:
            rows = []

        # Remember which user has logged in
        if rows:
            session["user_id"] = rows[0]["id"]
        else:
            print("No user found with the specified username.")

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

        # Query database for user
        try:
            with engine.connect() as conn:
                query = text("SELECT * FROM users WHERE username = :username")
                result_proxy = conn.execute(query.params(username=request.form.get("username")))
                rows = result_proxy.fetchall()
                print(f"Query results: {rows}")
        except Exception as e:
            print(f"Failed to execute query: {e}")
            return apology("login failed", 500)

        # Assuming that 'id' is the first column, 'username' is the second column, and 'hash' is the third column in your 'users' table
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

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
    asset_type = request.form.get('assetType')
    location = request.form.get('location')
    # Combine the asset type and location
    door = f'{location} - {asset_type}'

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

         # Fetch the fault and remedy
        with engine.connect() as conn:
            result_proxy = conn.execute("SELECT fault FROM doorfixes WHERE fault_id = :door_fault", door_fault=door_fault)
            faultDict = dict(result_proxy.fetchone())
            faultStr = faultDict['fault']

            result_proxy = conn.execute("SELECT remedy FROM doorfixes WHERE fault_id = :door_fault", door_fault=door_fault)
            remedyDict = dict(result_proxy.fetchone())
            remedyStr = remedyDict['remedy']

        # The strings were saved into these variables to build the results table below.
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
        with engine.connect() as conn:
            conn.execute("INSERT INTO results (user_id, asset, fault_id, fault, remedy, comment, timestamp) VALUES (:user_id, :asset, :fault_id, :fault, :remedy, :comment, :timestamp)",
                user_id=session["user_id"], asset=asset, fault_id=door_fault, fault=fault, remedy=remedy, comment=comment, timestamp=datetime.now(eastern_australia_tz))

         # Get the ID of the last inserted row
        with engine.connect() as conn:
            result_proxy = conn.execute("SELECT last_insert_rowid()")
            result_id = result_proxy.fetchone()["last_insert_rowid()"]
       

        # Get the imageUrl string from the form and split it into a list of URLs
        image_urls = request.form.get("imageUrl").split(';')

        print(f"result_id: {result_id}")  # Log the value of result_id
        print(f"image_urls: {image_urls}")  # Log the value of image_urls

        for image_url in image_urls:
            print(f"image_url: {image_url}")  # Log the value of image_url
            try:
                print("Inside the try block")  # Log a message
                with engine.connect() as conn:
                    conn.execute("INSERT INTO images (result_id, image_url) VALUES (:result_id, :image_url)",
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

    # Get the asset type and location from the form data
    asset_type = request.form.get('assetType')
    location = request.form.get('location')
    # Combine the asset type and location
    light = f'{location} - {asset_type}'
    
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

        # Fetch the fault and remedy
        with engine.connect() as conn:
            result_proxy = conn.execute("SELECT fault FROM em_lightfixes WHERE fault_id = :light_fault", light_fault=light_fault)
            faultDict = dict(result_proxy.fetchone())
            faultStr = faultDict['fault']

            result_proxy = conn.execute("SELECT remedy FROM em_lightfixes WHERE fault_id = :light_fault", light_fault=light_fault)
            remedyDict = dict(result_proxy.fetchone())
            remedyStr = remedyDict['remedy']

        # The strings were saved into these variables to build the results table below.
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
        with engine.connect() as conn:
            conn.execute("INSERT INTO results (user_id, asset, fault_id, fault, remedy, comment, timestamp) VALUES (:user_id, :asset, :fault_id, :fault, :remedy, :comment, :timestamp)",
                user_id=session["user_id"], asset=asset, fault_id=light_fault, fault=fault, remedy=remedy, comment=comment, timestamp=datetime.now(eastern_australia_tz))

            # Get the ID of the last inserted row
            result_proxy = conn.execute("SELECT last_insert_rowid()")
            result_id = result_proxy.fetchone()["last_insert_rowid()"]

        # Get the imageUrl string from the form and split it into a list of URLs
        image_urls = request.form.get("imageUrl").split(';') 

        print(f"result_id: {result_id}")  # Log the value of result_id
        print(f"image_urls: {image_urls}")  # Log the value of image_urls

        for image_url in image_urls:
            print(f"image_url: {image_url}")  # Log the value of image_url
            try:
                print("Inside the try block")  # Log a message
                with engine.connect() as conn:
                    conn.execute("INSERT INTO images (result_id, image_url) VALUES (:result_id, :image_url)",
                        result_id=result_id, image_url=image_url)
            except Exception as e:
                print(f"An error occurred while inserting into the images table: {e}")

        return redirect("/results")
            
    # The else statement has been removed as it was not associated with an if statement
    else:    
        return render_template("em_lights.html",  light_faults=LIGHT_FAULTS)



# These following functions could be completed as per the doors method above, however, since hearing about OOP
# it maybe better to write app.py having classes producing the objects.


@app.route("/fire_ext", methods=["POST", "GET"])
def fire_ext():
    # Get the asset type and location from the form data
    asset_type = request.form.get('assetType')
    location = request.form.get('location')
    # Combine the asset type and location
    fireEx = f'{location} - {asset_type}'
    
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
        # Fetch the fault and remedy
        with engine.connect() as conn:
            result_proxy = conn.execute("SELECT fault FROM fireEXfixes WHERE fault_id = :fireEx_fault", fireEx_fault=fireEx_fault)
            faultDict = dict(result_proxy.fetchone())
            faultStr = faultDict['fault']

            result_proxy = conn.execute("SELECT remedy FROM fireEXfixes WHERE fault_id = :fireEx_fault", fireEx_fault=fireEx_fault)
            remedyDict = dict(result_proxy.fetchone())
            remedyStr = remedyDict['remedy']

        # The strings were saved into these variables to build the results table below.
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
        with engine.connect() as conn:
            conn.execute("INSERT INTO results (user_id, asset, fault_id, fault, remedy, comment, timestamp) VALUES (:user_id, :asset, :fault_id, :fault, :remedy, :comment, :timestamp)",
                user_id=session["user_id"], asset=asset, fault_id=fireEx_fault, fault=fault, remedy=remedy, comment=comment, timestamp=datetime.now(eastern_australia_tz))

            # Get the ID of the last inserted row
            result_proxy = conn.execute("SELECT last_insert_rowid()")
            result_id = result_proxy.fetchone()["last_insert_rowid()"]

        # Get the imageUrl string from the form and split it into a list of URLs
        image_urls = request.form.get("imageUrl").split(';')

        print(f"result_id: {result_id}")  # Log the value of result_id
        print(f"image_urls: {image_urls}")  # Log the value of image_urls

        for image_url in image_urls:
            print(f"image_url: {image_url}")  # Log the value of image_url
            try:
                print("Inside the try block")  # Log a message
                with engine.connect() as conn:
                    conn.execute("INSERT INTO images (result_id, image_url) VALUES (:result_id, :image_url)",
                        result_id=result_id, image_url=image_url)
            except Exception as e:
                print(f"An error occurred while inserting into the images table: {e}")

        return redirect("/results")
        
    else:
        return render_template("fire_ext.html",  fireEx_faults=FIREEX_FAULTS)

@app.route("/other", methods=["POST", "GET"])
def other():
    if request.method == "POST":
        from datetime import datetime
        asset_type = request.form.get('assetType')
        location = request.form.get('location')
        asset = f'{location} - {asset_type}'
        fault = request.form.get("fault")
        remedy = request.form.get("remedy")
        comment = request.form.get("comment")

        try:
            session = SqlAlchemySession(bind=engine)
            session.execute(
                text("INSERT INTO results (user_id, asset, fault_id, fault, remedy, comment, timestamp) VALUES (:user_id, :asset, :fault_id, :fault, :remedy, :comment, :timestamp)"),
                {
                    "user_id": flask_session["user_id"],  # get user_id from the session
                    "asset": asset, 
                    "fault_id": request.form.get("fault_id") or 0, 
                    "fault": fault, 
                    "remedy": remedy, 
                    "comment": comment, 
                    "timestamp": datetime.now()
                }
            )
            session.commit()
            result_id = session.execute(text("SELECT @@IDENTITY AS id")).scalar()
        except Exception as e:
            session.rollback()
            print(f"Failed to execute query: {e}")
            return apology("fault logging failed", 500)
        finally:
            session.close()

        image_urls = request.form.get("imageUrl").split(';')

        for image_url in image_urls:
            try:
                session = SqlAlchemySession(bind=engine)
                session.execute(
                    text("INSERT INTO images (result_id, image_url) VALUES (:result_id, :image_url)"),
                    {"result_id": result_id, "image_url": image_url}
                )
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Failed to execute query: {e}")
                return apology("image logging failed", 500)
            finally:
                session.close()
        print("Redirecting to /results")  # Print a message before the redirect
        return redirect("/results")
        
    else:
        return render_template("other.html")

@app.route("/report")
@login_required
def report():
    """Show report of results for the building"""
    # Query database for user's results, ordered by the most recent first. Maybe need to put a time cut off when printing this report.
    with engine.connect() as conn:
        result_proxy = conn.execute(
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
        results = [dict(row) for row in result_proxy.fetchall()]

    # Group results by result_id, each result will have a list of image_urls
    grouped_results = {}
    for result in results:
        if result['id'] not in grouped_results:
            grouped_results[result['id']] = result
            grouped_results[result['id']]['image_urls'] = []
        grouped_results[result['id']]['image_urls'].append(result['image_url'])

    # Render history page with defects
    return render_template("report.html", results=grouped_results.values(), username=session['username'])
@app.route('/results')
@login_required
def results():
    # Check if 'username' is in the flask_session
    if 'username' not in flask_session:
        # If not, redirect to the login page
        return redirect(url_for('login'))
    
    try:
        session = SqlAlchemySession(bind=engine)
        result_proxy = session.execute(
            text("SELECT * FROM results WHERE user_id = :user_id ORDER BY timestamp DESC"),
            {"user_id": flask_session["user_id"]}
        )

        keys = result_proxy.keys()
        print(f"Number of keys: {len(keys)}")  # Print the number of keys

        results = []
        for row in result_proxy.fetchall():
            print(f"Number of elements in row: {len(row)}")  # Print the number of elements in each row
            results.append({column: value for column, value in zip(keys, row)})

        print(f"Results: {results}")  # Print the results

    except Exception as e:
        print(f"Failed to execute query: {e}")
        return apology("failed to retrieve results", 500)
    finally:
        session.close()

    # Render history page with defects
    return render_template("results.html", results=results, username=flask_session['username'])


@app.route('/create_pdf', methods=['POST'])
def create_pdf():
     # Create the flowables list
    flowables = []
    # Fetch the data from the database
    with engine.connect() as conn:
        result_proxy = conn.execute("""
            SELECT results.*, images.image_url 
            FROM results 
            LEFT JOIN images ON results.id = images.result_id 
            WHERE results.user_id = :user_id 
            ORDER BY results.timestamp DESC 
            LIMIT 10
            """, 
            user_id=session["user_id"]
        )
        results = [dict(row) for row in result_proxy.fetchall()]

    for result in results:
        if result['image_url']:
            # Print the image URL
            print(f"Image URL: {result['image_url']}")
            # Reduce the width of the image
            #img = Image(result['image_url'], width=200)  # Reduced from 400 to 300
           
        else:
            print(f"Warning: Empty image URL for result {result['id']}")
            # Skip adding an image to the PDF
    # Group results by result_id, each result will have a list of image_urls
    grouped_results = {}
    for result in results:
        if result['id'] not in grouped_results:
            grouped_results[result['id']] = result
            grouped_results[result['id']]['image_urls'] = []
        grouped_results[result['id']]['image_urls'].append(result['image_url'])

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    # class MyPageTemplate(PageTemplate):
    #     def afterDrawPage(self, canvas, doc):
    #         # Draw horizontal rulers
    #         for i in range(int(A4[0])):
    #             if i % 50 == 0:
    #                 canvas.drawString(i, A4[1] - 10, str(i))
    # Create the PDF object, using the buffer as its "file"
    doc = BaseDocTemplate(buffer, pagesize=A4)

    # Create a Frame with a specified width and start position
    frame = Frame(50, 50, A4[0]-100, A4[1]-100)  # Adjust the x, y, width, and height as needed


    # Create a custom PageTemplate that uses the Frame
    #template = MyPageTemplate(frames=[frame])
    template = PageTemplate(frames=[frame])
    # Add the custom PageTemplate to the BaseDocTemplate
    doc.addPageTemplates([template])


    # Create a Paragraph
    styles = getSampleStyleSheet()

    print(grouped_results)

# Add the flowables for each result
    for result_id, result in grouped_results.items():
        keys = ['asset', 'fault_id', 'fault', 'remedy', 'comment']
        for key in keys:
            text = f"{key.capitalize()}: {result[key]}"
            print(text)
            paragraph = Paragraph(text, styles['Normal'])
            flowables.append(paragraph)
        flowables.append(Spacer(1, 20))

        # Add images for each result
        for image_url in result.get('image_urls', []):
            if not image_url:  # Skip if the URL is empty
                continue
            # Open the image with PIL to get its size
            pil_image = PilImage.open(requests.get(image_url, stream=True).raw)
            original_width, original_height = pil_image.size

            # Calculate the new height based on the aspect ratio
            new_width = 250
            new_height = (new_width / original_width) * original_height

            # Create the Image object with the new width and height
            image = Image(image_url, width=new_width, height=new_height)
            flowables.append(image)
            flowables.append(Spacer(1, 20))

    # Build the PDF
    doc.build(flowables)

    # Make the buffer's current position at 0
    buffer.seek(0)

    # Create a response
    response = Response(buffer, mimetype='application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename='report.pdf')

    return response

@app.route("/debug/users", methods=["GET"])
def debug_users():
    with engine.connect() as conn:
        result_proxy = conn.execute("SELECT username FROM users")
        rows = [row["username"] for row in result_proxy.fetchall()]
    return jsonify(rows)

from sqlalchemy.orm import Session

@app.route('/test_insert', methods=['GET'])
def test_insert():
    from datetime import datetime
    with Session(engine) as session:
        query = text("INSERT INTO results (user_id, asset, fault_id, fault, remedy, comment, timestamp) VALUES (:user_id, :asset, :fault_id, :fault, :remedy, :comment, :timestamp)")
        params = {
            "user_id": 59,  # replace with a valid user_id
            "asset": "Test Asset",
            "fault_id": 0,  # replace with a valid fault_id
            "fault": "Test Fault",
            "remedy": "Test Remedy",
            "comment": "Test Comment",
            "timestamp": datetime.now()
        }
        result_proxy = session.execute(query, params)
        session.commit()
    return f"Rows inserted: {result_proxy.rowcount}"