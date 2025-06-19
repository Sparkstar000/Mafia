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
def players():
    client = connect_db()
    sql = """SELECT * from players ORDER BY name ASC"""
    result = client.execute(sql)
    players = result.rows
    return render_template("pages/players.jinja")