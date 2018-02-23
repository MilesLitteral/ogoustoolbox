# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

'''# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())
'''

# Define a User model
'''class User(db.Model):

    __tablename__ = 'auth_user'

    # User Name
    name    = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(192),  nullable=False)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name     = name
        self.email    = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)     
'''
# Define a Tool Model
class hand_tool(db.Model):

    __tablename__ = 'hand_tool'
    tool_name  = db.Column(db.String(10),primary_key=True,  nullable=False)
    tool_price = db.Column(db.Integer,  nullable=False, unique=True)

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.tool_name     = tool_name
        self.tool_price    = tool_price

    def __repr__(self):
        return '<User %r>' % (self.name)     