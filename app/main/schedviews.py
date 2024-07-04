#!/usr/bin/env python3.9

"""handle schedule views"""
import json
import datetime
import os
from base64 import b64decode
from flask_wtf import FlaskForm
from flask import render_template, redirect, url_for, request, \
	make_response, jsonify, Response, stream_with_context
# from flask_cors import CORS, cross_origin
from sqlalchemy import exc
from datetime import date, timedelta
from .. import db
from . import main, logger
from wtforms import SubmitField

blkDuration = 20

class Account(db.Model):
	__tablename__ = 'account'
	id = db.Column(db.Integer, unique=True, index=True, autoincrement=True, primary_key=True)
	name = db.Column(db.String(32))
	pw = db.Column(db.String(32))
	title = db.Column(db.String(32))

	def __repr__(self):
		# return '<Account %s>' % self.name
		return "<Account for {}>".format(self.title)

class Reservation(db.Model):
	__tablename__ = 'reservation'
	id = db.Column(db.Integer, unique=True, index=True, autoincrement=True, primary_key=True)
	acctId = db.Column(db.Integer)
	resDate = db.Column(db.Date)
	resTime = db.Column(db.Integer)
	firstName = db.Column(db.String(31))
	lastName = db.Column(db.String(31))
	phone = db.Column(db.String(16))
	email = db.Column(db.String(64))

	def __repr__(self):
		# return '<Reservation %s>' % self.firstName
		return "<Reservation for {} {}>".format(self.firstName, self.lastName)

class Block(db.Model):
	__tablename__ = 'block'
	id = db.Column(db.Integer, unique=True, index=True, autoincrement=True, primary_key=True)
	acctId = db.Column(db.Integer)
	blkDate = db.Column(db.Date)
	duration = db.Column(db.Integer)
	startTime = db.Column(db.Integer)
	numBlocks = db.Column(db.Integer)

	def __repr__(self):
		# return '<Block %>' % self.pilot
		return "<Block {}, {}:{}>".format(self.blkDate, self.startTime/60,self.startTime%60)

class ScheduleForm(FlaskForm):
	submit = SubmitField('Submit')


# @main.route("/")
# def index():
# 	print("print: index", flush=True)
# 	logger.info("logger: index")
# 	logger.debug("debug: index")
# 	return render_template('index.html')


@main.route("/")
@main.route("/<acct>")
def index(acct=None):
	print("print: index", acct, flush=True)
	logger.info("logger: index")
	logger.debug("debug: index")
	resp = None

	if acct == None:
		resp = make_response(render_template('noaccount.html'))

	else:
		account = Account.query.filter_by(name=acct).first()
		resp = make_response(render_template('index.html', acct=account.name, title=account.title))

	resp.set_cookie('Account', acct)
	return resp

@main.route("/schedule")
def schedule():
	acctName = request.cookies.get("Account")
	account = Account.query.filter_by(name=acctName).first()
	form = ScheduleForm
	blocks = Block.query.filter(Block.blkDate >= date.today(), Block.acctId == account.id).order_by(Block.blkDate).all()
	reservations = Reservation.query.filter(Block.blkDate >= date.today()).order_by(Reservation.resDate, Reservation.resTime).all()

	return render_template('schedule.html', form=form, blocks=blocks, reservations=reservations, acct=account.name, title=account.title)

@main.route("/change")
def change():
	acctName = request.cookies.get("Account")
	account = Account.query.filter_by(name=acctName).first()
	form = ScheduleForm
	blocks = Block.query.filter_by(acctId=account.id).order_by(Block.blkDate).all()
	reservations = Reservation.query.filter_by(acctId=account.id).order_by(Reservation.resDate, Reservation.resTime).all()
	print(reservations)

	return render_template('change.html', form=form, blocks=blocks, reservations=reservations, acct=account.name, title=account.title)


