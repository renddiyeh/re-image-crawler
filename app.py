import os
from flask import Flask, request, redirect, url_for, jsonify
import haul
import validators
from urllib import unquote

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'p7HzB2UBZCxp8B1XGYV10h6eRqOirD8h')


###
# Routing for your application.
###

@app.route('/')
def home():
    url = unquote(request.args.get('url'))
    if url is None:
        return jsonify(error=406, text="No url given."), 406
    if not validators.url(url):
        return jsonify(error=406, text="Invalid url."), 406

    result = haul.find_images(url)
    return jsonify(result.__dict__)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['Content-Type'] = 'application/json'
    return response

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page."""
    return jsonify(error=404, text=str(e)), 404

if __name__ == '__main__':
    app.run(debug=True)
