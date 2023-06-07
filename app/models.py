from flask_login import UserMixin
from datetime import timedelta
from . import db
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class Player(db.Model, UserMixin):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    match = db.relationship('Match', backref='player', lazy='select', cascade='all, delete-orphan')

    def __repr__(self):
        return f"{self.username}"
    
    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def num_matches_played(self):
        return len(self.match)
    
    def num_matches_win(self):
        return len([w for w in self.match if w.status == "Win"])
    
    def num_matches_loss(self):
        return len([l for l in self.match if l.status == "Loss"])
    
    def num_matches_draw(self):
        return len([d for d in self.match if d.status == "Draw"])

class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False)
    moves = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Float, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)

    def __repr__(self):
        return f"{self.status} in {self.moves} moves"
    
@login_manager.user_loader
def load_player(player_id):
    return Player.query.get(int(player_id))