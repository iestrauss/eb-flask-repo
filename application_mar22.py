from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime

#    DATE      WHO     DESCRIPTION
# april 29
# ########## ####### ###################################################################################
from flask import Flask, jsonify, request, render_template

application = Flask(__name__)
application.config['SQLALCHEMY_ECHO'] = True
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:iski8iski8A@database-2.cv15axugkvps.us-east-2.rds.amazonaws.com/bear'
application.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(application)

print("tiger print one", db)

##############################################
class Permission(db.Model):
    # object mirrors table 'permission'
    # todo: actually design and implement a permission strategy
    id = db.Column('id', db.Integer, primary_key=True)
    permission = db.Column(db.String(100))

    # missing field 'created_at'

    def __init__(self, permission):
        self.permission = permission


##############################################

class Config(object):
    # ...
    POSTS_PER_PAGE = 3


##############################################
class User(db.Model):
    # object mirrors table 'user'
    # todo: retrieve actual users who can be permissioned

    id = db.Column('id', db.Integer, primary_key=True)
    fb_id = db.Column('fb_id', db.String(100))
    fb_pic = db.Column('fb_pic', db.String(400))

    name = db.Column(db.String(100))
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))
    # missing field 'created_at'
    user_list = []

    def __init__(self, fb_id, fb_pic, name, permission_id):
        self.fb_id = fb_id
        self.fb_pic = fb_pic
        self.name = name
        self.permission_id = permission_id

    @classmethod
    def getUserList(cls):
        # return the list of users objects
        if not cls.user_list:
            print('Going to database to retrieve Users:')
            cls.user_list = User.query.all()
            for item in cls.user_list:
                print("id: " + str(item.id) + " name: " + item.name + " permission_id: " + str(item.permission_id))

        return cls.user_list


##############################################
class Article(db.Model):
    # object mirrors table 'article'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    url = db.Column(db.String(400))
    image_url = db.Column(db.String(400))
    snippet = db.Column(db.String(1000))
    date_upload = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, title, url, image_url, snippet):
        self.title = title
        self.url = url
        self.image_url = image_url
        self.snippet = snippet


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


##############################################
class VoteChoice(db.Model):
    # object mirrors table 'vote_choice' in the database
    id = db.Column('id', db.Integer, primary_key=True)
    choice = db.Column(db.String(100))
    color = db.Column(db.String(20))
    status = db.Column(db.Integer)  # active is true if non-zero

    # this is a class variable
    vote_choice_list = []  # objects representing vote choices consisting: id, text, color
    vote_choice_color = {}  # provide key to retrieve color
    vote_choice_text = {}  # provide key to retrieve choice text

    def __init__(self, choice, color, status):
        self.choice = name
        self.color = color
        self.status = status

    @classmethod
    def getVoteChoiceList(cls):
        # return the list of vote choices where status is active ( none 0 )
        if not cls.vote_choice_list:
            # if the vote_choice_list has not been intialized we retrieve it here
            # this keeps the prog from repeating the same query
            print('Going to database to retrieve VoteChoice:')
            cls.vote_choice_list = VoteChoice.query.filter(VoteChoice.status > 0).all()
            for item in cls.vote_choice_list:
                print('   id: ' + str(item.id) + ' color: ' + item.color + ' choice:' + item.choice)
                cls.vote_choice_color[item.id] = item.color
                cls.vote_choice_text[item.id] = item.choice

        return cls.vote_choice_list

    @classmethod
    def getVoteChoiceById(id):
        if not cls.vote_choice_list:
            cls.getVoteChoiceList()
        return cls.vote_choice_text[id]

    @classmethod
    def getVoteColorById(id):
        if not cls.vote_choice_list:
            cls.getVoteChoiceList()
        return cls.vote_choice_color[id]



#############################################


from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter, get_page_args

mod = Blueprint('home_data', __name__)


@application.route('/')
def home():
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page
    # home_data = Article.query.order_by(Article.title.desc())
    home_data = Article.query.order_by(Article.date_upload.desc())
    # home_data = Article.query.order_by(Article.desc().title)
    home_data_for_render = home_data.limit(per_page).offset(offset)

    print("article dicts:", home_data_for_render)

    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, search=search, record_name='home_data', per_page=per_page, offset=offset,
                            total=home_data.count(), css_framework='bootstrap3')

    return render_template('home.html', home_data=home_data_for_render, pagination=pagination, )