@main.route('/addreservation', methods=['POST'])
def addreservation():
	"""add reservation"""
	try:
		print("add reservation")
		acctName = request.cookies.get("Account")
		account = Account.query.filter_by(name=acctName).first()
		acctId = account.id
		date = request.json.get('resdate')
		time = request.json.get('restime')
		first = request.json.get('first')
		last = request.json.get('last')
		phone = request.json.get('phone')
		res = Reservation()

		res.acctId = acctId
		res.resDate = date
		res.resTime = time
		res.firstName = first
		res.lastName = last
		res.phone = phone
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
		acctName = request.cookies.get("Account")
		account = Account.query.filter_by(name=acctName).first()
		acctId = account.id
		id = request.json.get('id')
		date = request.json.get('resdate')
		time = request.json.get('restime')
		phone = request.json.get('phone')
		first = request.json.get('first')
		last = request.json.get('last')
		res = Reservation.query.filter_by(id=id).first()
		res.acctId = acctId
		res.resDate = date
		res.resTime = time
		res.firstName = first
		res.lastName = last
		res.phone = phone
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
		acctName = request.cookies.get("Account")
		account = Account.query.filter_by(name=acctName).first()
		acctId = account.id
		reservations = Reservation.query.filter_by(resDate=date, acctId=acctId).all()
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


@main.route("/admin")
@main.route("/admin/<acct>")
def admin(acct=None):
	form = ScheduleForm

	# return render_template('admin.html', form=form)

	resp = None
	nameCookie = "none"

	if acct == None:
		resp = make_response(render_template('noaccount.html'))

	else:
		nameCookie = acct
		account = Account.query.filter_by(name=acct).first()
		resp = make_response(render_template('admin.html', acct=account.name, title=account.title))

	resp.set_cookie('Account', nameCookie, path="/", max_age=timedelta(days=400))
	print("admin - set acct cookie", nameCookie)
	return resp


@main.route("/showlist")
def showlist():
	acctName = request.cookies.get("Account")
	account = Account.query.filter_by(name=acctName).first()
	print(acctName, account)
	form = ScheduleForm
	blocks = Block.query.filter_by(acctId=account.id).order_by(Block.blkDate).all()
	reservations = Reservation.query.filter_by(acctId=account.id).order_by(Reservation.resDate, Reservation.resTime).all()

	return render_template('showlist.html', form=form, blocks=blocks, reservations=reservations, acct=account.name, title=account.title)

@main.route("/blocks")
def blocks():
	acctName = request.cookies.get("Account")
	account = Account.query.filter_by(name=acctName).first()
	form = ScheduleForm
	blocks = Block.query.filter_by(acctId=account.id).order_by(Block.blkDate).all()

	return render_template('setblock.html', form=form, blocks=blocks, acct=account.name, title=account.title)
	
@main.route("/addblock", methods=['POST'])
def addblock():
	try:
		print("add block")
		acctName = request.cookies.get("Account")
		account = Account.query.filter_by(name=acctName).first()
		acctId = account.id
		date = request.json.get('date')
		time = request.json.get('time')
		count = request.json.get('count')
		blk = Block()

		blk.acctId = acctId
		blk.blkDate = date
		blk.resTime = date
		blk.duration = blkDuration
		blk.startTime = time
		blk.numBlocks = count
		print(blk)
		db.session.add(blk)
		db.session.commit()
		return jsonify(success=True, id=blk.id), 200

	except exc.SQLAlchemyError as e:
		print("exception adding block: ", e, flush=True)
		db.session.rollback()
		return jsonify(success=False), 400
	
@main.route("/delblock", methods=['POST'])
def delblock():
	try:
		id = request.json.get('id')
		print("del block", id)
		Block.query.filter_by(id=id).delete()
		db.session.commit()
		return jsonify(success=True), 200
	except exc.SQLAlchemyError as e:
		print("exception deleting block: ", e, flush=True)
		db.session.rollback()
		return jsonify(success=False), 400
