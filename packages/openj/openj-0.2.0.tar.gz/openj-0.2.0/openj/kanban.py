#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from openj.db import get_db
from openj.api.card import create_card
from openj.api.card import read_card
from openj.api.card import update_card
from openj.api.card import delete_card

kanban = Blueprint("kanban", __name__)


@kanban.route("/kanban")
def index():
    interval = request.args.get("interval")
    lanes = get_db().execute("SELECT * FROM lane").fetchall()
    cards = get_db().execute("SELECT * FROM card").fetchall()
    groups = {l["title"]: [c for c in cards if c["lane_id"] == l["id"]] for l in lanes}
    return render_template("kanban.html", interval=interval, groups=groups)


@kanban.route("/kanban/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        response = create_card()
        if response[1] < 300:
            return redirect(url_for("kanban.index"))
        flash(response[0], "error")
    lanes = get_db().execute("SELECT * FROM lane").fetchall()
    return render_template("create_card.html", lanes=lanes)


@kanban.route("/kanban/update/<int:id>", methods=("GET", "POST"))
def update(id: int):
    if request.method == "POST":
        response = update_card(id)
        if response[1] < 300:
            return redirect(url_for("kanban.index"))
        flash(response[0], "error")
    card = read_card(id)[0]
    lanes = get_db().execute("SELECT * FROM lane").fetchall()
    return render_template("update_card.html", lanes=lanes, card=card)


@kanban.get("/kanban/delete/<int:id>")
def delete(id: int):
    delete_card(id)
    return redirect(url_for("kanban.index"))
