from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ARRAY
from flask_migrate import Migrate

# Config

db = SQLAlchemy()


def setup_db(app, test=False):
    if test:
        app.config.from_object('test_config')
        db.app = app
        db.init_app(app)
        db.drop_all()
        db.create_all()
    else:
        app.config.from_object('config')
        db.app = app
        db.init_app(app)
        migrate = Migrate(app, db)

# Models

class Players(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    nationality = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'nationality': self.nationality,
            'team': self.team.name
        }

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'nationality': self.nationality,
            'rating': self.rating,
            'team': self.team.name
        }

    # def __repr__(self):
    #         return


class Teams(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    nation = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    players = db.relationship('Players', backref='team', lazy='joined',
        cascade='all, delete-orphan')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'nation': self.nation,
            'players': [player.short() for player in self.players]
        }

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'nation': self.nation,
            'rating': self.rating,
            'players': [player.long() for player in self.players]
        }

    # def __repr__(self):
    #         return