##############################################
@application.route('/results/<int:id>')
def results(id):
    rate = 0  # either 0 or num/total
    updated_details = []
    article_list_of_one = Article.query.filter_by(id=id)
    a_obj = article_list_of_one[0]
    avs_obj = retrieve_article_vote_summary(a_obj.id)  # vote_summary is a list of [tuples('True', numOfTrue), etc]
    total_votes = avs_obj.getTotalVotes()
    vote_choices = []
    vote_choice_list = VoteChoice.getVoteChoiceList()
    for item in vote_choice_list:  # looping over VoteChoice objects
        num = avs_obj.getVoteCount(item.choice)
        if total_votes > 0:  # protecting against no votes
            rate = num / total_votes
        vote_choices.append([item.choice, item.color, num, rate * 100, total_votes])

    details = avs_obj.getVoteDetails()  # 10/02 - retrieve array of tuples [(user, VoteChoice, Comments)]
    print("Inside results(" + str(id) + "):")
    details_count = 0
    for detail in details:
        updated_details = [(user, VoteChoice, Comments, User.query.filter_by(name=user).first().fb_pic)
                           for (user, VoteChoice, Comments) in details]
        # print("    " + str(details_count) + ": " + details[0] + " " + details[1] + " " + details[2])
        # details_count += 1

    return render_template('results.html', title=a_obj.title, id=id,
                           image_url=a_obj.image_url, url=a_obj.url,
                           vote_choices=vote_choices, home_data=Article.query.all(),
                           vote_details=updated_details)


##############################################
@application.route('/user/', methods=['GET', 'POST'])
def user():
    global user_id
    # calls the page to allow user to change the user
    # this is for testing only as we wouldn't want in production
    print("inside user method")
    user_list = User.getUserList()
    my_list = []
    for item in user_list:
        my_list.append((item.id, item.name, item.permission_id, item.fb_pic))

    print(user_id)
    print(user_list)
    return render_template('/user.html', user_id=user_id, user_list=my_list)


@application.route('/change_user', methods=['GET', 'POST'])
def change_user():
    global user_id
    # action as set int user.html page
    if request.method == 'POST':
        if (user_id != int(request.form['options'])):
            user_id = int(request.form['options'])
            print("user_id change to: " + str(user_id))
        else:
            print("user_id did not change still : " + str(user_id))
    return render_template('/enterdata.html')


##############################################
@application.route('/enterdata/', methods=['GET', 'POST'])
def enterdata():
    print("enterdata")
    return render_template('/enterdata.html')


##############################################
@application.route('/commenttest/', methods=['GET', 'POST'])
def commenttest():
    print("commenttest")
    return render_template('/commenttest.html')

##############################################
@application.route('/privacy/')
def privacy():
    return render_template('privacypolicy.html')

##############################################
@application.route('/factcheckclass/')
def factcheckclass():
    return render_template('factcheckclass.html')


##############################################
@application.route('/factcheckclass1/')
def factcheckclass1():
    return render_template('factcheckclass1.html')


##############################################
@application.route('/factcheckclass3/')
def factcheckclass3():
    return render_template('factcheckclass3.html')


##############################################
@application.route('/factcheckclass4/')
def factcheckclass4():
    return render_template('factcheckclass4.html')


##############################################
@application.route('/factcheckclass5/')
def factcheckclass5():
    return render_template('factcheckclass5.html')

##############################################
@application.route('/chat/')
def chat():
    return render_template('chat.html')

##############################################
@application.route('/take_test', methods=['GET', 'POST'])
def take_test():
    if request.method == 'POST' or request.method == 'GET':
        if not request.form['popquiz']:
            flash('Please enter all the fields', 'error')
        else:
            print("you took the test")
            message = {'greeting': "hope you chose bikes"}
            print(message)
            return jsonify(message)


