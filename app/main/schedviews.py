#!/usr/bin/env python3.9

"""handle schedule views"""
import json
import datetime
import os
from base64 import b64decode
from flask import render_template, redirect, url_for, request, \
	make_response, jsonify, Response, stream_with_context
# from flask_cors import CORS, cross_origin
from sqlalchemy import exc
from .. import db
from . import main, logger

class Reservation(db.Model):
	__tablename__ = 'reservation'
	id = db.Column(db.Integer, unique=True, index=True, autoincrement=True, primary_key=True)
	resDate = db.Column(db.Date)
	resTime = db.Column(db.Integer)
	duration = db.Column(db.Integer)
	pilot = db.Column(db.String(31))
	note = db.Column(db.String(255))

	def __repr__(self):
		return '<Reservation %s>' % self.pilot

@main.route("/schedule")
def schedule():
	return render_template('schedule.html')


@main.route('/addreservation', methods=['POST'])
def addreservation():
	"""add reservation"""
	try:
		print("add reservation")
		date = request.json.get('resdate')
		time = request.json.get('restime')
		duration = request.json.get('duration')
		pilot = request.json.get('pilot')
		note = request.json.get('note')
		res = Reservation()

		res.resDate = date
		res.resTime = time
		res.duration = duration
		res.pilot = pilot
		res.note = note
		print(res)
		db.session.add(res)
		db.session.commit()
		return jsonify(success=True, id=res.id), 200
	except exc.SQLAlchemyError as e:
		print("exception adding reservation: ", e, flush=True)
		db.session.rollback()
		return jsonify(success=False), 400

@main.route('/modreservation', methods=['POST'])
def modreservation():
	"""change reservation"""
	try:
		id = request.json.get('id')
		date = request.json.get('resdate')
		time = request.json.get('restime')
		duration = request.json.get('duration')
		pilot = request.json.get('pilot')
		note = request.json.get('note')
		res = Reservation.query.filter_by(id=id).first()
		res.resDate = date
		res.resTime = time
		res.duration = duration
		res.pilot = pilot
		res.note = note
		db.session.commit()
		return jsonify(success=True), 200
	except exc.SQLAlchemyError as e:
		print("exception changing reservation: ", e, flush=True)
		db.session.rollback()
		return jsonify(success=False), 400

@main.route('/delreservation/<id>', methods=['get'])
def delreservation(id):
	"""delete reservation"""
	try:
		Reservation.query.filter_by(id=id).delete()
		db.session.commit()
		return jsonify(success=True), 200
	except exc.SQLAlchemyError as e:
		print("exception deleting reservation: ", e, flush=True)
		db.session.rollback()
		return jsonify(success=False), 400

@main.route('/getreservations/<date>', methods=['GET'])
def getreservations(date):
	try:
		print("reservation date: ", date)
		reservations = Reservation.query.filter_by(resDate=date).all()
		resList = []
		for r in reservations:
			e = {"id": r.id, "date": r.resDate, "time": r.resTime, "duration": r.duration, "pilot": r.pilot, "note": r.note}
			resList.append(e)
		print(resList)

		jsondata = jsonify(results = resList)
		return jsondata

	except exc.SQLAlchemyError as e:
		print("exception getting reservations: ", e, flush=True)
		return jsonify(success=False), 400


@main.route("/manage")
def manage():
	return render_template('manage.html')
