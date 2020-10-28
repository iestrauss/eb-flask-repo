from flask import Flask, request, flash, url_for, redirect, render_template
from flask import session as flask_session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, func, desc
from datetime import datetime
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_before_login

#    DATE      WHO     DESCRIPTION
# april 29
# ########## ####### ###################################################################################
from flask import Flask, jsonify, request, render_template

application = Flask(__name__)
application.config['SQLALCHEMY_ECHO'] = True
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:iski8iski8A@database-2.cv15axugkvps.us-east-2.rds.amazonaws.com/bear'
application.config['SECRET_KEY'] = "random string"
application.config["FACEBOOK_OAUTH_CLIENT_ID"] = '1560520617436290'
application.config["FACEBOOK_OAUTH_CLIENT_SECRET"] = '0a41f3b2a58fc6d27f3ae9d6b8570fea'
application.config["TWITTER_OAUTH_CLIENT_KEY"] = 'vTJtz4tMVHOlk3PEgVTQAlQBi'
application.config["TWITTER_OAUTH_CLIENT_SECRET"] = 'pHbL1GtgbC0hCCDs1qXG4H8mbr4pgjldmZH9Rybt8vVWh9Yrw8'
application.config["GOOGLE_OAUTH_CLIENT_ID"] = '999488574192-i9rpq3mvjb4putke6j8a13098f74ff9k.apps.googleusercontent.com'
application.config["GOOGLE_OAUTH_CLIENT_SECRET"] = 'qjoGqzwuHTGWOY1ptb4mRmPt'

google_bp = make_google_blueprint(scope=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"])
application.register_blueprint(google_bp, url_prefix="/login")

twitter_bp = make_twitter_blueprint()
application.register_blueprint(twitter_bp, url_prefix="/login")

facebook_bp = make_facebook_blueprint()
application.register_blueprint(facebook_bp, url_prefix="/login")

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
    auth_provider = db.Column(db.String(100))
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))
    # missing field 'created_at'
    user_list = []

    def __init__(self, fb_id, fb_pic, name, permission_id, auth_provider):
        self.fb_id = fb_id
        self.fb_pic = fb_pic
        self.name = name
        self.permission_id = permission_id
        self.auth_provider = auth_provider

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
    hint = db.Column(db.String(100))

    # this is a class variable
    vote_choice_list = []  # objects representing vote choices consisting: id, text, color
    vote_choice_color = {}  # provide key to retrieve color
    vote_choice_text = {}  # provide key to retrieve choice text
    vote_choice_hint = {}

    def __init__(self, choice, color, status, hint):
        self.choice = name
        self.color = color
        self.status = status
        self.hint = hint

    @classmethod
    def getVoteChoiceList(cls):
        # return the list of vote choices where status is active ( none 0 )
        if not cls.vote_choice_list:
            # if the vote_choice_list has not been intialized we retrieve it here
            # this keeps the prog from repeating the same query
            print('Going to database to retrieve VoteChoice:')
            cls.vote_choice_list = VoteChoice.query.filter(VoteChoice.status > 0).all()
            for item in cls.vote_choice_list:
                print('   id: ' + str(item.id) + ' color: ' + item.color + ' choice:' + item.choice + ' hint:' +
                      item.hint)
                cls.vote_choice_color[item.id] = item.color
                cls.vote_choice_text[item.id] = item.choice
                cls.vote_choice_hint[item.id] = item.hint

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

    @classmethod
    def getVoteHintById(id):
        if not cls.vote_choice_list:
            cls.getVoteChoiceList()
        return cls.vote_choice_hint[id]


