#!/usr/bin/env python3.9

"""handle views"""
import json
import datetime
import os
from flask import render_template, session, redirect, url_for, request, \
	make_response, jsonify
from sqlalchemy import exc, text, column

from .. import db
from . import main, logger

@main.route("/")
def index():
	print("print: index", flush=True)
	logger.info("logger: index")
	logger.debug("debug: index")
	return render_template('index.html')

