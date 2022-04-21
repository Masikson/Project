import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///closet.db")

TYPES = [
    "bottoms",
    "tops",
    "dresses",
    "shoes"
]

WEATHER = [
    "warm",
    "hot",
    "cold",
    "all"
]

EVENTS = [
    "casual",
    "office",
    "party",
    "all"
]

@app.route("/")
@login_required
def index():
    """Choose your outfit"""
    userid = session["user_id"]

    tops = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'tops'", userid)
    bottoms = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'bottoms'", userid)
    dresses = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'dresses'", userid)
    shoes = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'shoes'", userid)

    return render_template("index.html", tops=tops, bottoms=bottoms, dresses=dresses, shoes=shoes)
    #return render_template("picture2.html")

@app.route('/choose', methods = ['GET', 'POST'])
@login_required
def choose():
    userid=session["user_id"]
    if request.method == "POST":
        types=["dresses", "tops and bottoms"]
        type = request.form.get("type")
        if not type:
            return apology("must provide a type", 400)

        if type not in types:
            return apology("Invalid type", 400)

        weather = request.form.get("weather")
        if weather:
            if weather not in WEATHER:
                return apology("Invalid weather", 400)
            if weather == "all":
                weather = "None"

        event = request.form.get("event")
        if event:
            if event not in EVENTS:
                return apology("Invalid event", 400)
            if event=="all":
                event=None
        print(weather)
        print(event)

        #filter specified items
        if not weather and not event:
            dresses = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'dresses'", userid)
            tops = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'tops'", userid)
        elif not weather:
            dresses = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'dresses' AND (event=? OR event IS NULL)", userid,event)
            tops = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'tops' AND (event=? OR event IS NULL)", userid, event)
        elif not event:
            dresses = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'dresses' AND (weather=? OR weather IS NULL)", userid, weather)
            tops = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'tops' AND (weather=? OR weather IS NULL)", userid, weather)
            print(dresses)
        else:
            dresses = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'dresses' AND (weather=? OR weather IS NULL) AND (event=? OR event IS NULL)", userid, weather, event)
            tops = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'tops' AND (weather=? OR weather IS NULL) AND (event=? OR event IS NULL)", userid, weather, event)

        if type=="dresses":
            return render_template("dresses.html", dresses=dresses, weather=weather, event=event)
        else:
            return render_template("tops.html", tops=tops, weather=weather, event=event)

    else:
        return render_template("choose.html", WEATHER=WEATHER, EVENTS=EVENTS)



@app.route('/processtop', methods = ['POST'])
@login_required
def process():
    userid = session["user_id"]
    top = request.form.get('hidden1')
    weather=request.form.get('weather')
    event=request.form.get('event')
    print(weather)
    print(event)

    if top: #
        print(top)

    if weather=="None" and event=="None":
        bottoms = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'bottoms'", userid)
    elif weather=="None":
        bottoms = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'bottoms' AND (event=? OR event IS NULL)", userid,event)

    elif event=="None":
        bottoms = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'bottoms' AND (weather=? OR weather IS NULL)", userid, weather)
    else:
        bottoms = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'bottoms' AND (weather=? OR weather IS NULL) AND (event=? OR event IS NULL)", userid, weather, event)
        print(bottoms)

    return render_template("bottoms.html", bottoms=bottoms, weather=weather, event=event, top=top)

@app.route('/processbottom', methods = ['POST'])
@login_required
def process2():
    userid=session["user_id"]
    bottom = request.form['hidden2']
    weather=request.form.get('weather')
    event=request.form.get('event')
    top=request.form.get('top')
    if bottom:
        print(bottom)

    if weather=="None" and event=="None":
        shoes = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'shoes'", userid)
    elif weather=="None":
        shoes = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'shoes' AND (event=? OR event IS NULL)", userid,event)
    elif event=="None":
        shoes = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'shoes' AND (weather=? OR weather IS NULL)", userid, weather)
    else:
        shoes = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'shoes' AND (weather=? OR weather IS NULL) AND (event=? OR event IS NULL)", userid, weather, event)

    return render_template("shoes.html", shoes=shoes, weather=weather, event=event, top=top, bottom=bottom)

