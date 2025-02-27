# app/__init__.py
from flask import Flask

app = Flask(__name__)

def register_routes():
    from app import routes

register_routes()