#############################################


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(140))
    article_id = db.Column(db.Integer)
    vote_id = db.Column(db.Integer)
    text = db.Column(db.Text())
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship(
        'Comment', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')

    def add_reply(self, fb_user_id, article_id, text):
        return Comment(user_id=fb_user_id, article_id=article_id, text=text, parent=self)

#############################################


from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter, get_page_args

mod = Blueprint('home_data', __name__)


@application.route('/')
def home():
    next_url = flask_session.pop("next_url", "")
    if next_url:
      return redirect(next_url)

    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page
    search = False
    q = request.args.get('q')
    sort_by = request.args.get('sort_by')
    if sort_by and sort_by == 'recent':
        home_data = Article.query.order_by(Article.date_upload.desc())
    else:
        sq_votes = db.session.query(ArticleVote.article_id, func.count('*').label('vote_count')).group_by(ArticleVote.article_id).subquery()
        home_data = db.session.query(
            Article.id, Article.title, Article.url, Article.image_url, Article.snippet, Article.date_upload, sq_votes.c.vote_count
        ).outerjoin(sq_votes, Article.id==sq_votes.c.article_id).order_by(desc('vote_count'))

    if q:
        home_data = Article.query.filter(Article.title.like('%' + q + '%')).order_by(Article.date_upload.desc())

    home_data_for_render = home_data.limit(per_page).offset(offset)

    print("article dicts:", home_data_for_render)


    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, search=search, record_name='home_data', per_page=per_page, offset=offset,
                            total=home_data.count(), css_framework='bootstrap3')

    return render_template('home.html', home_data=home_data_for_render, pagination=pagination, query_param=q, sort_by=sort_by)


##############################################
def retrieve_pub_vote_summary(publication):
    # new counting code
    import sqlalchemy as sa

    # for 1 votes
    q = (db.session.query(Article.snippet, sa.func.count(ArticleVote.id))
         .join(ArticleVote, Article.id == ArticleVote.article_id)
         .filter(Article.snippet == publication)
         .filter(ArticleVote.vote_choice_id == 1)
         .group_by(Article.snippet))
    for snippet, count in q:
        print(snippet, count)
        onevotes = count
        print("onevotes", onevotes)
    if 'onevotes' in locals():
        print("onevotes in locals")
    else:
        onevotes = 0

    # for 2 votes
    q = (db.session.query(Article.snippet, sa.func.count(ArticleVote.id))
         .join(ArticleVote, Article.id == ArticleVote.article_id)
         .filter(Article.snippet == publication)
         .filter(ArticleVote.vote_choice_id == 2)
         .group_by(Article.snippet))
    for snippet, count in q:
        print(snippet, count)
        twovotes = count
        print("twovotes", twovotes)
    if 'twovotes' in locals():
        print("twoevotes in locals")
    else:
        print("twovotes not in locals")
        twovotes = 0

    # for 3 votes
    q = (db.session.query(Article.snippet, sa.func.count(ArticleVote.id))
         .join(ArticleVote, Article.id == ArticleVote.article_id)
         .filter(Article.snippet == publication)
         .filter(ArticleVote.vote_choice_id == 3)
         .group_by(Article.snippet))
    for snippet, count in q:
        print(snippet, count)
        threevotes = count
        print("threevotes", threevotes)
    if 'threevotes' in locals():
        print("threevotes in locals")
    else:
        print("threevote not in locals")
        threevotes = 0

    # for 4 votes
    q = (db.session.query(Article.snippet, sa.func.count(ArticleVote.id))
         .join(ArticleVote, Article.id == ArticleVote.article_id)
         .filter(Article.snippet == publication)
         .filter(ArticleVote.vote_choice_id == 4)
         .group_by(Article.snippet))
    for snippet, count in q:
        print(snippet, count)
        fourvotes = count
        print("fourvotes", fourvotes)
    if 'fourvotes' in locals():
        print("fourvotes in locals")
    else:
        fourvotes = 0

    # for 5 votes
    q = (db.session.query(Article.snippet, sa.func.count(ArticleVote.id))
         .join(ArticleVote, Article.id == ArticleVote.article_id)
         .filter(Article.snippet == publication)
         .filter(ArticleVote.vote_choice_id == 5)
         .group_by(Article.snippet))
    for snippet, count in q:
        print(snippet, count)
        fivevotes = count
        print("fivevotes", fivevotes)
    if 'fivevotes' in locals():
        print("fivevotes in locals")
    else:
        fivevotes = 0

    # for 6 votes
    q = (db.session.query(Article.snippet, sa.func.count(ArticleVote.id))
         .join(ArticleVote, Article.id == ArticleVote.article_id)
         .filter(Article.snippet == publication)
         .filter(ArticleVote.vote_choice_id == 6)
         .group_by(Article.snippet))
    for snippet, count in q:
        print(snippet, count)
        sixvotes = count
        print("sixvotes", sixvotes)
    if 'sixvotes' in locals():
        print("sixvotes in locals")
    else:
        sixvotes = 0
    # getting rating

    total = onevotes + twovotes + threevotes + fourvotes + fivevotes
    if total == 0:
        total = 1
    print("total: ", total)

    score = (onevotes + .5 * (twovotes)) / total
    print("score: ", score)
    score_percent = round(score * 100)

    pub_tuple = (onevotes, twovotes, threevotes, fourvotes, fivevotes, sixvotes, total, score,
                             score_percent)
    print("before pub_tuple")
    print(pub_tuple)
    print("after pub_tuple")
    return pub_tuple

