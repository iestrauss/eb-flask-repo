
SQLALCHEMY_DATABASE_URL= "mysql+pymysql://root:password@localhost/new_database"


from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
application.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(application)



##############################################
class ArticleVote(db.Model):
    # object mirrors table 'article_vote'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.fb_id'))  # Sloppy
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    vote_choice_id = db.Column(db.Integer)
    comment = db.Column(db.String(400))

    def __init__(self, user_id, article_id, vote_choice_id, comment):
        self.user_id = user_id
        self.article_id = article_id
        self.vote_choice_id = vote_choice_id
        self.comment = comment


article_id = "article_id_1"
user_id = "user_id_1"
vote_choice_id = "vote_choice_id_1"
comments = "comments_1"
av_obj = ArticleVote(user_id, article_id, vote_choice_id, comments)

article_id = 446

db.session.add(av_obj)
db.session.commit()

print("Article was inserted")
