# coding: utf-8
"""
Initialize Flask app

"""
from flask import Flask

app = Flask(__name__)

app.config.update({
    'OBJECTS_ON_PAGE': 20
})

# Pull in URL dispatch routes
import urls