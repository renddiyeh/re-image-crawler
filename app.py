import os
from flask import Flask, request, redirect, url_for, jsonify
import haul
import validators
from urllib import unquote
from urlparse import urlparse, parse_qs

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'p7HzB2UBZCxp8B1XGYV10h6eRqOirD8h')


###
# Routing for your application.
###
def getYoutubeId(url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

def youtubeImg(url):
    youtubeID = getYoutubeId(url)
    if youtubeID:
        return "https://i.ytimg.com/vi/"+youtubeID+"/hqdefault.jpg"
    return None

@app.route('/')
def home():
    if url is None:
        return jsonify(error=406, text="No url given."), 406

    url = unquote(request.args.get('url'))

    if not validators.url(url):
        return jsonify(error=406, text="Invalid url."), 406

    result = haul.find_images(url).__dict__
    if "YouTube" in result["title"]:
        result["finder_image_urls"].append(youtubeImg(result["url"]))
    return jsonify(result)

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