def retrieve_article_rating(article_url):
    article = Article.query.filter_by(url=article_url).first()
    if not article:
        return {'total': 0, 'score_percent': 0}

    vote_counts = db.session.query(
        ArticleVote.vote_choice_id, func.count(ArticleVote.vote_choice_id)
    ).filter_by(article_id=article.id).group_by(ArticleVote.vote_choice_id).all()
    votes_dict = dict((x, y) for x, y in vote_counts)
    total = sum(votes_dict.values())
    if total == 0:
        total = 1
    for i in range(1, 7):
        if i not in votes_dict:
            votes_dict[i] = 0
    score = (votes_dict[1] + .5 * (votes_dict[2])) / total

    score_percent = round(score * 100)

    return {'total': total, 'score_percent': score_percent}


##############################################
@application.route('/buttoncolor', methods=['GET', 'POST'])
def buttoncolor():
    print("buttoncolor")
    if request.method == 'POST':
        if not request.form['url']:
            flash('Please enter all the fields', 'error')
        else:
            if 'source' in request.form and request.form['source'] == 'twitter':
                news_link = request.form['url']
                import requests
                final_link = requests.get(news_link)
                print("here comes the final_link.url")
                print(final_link.url)
                # now to get rid of the pesky fb stuff at the end
                import urllib.parse as url_parse
                link3 = url_parse.unquote(final_link.url).split("?")[0]
                # // link 3 is the domain link
                print("here comes link3")
                print(link3)
            elif 'source' in request.form and request.form['source'] == 'google':
                link3 = request.form['url']
            else:
                rurl = request.form['url']
                print("here comes rurl")
                print(rurl)
                import urllib.parse as url_parse
                url = rurl
                news_link = url_parse.unquote(url).split("?u=")[1].split("?fbclid")[0]
                print("here comes the news_link")
                print(news_link)
                import requests
                final_link = requests.get(news_link)
                print("here comes the final_link.url")
                print(final_link.url)
                # now to get rid of the pesky fb stuff at the end
                link3 = url_parse.unquote(final_link.url).split("?u")[0]
                # // link 3 is the domain link
                print("here comes link3")
                print(link3)
# getting the domain
            import tldextract  # The module looks up TLDs in the Public Suffix List, mantained by Mozilla volunteers
            extract = tldextract.extract(link3)
            domain = extract.domain
# getting the score info
            publication = domain
            pub_tuple = retrieve_pub_vote_summary(publication)
            article_rating = retrieve_article_rating(link3)
            print("pub tuple: ", pub_tuple)
            pubscore = (pub_tuple[6], pub_tuple[8], article_rating['total'], article_rating['score_percent'])
            print(pubscore)
    return jsonify(pubscore)