@app.route('/processdress', methods = ['POST'])
@login_required
def process3():
    userid=session["user_id"]
    dress = request.form['hidden3']
    weather=request.form.get('weather')
    event=request.form.get('event')
    if dress:
        print(dress)

    if weather=="None" and event=="None":
        shoes = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'shoes'", userid)
    elif weather=="None":
        shoes = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'shoes' AND (event=? OR event IS NULL)", userid,event)
    elif event=="None":
        shoes = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'shoes' AND (weather=? OR weather IS NULL)", userid, weather)
    else:
        shoes = db.execute("SELECT picture FROM closet WHERE user_id = ? AND type = 'shoes' AND (weather=? OR weather IS NULL) AND (event=? OR event IS NULL)", userid, weather, event)

    print(shoes)
    return render_template("shoesdress.html", shoes=shoes, weather=weather, event=event, dress=dress)

@app.route('/processshoe', methods = ['POST'])
@login_required
def process4():
    userid=session["user_id"]
    shoe = request.form['hidden4'].removeprefix('/static/')
    top=request.form.get('top').removeprefix('/static/')
    bottom=request.form.get('bottom').removeprefix('/static/')


    topid= db.execute("SELECT id FROM closet WHERE picture=?", top)[0]["id"]
    bottomid= db.execute("SELECT id FROM closet WHERE picture=?", bottom)[0]["id"]
    shoesid = db.execute("SELECT id FROM closet WHERE picture=?", shoe)[0]["id"]

    db.execute("INSERT INTO outfits (user_id, top_id, bottom_id, shoes_id, date) VALUES(?,?,?,?,datetime('now'))", userid, topid, bottomid, shoesid)


    return redirect("/myoutfits")

@app.route('/processshoedress', methods = ['POST'])
@login_required
def process5():
    userid=session["user_id"]
    shoe = request.form['hidden4'].removeprefix('/static/')
    dress=request.form.get('dress').removeprefix('/static/')



    dressid= db.execute("SELECT id FROM closet WHERE picture=?", dress)[0]["id"]
    shoesid = db.execute("SELECT id FROM closet WHERE picture=?", shoe)[0]["id"]
    db.execute("INSERT INTO outfits (user_id, dress_id, shoes_id, date) VALUES (?, ?, ?, datetime('now'))", userid, dressid, shoesid)



    return redirect("/myoutfits")

# @app.route('/dressme', methods = ['POST'])
# @login_required
# def dressme():
#     userid = session["user_id"]

@app.route('/myoutfits')
@login_required
def outfits():
    userid=session["user_id"]

    #outfit id, sort by date descendingg
    outfits= db.execute("SELECT id, top_id, bottom_id, dress_id, shoes_id FROM outfits WHERE user_id =? ORDER BY datetime(date) DESC",userid)
    print(outfits)
    #[{'id': 2, 'top_id': None, 'bottom_id': None, 'dress_id': 7, 'shoes_id': 20}, {'id': 1, 'top_id': 11, 'bottom_id': 17, 'dress_id': None, 'shoes_id': 23}]

    dresses =[]
    topbottoms = []
    for outfit in outfits:
        # if it's a top and bottom
        if outfit["dress_id"] == None:
            top = db.execute("SELECT picture FROM closet WHERE id=?", outfit["top_id"])[0]["picture"]
            bottom = db.execute("SELECT picture FROM closet WHERE id=?", outfit["bottom_id"])[0]["picture"]
            shoes = db.execute("SELECT picture FROM closet WHERE id=?", outfit["shoes_id"])[0]["picture"]
            topbottoms.append({'top': top, 'bottom': bottom, 'shoes': shoes})
            print(topbottoms)
        else:
            dress = db.execute("SELECT picture FROM closet WHERE id=?", outfit["dress_id"])[0]["picture"]
            shoes = db.execute("SELECT picture FROM closet WHERE id=?", outfit["shoes_id"])[0]["picture"]
            dresses.append({'dress': dress, 'shoes': shoes})
            print(dresses)

    return render_template("myoutfits.html", topbottoms=topbottoms, dresses=dresses)






