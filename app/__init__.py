from flask import Flask, render_template, request, redirect
from libsql_client  import create_client_sync
from dotenv import load_dotenv
import html
import os
       
app = Flask(__name__)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_KEY = os.getenv("DATABASE_KEY")

client = None

def connect_db():
    global client
    if client == None:
        client = create_client_sync(url=DATABASE_URL, auth_token=DATABASE_KEY)
    return client

@app.get("/")
def index():
    return render_template("pages/home.jinja")

@app.get("/players")
def spectate():
    client = connect_db()
    sql = """SELECT * from players ORDER BY id ASC"""
    result = client.execute(sql)
    players = result.rows
    return render_template("pages/players.jinja", players=players, id=0)

@app.get("/players/<int:encoded>")
def players(encoded):

    id = encoded / 27

    client = connect_db()

    sql = """SELECT * from players ORDER BY id ASC"""
    result = client.execute(sql)
    players = result.rows

    return render_template("pages/players.jinja", players=players, id=id)

@app.post("/join")
def join():

    name = request.form.get("name")
    client = connect_db()
    

    sql = """INSERT INTO players (name) VALUES (?)"""
    values = [name]
    client.execute(sql, values)

    sql = """SELECT id FROM players WHERE name=?"""
    values = [name]
    result = client.execute(sql, values)
    id = result.rows[0]

    return redirect(f"/players/{id[0] * 27}")


@app.post("/rerole/<int:id>")
def rerole(id):

    role = request.form.get("role")

    client = connect_db()

    sql = """UPDATE players SET role=? WHERE id=?"""
    values = [role,id]
    client.execute(sql, values)

    return redirect("/narrator/27")


@app.get("/narrator/27")
def narrate():
    client = connect_db()
    sql = """SELECT * from players ORDER BY id ASC"""
    result = client.execute(sql)
    players = result.rows

    return render_template("pages/narrate.jinja", players=players)