##############################################
@application.route('/domain_check', methods=['GET', 'POST'])
def domain_check():
    if request.method == 'POST':
        if not request.form['url']:
            flash('Please enter all the fields', 'error')
        else:
            rurl = request.form['url']
            import urllib.parse as url_parse
            # now to get rid of the pesky fb stuff at the end
            link3 = url_parse.unquote(rurl).split("?u")[0]
            # getting the domain
            import tldextract  # The module looks up TLDs in the Public Suffix List, mantained by Mozilla volunteers
            extract = tldextract.extract(link3)
            domain = extract.domain
            # getting the score info
            publication = domain
            article = Article.query.filter_by(snippet=publication).first()
            if(article):
                pub_tuple = retrieve_pub_vote_summary(publication)
                article_rating = retrieve_article_rating(link3)
                pub_total = pub_tuple[6]
                pub_rating = pub_tuple[8]
                article_total = article_rating['total']
                article_rating = article_rating['score_percent']
            else:
                pub_total = 0
                pub_rating = 0
                article_total = 0
                article_rating = 0
            pubscore = {
                'present': True if article else False,
                'pub_total': pub_total,
                'pub_rating': pub_rating,
                'article_total': article_total,
                'article_rating': article_rating,
            }
    return jsonify(pubscore)


##############################################
@application.route('/results/<int:id>')
def results(id):
    fb_user_id = ""
    # global article
    f_resp = facebook.get("/me?fields=id,name,picture.type(large)")
    t_resp = twitter.get("account/verify_credentials.json")
    g_resp = google.get("/oauth2/v1/userinfo")
    if f_resp.ok:
        fb_resp = f_resp.json()
        maybe_existing_user = User.query.filter_by(fb_id=fb_resp['id']).first()
        if(maybe_existing_user):
            fb_user_id = maybe_existing_user.fb_id
        else:
            profile_picture = fb_resp.get('picture', {}).get('data', {}).get('url')
            new_user = User(int(fb_resp['id']), profile_picture, fb_resp['name'], 5, auth_provider='facebook')
            db.session.add(new_user)
            try:
                db.session.commit()
                fb_user_id = fb_resp['id']
            except exc.SQLAlchemyError as e:
                pass
    elif t_resp.ok:
        fb_resp = t_resp.json()
        maybe_existing_user = User.query.filter_by(fb_id=fb_resp['id']).first()
        if(maybe_existing_user):
            fb_user_id = maybe_existing_user.fb_id
        else:
            profile_picture = fb_resp.get('profile_image_url_https', '')
            new_user = User(int(fb_resp['id']), profile_picture, fb_resp['name'], 5, auth_provider='twitter')
            db.session.add(new_user)
            try:
                db.session.commit()
                fb_user_id = fb_resp['id']
            except exc.SQLAlchemyError as e:
                pass
    elif g_resp.ok:
        fb_resp = g_resp.json()
        maybe_existing_user = User.query.filter_by(fb_id=fb_resp['id']).first()
        if(maybe_existing_user):
            fb_user_id = maybe_existing_user.fb_id
        else:
            profile_picture = fb_resp.get('picture', '')
            new_user = User(int(fb_resp['id']), profile_picture, fb_resp['name'], 5, auth_provider='google')
            db.session.add(new_user)
            try:
                db.session.commit()
                fb_user_id = fb_resp['id']
            except exc.SQLAlchemyError as e:
                pass

    rate = 0  # either 0 or num/total
    updated_details = []
    article_list_of_one = Article.query.filter_by(id=id)
    all_comments = Comment.query.filter_by(article_id=id)
    ids = [c.user_id for c in all_comments]
    user_name_dict = {}
    all_users = User.query.filter(User.fb_id.in_(ids)).all()
    for user in all_users:
        user_name_dict[str(user.fb_id)] = user.name
        user_name_dict[str(user.fb_id)+"-picture"] = user.fb_pic
        user_name_dict[str(user.fb_id)+"-auth_provider"] = user.auth_provider
    article_comments = Comment.query.filter((Comment.article_id == id) & (Comment.parent == None))
    article_comments_dict = {}
    for comment in article_comments:
        article_comments_dict.setdefault(comment.vote_id, []).append(comment)
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

