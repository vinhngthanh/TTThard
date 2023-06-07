from datetime import datetime
import time
from flask import Flask, flash, jsonify, render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user

from ..models import Player, Match
from . import main
from .. import db
from .forms import AddPlayerForm, LoginForm, DeletePlayerForm

@main.route("/")
def home():
    return render_template('home.html')

@main.route("/tic-tac-toe")
def tictactoe():
    if current_user.is_authenticated:
        return render_template("tic_tac_toe.html")
    else:
        flash('You must be logged in!', 'danger')
        return redirect(url_for('main.login'))

@main.route('/update_match', methods=['GET', 'POST'])
@login_required
def update_match():
    status = request.form['status']
    moves = request.form['moves']
    start_time = datetime.strptime(request.form['start_time'], '%a %b %d %Y %H:%M:%S GMT%z (%Z)')
    duration = request.form['duration']
    
    player_id = current_user.id
    match = Match(status=status, moves=moves, start_time=start_time, duration=duration, player_id=player_id)
    db.session.add(match)
    db.session.commit()

    message = {'message': 'Match added successfully'}
    player_profile_url = url_for('main.player_profile',player_id=player_id)

    time.sleep(1)
    return jsonify(message), 200, {'Content-Type': 'application/json', 'Location': player_profile_url}   

@main.route('/players')
def players():
    players = Player.query.all()
    return render_template('players.html', players=players)

@main.route('/player/<int:player_id>')
def player_profile(player_id):
    player = Player.query.get_or_404(player_id)
    return render_template('player_profile.html', player=player)
    
@main.route('/player/new', methods=['GET', 'POST'])
def new_player():
    form = AddPlayerForm()
    if form.validate_on_submit():
        search_email = Player.query.filter_by(email=form.email.data).first()
        search_username = Player.query.filter_by(username=form.username.data).first()
        if search_email is not None or search_username is not None:
            return render_template('new_player.html', form=form)
        player = Player(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(player)
        db.session.commit()
        added = Player.query.filter_by(email=form.email.data).first()
        login_user(added)
        flash('Account Created!', 'success')
        return redirect(url_for('main.player_profile', player_id=player.id))
    return render_template('new_player.html', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        player = Player.query.filter_by(email=form.email.data).first()
        if player is not None and player.verify_password(form.password.data):
            login_user(player)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.player_profile', player_id=player.id))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('main.players'))

@main.route("/delete_player/<int:player_id>", methods = ["GET", "POST"])
def delete_player(player_id):
    form = DeletePlayerForm()
    if(form.validate_on_submit()):
        player = Player.query.filter_by(id=player_id).first()
        if player is not None and player.verify_password(form.password.data) and (player.email == form.email.data):
            db.session.delete(player)
            db.session.commit()
            flash('Account Deleted!', 'success')
            return redirect(url_for('main.players'))
        flash('Wrong Email or Password!', 'danger')
        return redirect(url_for("main.delete_player", player_id = player_id))
    
    return render_template("delete_player.html", form = form, player_id=player_id)