##############################################
@application.route('/bootstrap', methods=['GET', 'POST'])
# // this takes the article from the extension and inserts it into the database
def bootstrap():
    posted = 1
    print ("bootstrap")
    if request.method == 'POST':
        if not request.form['title'] or not request.form['url'] or not request.form['image_url'] or not request.form['snippet']:
            flash('Please enter all the fields', 'error')
        else:

            rurl = request.form['url']
            print("here comes rurl")
            print(rurl)
            import urllib.parse as url_parse
            url = rurl
            news_link = url_parse.unquote(url).split("?u=")[1].split("?fbclid")[0]
            print("here comes the news_link")
            print(news_link)
            article = Article(request.form['title'], news_link, request.form['image_url'],
                               request.form['snippet'])

            db.session.add(article)
            try:
                db.session.commit()
            except exc.SQLAlchemyError:
               flash('Article url already exists, failed to post new article')
               posted = 0
               #return render_template('/error.html', article_url=article.url)

            # article_list = Article.query.filter_by(image_url=article.image_url)
            # article_list = Article.query.filter_by(url=article.url)
            article_list = Article.query.filter_by(title=article.title)

            if posted == 1:
                flash('Record was successfully added')
            else:
                db.session.rollback()
                # article_list = Article.query.filter_by(image_url=article.image_url)
                # article_list = Article.query.filter_by(url=article.url)
                article_list = Article.query.filter_by(title=article.title)

                article=article_list[0]

            print ("article.id=" + str(article.id))
            import json
            return json.dumps(article.id)

    else:
        # print("article.id=" + str(article.id))
        urlNumber = str(article.id)

        message = {'greeting':urlNumber}
        return jsonify(message)  # serialize and use JSON headers


##############################################


@application.route('/fbuser', methods=['POST'])
def fbuser():
    print("this is version 1.1")
    # global user_id
    # request.form is the data from facebook, includes userID, picture, name
    person = request.form
    print("FBUSER", person)
    print("ID", person.get("userID"))
    # user = person.get("userID")
    # we check the db for the user, if they exist we are done

    maybe_existing_user = User.query.filter_by(fb_id=person.get("userID")).first()

    # check if user is in db, if so, set ID...

    if(maybe_existing_user):
        fb_user_id = maybe_existing_user.id
        return "exists"
    else:
        new_user = User(int(person.get("userID")), person.get("picture"), person.get("name"), 5)
        db.session.add(new_user)
        try:
            db.session.commit()
            print("success sql")
            now_existing_user = db.session.query(User).filter_by(fb_id=int(person.get("userID"))).first()
            # if(now_existing_user is None) Error
            fb_user_id = now_existing_user.id
            print("here comes the now_existing_user.id I just inserted")
            print(now_existing_user.id)
            return "created"
        except exc.SQLAlchemyError as e:
            print(e)
            flash('Article url already exists, failed to post new user')
            print("sql fail")
            return "failed to create"


##############################################
@application.route('/votefor/<int:article_id>', methods=['GET', 'POST'])
def votefor(article_id):
    print("votefor")
    # global article
    article_list_of_one = Article.query.filter_by(id=article_id)
    article = article_list_of_one[0]
    print("here's the id from votefor local hopefully article.id version", article.id)
    posted = 1
    # global article

    vote_choices = VoteChoice.getVoteChoiceList()

    return render_template('/votefor.html', article_id=article.id,
                           article_title=article.title, image_url=article.image_url, article_url=article.url,
                           vote_choices=vote_choices
                           )


##############################################
class ArticleVoteSummary():
    # todo: add reset method
    # This object keeps the count of votes for an Article
    # 09/29 - adding an array of vote comments

    def __init__(self, article_id):
        self.article_id = article_id
        self.choice_count = {}  # count by textual choice
        self.choice_id = {}
        self.vote_comments = []  # list to which comments are appended
        self.vote_details = []  # list of tuples (user, vote_choice, comment)
        choice_list = VoteChoice.getVoteChoiceList()
        for item in choice_list:
            self.choice_id[str(item.id)] = item.choice
        for item in choice_list:
            self.choice_count[item.choice] = 0
        self.total_votes = 0

    def addVote(self, choice):
        self.choice_count[choice] = self.choice_count[choice] + 1
        self.total_votes = self.total_votes + 1

    def appendComment(self, comment):
        # 09/29 - append commentions to vote_comments
        self.vote_comments.append(comment)

    def appendDetail(self, detail):  # detail is a tuple of (user, vote_choice, comment)
        self.vote_details.append(detail)

    def getVoteCount(self, choice):
        return self.choice_count[choice]

    def getVoteText(self, choice_id):
        return self.choice_id[str(choice_id)]

    def dump(self):
        keys = self.choice_count.keys()
        for key in keys:
            print(key + ': ' + str(self.choice_count[key]))

    def getVotes(self):
        ret_v = []  # return a list of tuple(choice, count)

        keys = self.choice_count.keys()
        for key in keys:
            t = (key, self.choice_count[key])
            ret_v.append(t)

        return ret_v

    def getTotalVotes(self):
        return self.total_votes

    def getVoteComments(self):
        # 09/29 - return a list of comments
        return (self.vote_comments)

    def getVoteDetails(self):
        # 10/02 - return [(user, vote_choice, comments),...,(user, vote_choice, comments)]
        return (self.vote_details)