# getting publication score info
    publication = a_obj.snippet
    pub_tuple = retrieve_pub_vote_summary(publication)
    print("pub tuple: ", pub_tuple)


    total_plus_nn = pub_tuple[0] + pub_tuple[1] + pub_tuple[2] + pub_tuple[3] + pub_tuple[4] + pub_tuple[5]
    print("total_plus_nn: ", total_plus_nn)
    if total_plus_nn == 0:
        total_plus_nn = 1

    onescore = pub_tuple[0]*100 / total_plus_nn
    twoscore = pub_tuple[1]*100 / total_plus_nn
    threescore = pub_tuple[2]*100 / total_plus_nn
    fourscore = pub_tuple[3]*100 / total_plus_nn
    fivescore = pub_tuple[4]*100 / total_plus_nn
    sixscore = pub_tuple[5]*100 / total_plus_nn

    pubscorechoices=(onescore, twoscore, threescore, fourscore, fivescore, sixscore)
    print("pubscorechoices")
    print(pubscorechoices)


    details = avs_obj.getVoteDetails()  # 10/02 - retrieve array of tuples [(user, VoteChoice, Comments)]
    print("Inside results(" + str(id) + "):")
    details_count = 0
    for detail in details:
        updated_details = [(user, VoteChoice, Comments, User.query.filter_by(name=user).first().fb_id, vote_id)
                           for (vote_id, user, VoteChoice, Comments) in details]
        # print("    " + str(details_count) + ": " + details[0] + " " + details[1] + " " + details[2])
        # details_count += 1


    return render_template('results.html', title=a_obj.title, snippet=a_obj.snippet, id=id,
                           image_url=a_obj.image_url, url=a_obj.url, user_name_dict=user_name_dict,
                           vote_choices=vote_choices, home_data=Article.query.all(),
                           vote_details=updated_details, onevotes=pub_tuple[0], twovotes=pub_tuple[1],
                           threevotes=pub_tuple[2], article_comments_dict=article_comments_dict,
                           fourvotes=pub_tuple[3], fivevotes=pub_tuple[4], sixvotes=pub_tuple[5],
                           score_percent=pub_tuple[8], pubscorechoices=pubscorechoices, total_plus_nn=total_plus_nn,
                           fb_user_id=fb_user_id)

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
            if 'source' in request.form and request.form['source'] == 'twitter':
                news_link = request.form['url']
                import requests
                final_link = requests.get(news_link)
                print("here comes the final_link.url")
                print(final_link.url)
                # now to get rid of the pesky fb stuff at the end
                import urllib.parse as url_parse
                link3 = url_parse.unquote(final_link.url).split("?")[0]
                # // link 3 is the domain link
                print("here comes link3")
                print(link3)
            elif 'source' in request.form and request.form['source'] == 'google':
                link3 = request.form['url']
            else:
                rurl = request.form['url']
                print("here comes rurl")
                print(rurl)
                import urllib.parse as url_parse
                url = rurl
                news_link = url_parse.unquote(url).split("?u=")[1].split("?fbclid")[0]
                print("here comes the news_link")
                print(news_link)
                import requests
                final_link = requests.get(news_link)
                print("here comes the final_link.url")
                print(final_link.url)
                # now to get rid of the pesky fb stuff at the end
                link3 = url_parse.unquote(final_link.url).split("?u")[0]
                # // link 3 is the domain link
                print("here comes link3")
                print(link3)
                link3 = url_parse.unquote(link3).split("&fbclid")[0]

            import tldextract  # The module looks up TLDs in the Public Suffix List, mantained by Mozilla volunteers
            extract = tldextract.extract(link3)
            print("extracted:", extract)
            print(extract.domain)
            domain = extract.domain
            print("domain: ", domain)


            article = Article(request.form['title'], link3, request.form['image_url'],
                               domain)

            db.session.add(article)
            try:
                db.session.commit()
            except exc.SQLAlchemyError as e:
               print(e)
               flash('Article url already exists, failed to post new article')
               posted = 0
               #return render_template('/error.html', article_url=article.url)

            # article_list = Article.query.filter_by(image_url=article.image_url)
            # article_list = Article.query.filter_by(url=article.url)

            article_list = Article.query.filter_by(url=article.url)

            if posted == 1:
                flash('Record was successfully added')
            else:
                db.session.rollback()
                # article_list = Article.query.filter_by(image_url=article.image_url)
                # article_list = Article.query.filter_by(url=article.url)
                article_list = Article.query.filter_by(url=article.url)

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
        new_user = User(int(person.get("userID")), person.get("picture"), person.get("name"), 5, auth_provider='facebook')
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


