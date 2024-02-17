# from datetime import date

import validators
from flask import Flask, request
from flask_cors import CORS

from db import create_record, get_record, record_exists


MAX_DAILY_URLS = 5

app = Flask("app")
CORS(app)


@app.post("/create")
def create():
    # check for daily limit
    # today = date.today().isoformat()

    # if get_record(f"count_{today}", 0) > MAX_DAILY_URLS:
    #     return "Daily limit reached", 503

    # try to insert
    url = request.form.get("url")
    alias = request.form.get("alias")

    if url is None:
        return "Missing URL", 400
    elif not validators.url(url):
        return "Invalid URL", 400
    elif alias is None or len(alias) == 0:
        return "Missing alias", 400
    elif len(alias) > 30 or not all(c.isalnum() for c in alias):
        return "Invalid alias", 400
    elif record_exists(alias):
        return "Alias already exists", 400

    create_record(alias, url)
    # db["stats"][today] = db["stats"].get(today, 0) + 1

    return "Success", 200


@app.get("/get")
def get():
    alias = request.args.get("alias", "")

    try:
        url = get_record(alias)
    except KeyError:
        return "Not found", 404

    return url, 200


if __name__ == "__main__":
    app.run()
