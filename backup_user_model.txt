import os

from database import Base
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_security import Security, SQLAlchemySessionUserDatastore, auth_required, hash_password
from flask_security.models import fsqla_v2 as fsqla

db = SQLAlchemy()
fsqla.FsModels.set_db_info(db)


roles_user = db.Table('roles_users',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('role_id', db.Integer, db.ForeignKey(role.id)))


friendship = db.Table('friendships',
  db.Column('friend_a_id', db.Integer, db.ForeignKey('user.id'),
                                          primary_key=True),
  db.Column('friend_b_id', db.Integer, db.ForeignKey('user.id'),
                                          primary_key=True))

class User(db.Model, fsqla.FsUserMixin):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, unique=True, nullable=False)
  name = db.Column(db.String, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  bio = db.Column(db.String(150))
  active = db.Column(db.Boolean)
  confirmed_at = db.Column(db.DateTime)
  roles = db.relationship('Roles', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
  friends = relationship('User', secondary=friendship,
                          primaryjoin=id==friendship.c.friend_a_id,
                          secondaryjoin=id==friendship.c.friend_b_id,
                          backref=db.backref('users', lazy='dynamic'))

  def __repr__(self):
      return f'User(id={self.id}, email="{self.email}", name="{self.name}")'

friendship_union = select([
                            friendship.c.friend_a_id,
                            friendship.c.friend_b_id
                            ]).union(
                                select([
                                        friendship.c.friend_b_id,
                                        friendship.c.friend_a_id]
                                )
                                ).alias()
User.all_friends = relationship('User', 
                          secondary=friendship_union,
                          primaryjoin=User.id==friendship_union.c.friend_a_id,
                          secondaryjoin=User.id==friendship_union.c.friend_b_id,
                          viewonly=True)

class Role(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40))
  description: db.Column(db.String(255))

user_datastore = SQLAlchemySessionUserDatastore(db, User, Role)
security = Security(app, user_datastore)


