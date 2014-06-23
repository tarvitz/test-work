# coding: utf-8

from flask import render_template

from application import app, views

app.add_url_rule('/_ah/warmup', 'warmup',
                 view_func=views.warmup)
app.add_url_rule('/', 'home', view_func=views.home)

@app.route('/login/required/')
def login_required():
    return render_template('login_required.html'), 200

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500