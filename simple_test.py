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
class PublicationVoteSummary():
# This object keeps the count of votes for a Publication

    def __init__(self, article_id):
        self.snippet = snippet
        self.choice_count = {}  # count by textual choice
        self.choice_id = {}

        pub_choice_list = VoteChoice.getVoteChoiceList()

        for item in pub_choice_list:
            self.choice_id[str(item.id)] = item.choice
        for item in pub_choice_list:
            self.choice_count[item.choice] = 0
        self.total_votes = 0

    def addVote(self, choice):
        self.choice_count[choice] = self.choice_count[choice] + 1
        self.total_votes = self.total_votes + 1

    def getVoteCount(self, choice):
        return self.choice_count[choice]

##############################################
class ArticleVoteSummary():
    # This object keeps the count of votes for an Article

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
def retrieve_publication_summary(article_id):
    pub_obj = PublicationSummary(article_id)
    publication_list = db.session.query(ArticleVote, Snippet).filter(ArticleVote.article_id == article_id).filter(
        ArticleVote.vote_choice_id == 1).all()
   for item in vote_choice_id:
        # avs_obj.appendComment(item.comment) # 09/27 - added to show comments in  page
        avs_obj.appendDetail((item[1].name, text, item[0].comment))  # 09/27 - added to show comments in results page
    return pub_obj



# find publication
# pulls all "true" votes with that publication name
# pulls all "false" votes with that publication name
# pulls all "eggagerated" votes with that publication name
# total_pub_votes = true + egg + false
# score = (truevotes + .5(eggageratedvotes))/total_pub_votes
# score_fraction = score(100)
