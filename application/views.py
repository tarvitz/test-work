# coding: utf-8
import os

from google.appengine.api import users
from application.forms import MessageForm
from flask import (
    request, render_template, flash, url_for, redirect, jsonify, abort
)


from google.appengine.ext import ndb
from application import app, decorators
from models import Message


def home():
    return render_template('home.html')


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
    """
    return ''


@app.route('/admin/messages/')
@decorators.admin_required
def message_list():
    page_size = app.config.get('OBJECTS_ON_PAGE', 20)
    messages = Message.query().fetch(page_size)
    return render_template('messages.html', messages=messages)


@app.route('/api/messages/<int:pk>/', methods=['GET', ])
def message_get(pk=None):
    msg = Message.get_by_id(pk)
    return jsonify(msg.to_dict()), 200


@app.route('/api/messages/', methods=['POST', ])
def message_post():
    form = MessageForm(request.form)
    if request.method == 'POST' and form.validate():
        msg = Message(message_id=form.data['message_id'],
                      message_data=form.data['message_data'])
        msg.put()
        return jsonify(
            message_id=form.data['message_id']
        ), 201
    return jsonify(
        form.errors
    ), 400

@app.route('/api/messages/<int:pk>/', methods=['PUT', ])

def message_put(pk=None):
    form = MessageForm(request.form)
    if request.method == 'PUT' and form.validate():

        @ndb.transactional(retries=1)
        def put():
            key = ndb.Key('Message', pk)
            msg = key.get()
            if msg:
                msg = Message(key=key, **form.data)
                msg.put()
            return msg

        msg = put()
        return jsonify(msg.to_dict()), 200
    return jsonify({'errors': {}}), 400


@app.route('/api/messages/<int:pk>/', methods=['DELETE', ])
def message_delete(pk=None):
    """ delete message

    :param pk:
    :return:
    """
    if request.method == 'DELETE':
        msg = Message.get_by_id(pk)
        msg.key.delete()
        return jsonify({
            pk: 'deleted'
        }), 204
    return jsonify({'errors': {}}), 400