@app.route('/gallery')
@login_required
def gallery():
    userid=session["user_id"]

    #outfit id, sort by date descending, users other than logged in
    outfits= db.execute("SELECT id, top_id, bottom_id, dress_id, shoes_id FROM outfits WHERE user_id !=? ORDER BY datetime(date) DESC",userid)
    print(outfits)
    #[{'id': 2, 'top_id': None, 'bottom_id': None, 'dress_id': 7, 'shoes_id': 20}, {'id': 1, 'top_id': 11, 'bottom_id': 17, 'dress_id': None, 'shoes_id': 23}]

    dresses =[]
    topbottoms = []
    for outfit in outfits:
        # if it's a top and bottom
        if outfit["dress_id"] == None:
            top = db.execute("SELECT picture FROM closet WHERE id=?", outfit["top_id"])[0]["picture"]
            bottom = db.execute("SELECT picture FROM closet WHERE id=?", outfit["bottom_id"])[0]["picture"]
            shoes = db.execute("SELECT picture FROM closet WHERE id=?", outfit["shoes_id"])[0]["picture"]
            topbottoms.append({'top': top, 'bottom': bottom, 'shoes': shoes})
            print(topbottoms)
        else:
            dress = db.execute("SELECT picture FROM closet WHERE id=?", outfit["dress_id"])[0]["picture"]
            shoes = db.execute("SELECT picture FROM closet WHERE id=?", outfit["shoes_id"])[0]["picture"]
            dresses.append({'dress': dress, 'shoes': shoes})
            print(dresses)

    return render_template("gallery.html", topbottoms=topbottoms, dresses=dresses)

# check file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# https://pythonbasics.org/flask-upload-file/
@app.route("/upload", methods = ["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return apology("no file part", 400)
        f = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if f.filename == '':
            return apology("no selected file", 400)
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return "file uploaded"
        else:
            return apology("not successful", 400)

        # Ensure type was submitted
        type = request.form.get("type")
        if not type:
            return apology("must provide a type", 400)
        if type not in TYPES:
            return apology("Invalid type", 400)

        weather = request.form.get("weather")
        if weather:
            if weather not in WEATHER:
                return apology("Invalid weather", 400)
            if weather == "all":
                weather = None

        event = request.form.get("event")
        if event:
            if event not in EVENTS:
                return apology("Invalid event", 400)
            if event=="all":
                event=None

        userid = session["user_id"]

        db.execute("INSERT INTO closet (user_id, picture, type, weather, event) VALUES (?, ?, ?, ?, ?)",
                    userid, filename, type, weather, event)

        return redirect("/")

    else:
        return render_template("upload.html", TYPES = TYPES, WEATHER = WEATHER, EVENTS = EVENTS)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username doesn't exist
        if len(rows) != 0:
            return apology("username already exists", 403)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        # ensure passwords are the same
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords do not match", 403)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        # Redirect user to log in
        return redirect("/login")

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

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change password"""

    if request.method == "POST":

        userid = session["user_id"]
        # Ensure old password was submitted
        if not request.form.get("password"):
            return apology("must provide old password", 403)

        # Ensure new password was submitted
        elif not request.form.get("newpassword"):
            return apology("must provide new password", 403)

        # Ensure new password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?", userid)

        # Ensure old password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid old password", 403)

        # ensure passwords are the same
        if request.form.get("confirmation") != request.form.get("newpassword"):
            return apology("passwords do not match", 403)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("newpassword")), userid)

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("change.html")




def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