@oauth_before_login.connect
def before_login(blueprint, url):
    flask_session["next_url"] = request.args.get("next_url")


##############################################
@application.route('/votefor/<int:article_id>', methods=['GET', 'POST'])
def votefor(article_id):
    print("votefor")
    fb_user_id = ""
    # global article
    f_resp = facebook.get("/me?fields=id,name,picture.type(large)")
    t_resp = twitter.get("account/verify_credentials.json")
    g_resp = google.get("/oauth2/v1/userinfo")
    if f_resp.ok:
        fb_resp = f_resp.json()
        maybe_existing_user = User.query.filter_by(fb_id=fb_resp['id']).first()
        if(maybe_existing_user):
            fb_user_id = maybe_existing_user.fb_id
        else:
            profile_picture = fb_resp.get('picture', {}).get('data', {}).get('url')
            new_user = User(int(fb_resp['id']), profile_picture, fb_resp['name'], 5, auth_provider='facebook')
            db.session.add(new_user)
            try:
                db.session.commit()
                fb_user_id = fb_resp['id']
            except exc.SQLAlchemyError as e:
                pass
    elif t_resp.ok:
        fb_resp = t_resp.json()
        maybe_existing_user = User.query.filter_by(fb_id=fb_resp['id']).first()
        if(maybe_existing_user):
            fb_user_id = maybe_existing_user.fb_id
        else:
            profile_picture = fb_resp.get('profile_image_url_https', '')
            new_user = User(int(fb_resp['id']), profile_picture, fb_resp['name'], 5, auth_provider='twitter')
            db.session.add(new_user)
            try:
                db.session.commit()
                fb_user_id = fb_resp['id']
            except exc.SQLAlchemyError as e:
                pass
    elif g_resp.ok:
        fb_resp = g_resp.json()
        maybe_existing_user = User.query.filter_by(fb_id=fb_resp['id']).first()
        if(maybe_existing_user):
            fb_user_id = maybe_existing_user.fb_id
        else:
            profile_picture = fb_resp.get('picture', '')
            new_user = User(int(fb_resp['id']), profile_picture, fb_resp['name'], 5, auth_provider='google')
            db.session.add(new_user)
            try:
                db.session.commit()
                fb_user_id = fb_resp['id']
            except exc.SQLAlchemyError as e:
                pass
    article_list_of_one = Article.query.filter_by(id=article_id)
    article = article_list_of_one[0]
    print("here's the id from votefor local hopefully article.id version", article.id)
    posted = 1
    # global article

    vote_choices = VoteChoice.getVoteChoiceList()

    return render_template('/votefor.html', article_id=article.id,
                           article_title=article.title, image_url=article.image_url, article_url=article.url,
                           vote_choices=vote_choices, fb_user_id=fb_user_id
                           )


