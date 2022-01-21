import datetime
from distutils.command.config import config
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)





class User(db.Model):
    #This line is to give the table a different name other than that of lowercase version of class-name
    # __tablename__ = "table-name"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255))
    #first optional argument is a column name that we can give

    posts = db.relationship('Post',backref='user',lazy='dynamic')

    def __init__(self, username):
        self.username = username
    
    def __repr__(self):
        return "<User '{}'".format(self.username)
    
class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime(), default=datetime.datetime.now)

    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic'
    )


    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('posts',lazy='dynamic')
    )
    def __init__(self, title):
        self.title = title
    
    def __repr__(self):
        return "<Post '{}'>".format(self.title)    
    

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment '{}'".format(self.text[:15])

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, title):
        self.title = title
    
    def __repr__(self):
        return "<Tag '{}'>".format(self.title)

@app.route('/')
def home():
    result = '<h1>Tables</h1><br><ul>'
    for table in db.metadata.tables.items():
        result += '<li> %s </li>' % str(table)
    result += "</ul>"
    return result

if __name__ == "__main__":
    app.run()