##############################################
def retrieve_article_vote_summary(article_id):
    avs_obj = ArticleVoteSummary(article_id)
    #    article_vote_list = ArticleVote.query.filter_by(article_id=article_id)
    print("article_id in ravs(): ", str(article_id))
    article_vote_list = db.session.query(ArticleVote, User).filter(ArticleVote.article_id == article_id).filter(
        ArticleVote.user_id == User.fb_id).all()
    print("before for item in article_vote_list")
    for item in article_vote_list:
        print("before text")
        text = avs_obj.getVoteText(item[0].vote_choice_id)
        print("before avs_obj.addVote(text)")
        avs_obj.addVote(text)
        print("article text: ", text)
        # avs_obj.appendComment(item.comment) # 09/27 - added to show comments in results page
        avs_obj.appendDetail((item[1].name, text, item[0].comment))  # 09/27 - added to show comments in results page

    return avs_obj


##############################################
@application.route('/insert_vote', methods=['GET', 'POST'])
def insert_vote():
    posted = 1
    # global user_id
    # global article, user_id
    # print ("insert_vote", "this should be the facebook user id", user_id)
    if request.method == 'POST' or request.method == 'GET':
        if not request.form['options']:
            flash('Please enter all the fields', 'error')
        else:
            rate = 0  # rate of votes protection against no votes
            vote_choice_id = int(request.form['options'])
            comments = request.form['comments']

            print("here comes the new stuff")

            article_id = int(request.form['article_id'])

            print(str(article_id), "article_id")

            print(request.form)

            user_id = request.form['user_id']
            print("this is the try bit")
            print(user_id)
            fb_user_id = int(user_id)
            # user_id = 1
            av_obj = ArticleVote(fb_user_id, article_id, vote_choice_id, comments)
            db.session.add(av_obj)
            try:
                print("db.session.commit before")
                db.session.commit()
                print("db.session.commit after")
            except exc.SQLAlchemyError as e:
                print("this is about to be %s", e)
                print("user has already voted before")
                flash('User has already voted on this article.')
                posted = 0

            if posted == 1:
                print("posted ==1 after")
                flash('Record was successfully added')
            else:
                print("right before rollback")
                db.session.rollback()

            a_obj = Article.query.filter_by(id=article_id).first()
            # this is the current global article
            avs_obj = retrieve_article_vote_summary(
                a_obj.id)  # vote_summary is a list of [tuples('True', numOfTrue), etc]
            total_votes = avs_obj.getTotalVotes()
            print("here's the object ", a_obj.id)
            print("this is the total votes ", total_votes)

            vote_choice_list = VoteChoice.getVoteChoiceList()
            vote_choices = []
            for item in vote_choice_list:  # looping over VoteChoice objects
                num = avs_obj.getVoteCount(item.choice)
                if total_votes > 0:
                    rate = num / total_votes
                vote_choices.append([item.choice, item.color, num, rate * 100, total_votes])

            print("a_obj", a_obj)
            details = avs_obj.getVoteDetails()  # 10/02 - retrieve array of tuples [(user, VoteChoice, Comments)]
            print("details", details)
            print("Inside results(" + str(id) + "):")
            print("tigers in the forest")
            # print(article.id)
            details_count = 0
            for detail in details:
                print(detail)
                # print("    " + str(details_count) + ": " + details[0] + " " + details[1] + " " + details[2])
                details_count += 1

            return redirect('/results/' + str(a_obj.id))

        # return render_template('/results.html', title=a_obj.title,
        #                            image_url=a_obj.image_url,
        #                            vote_choices=vote_choices, vote_details=details)


##############################################

if __name__ == '__main__':
    db.create_all()
    application.run(host="0.0.0.0", debug=True, ssl_context=("example.com+2.pem", "example.com+2-key.pem"))