##############################################
# class PubVoteSummary():
# # This object keeps the count of votes for a Publication
#
#     def __init__(self, article_id):
#         self.article_id = article_id
#         self.choice_count = {}  # count by textual choice
#         self.choice_id = {}
#         self.vote_details = []  # list of tuples (user, vote_choice, comment)
#         choice_list = VoteChoice.getVoteChoiceList()
#         for item in choice_list:
#             self.choice_id[str(item.id)] = item.choice
#         for item in choice_list:
#             self.choice_count[item.choice] = 0
#         self.total_votes = 0
#

    # def retrieve_publication_summary(article_id):
    #     pub_obj = PublicationSummary(article_id)
    #
    #     import sqlalchemy as sa
    #
    #     q = (db.session.query(ArticleVote.vote_choice_id, sa.func.count(ArticleVote.vote_choice_id))
    #          .filter(ArticleVote.article_id == id)
    #          .group_by(ArticleVote.vote_choice_id)
    #          .order_by(ArticleVote.vote_choice_id))
    #
    #     for vote_choice_id, count in q:
    #         print("here comes the count maybe")
    #         print(vote_choice_id, count)

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
        avs_obj.appendDetail((item[0].id, item[1].name, text, item[0].comment))  # 09/27 - added to show comments in results page

    return avs_obj



# find publication
# pulls all "true" votes with that publication name
# pulls all "false" votes with that publication name
# pulls all "eggagerated" votes with that publication name
# total_pub_votes = true + egg + false
# score = (truevotes + .5(eggageratedvotes))/total_pub_votes
# score_fraction = score(100)

@application.route('/insert_comment', methods=['POST'])
def insert_comment():
    article_id = int(request.form['article_id'])
    fb_user_id = request.form['user_id']
    parent_id = request.form['parent_id']
    vote_id = request.form['vote_id']
    text = request.form['comment']
    user_exists = User.query.filter_by(fb_id=fb_user_id).first()
    if not user_exists:
        flash('User does not exist', 'error')
        return redirect('/results/' + str(article_id))
    else:
        if parent_id:
            av_obj = Comment(user_id=fb_user_id, article_id=article_id, text=text, parent_id=int(parent_id))
        else:
            av_obj = Comment(user_id=fb_user_id, article_id=article_id, text=text, vote_id=int(vote_id))
        db.session.add(av_obj)
        try:
            db.session.commit()
        except exc.SQLAlchemyError as e:
            flash('Unable to add comment, Please try later', 'error')

        return redirect('/results/' + str(article_id))


##############################################
@application.route('/insert_vote', methods=['GET', 'POST'])
def insert_vote():
    posted = 1
    # global user_id
    # global article, user_id
    # print ("insert_vote", "this should be the facebook user id", user_id)
    if request.method == 'POST' or request.method == 'GET':
        if not request.form['options'] or not request.form['comments']:
            flash('Please enter all the fields', 'error')
            return redirect('/votefor/' + str(request.form['article_id']))
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
            user_exists = User.query.filter_by(fb_id=fb_user_id).first()
            if not user_exists:
                flash('User does not exist', 'error')
                return redirect('/votefor/' + str(article_id))
            else:
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
                # print(article.id)
                details_count = 0
                for detail in details:
                    print(detail)
                    # print("    " + str(details_count) + ": " + details[0] + " " + details[1] + " " + details[2])
                    details_count += 1

                publication = a_obj.snippet
                pub_tuple = retrieve_pub_vote_summary(publication)
                print("pub tuple: ", pub_tuple)



                return redirect('/results/' + str(a_obj.id))

        # return render_template('/results.html', title=a_obj.title,
        #                            image_url=a_obj.image_url,
        #                            vote_choices=vote_choices, vote_details=details)


##############################################

if __name__ == '__main__':
    db.create_all()
    application.run(host="0.0.0.0", debug=True, ssl_context=("example.com+2.pem", "example.com+2-key.pem"))
