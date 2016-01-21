import praw


#Handles all the connecting and authenticating
def setup():
    file=open('authentication.txt') #text file with the various keys needed to authenticate the bot

    var1=file.readline().replace('\n', '')
    var2=file.readline().replace('\n', '')
    var3=file.readline().replace('\n', '')
    var4=file.readline().replace('\n', '')
    user_agent = "Karma Assasian indexer by /u/dhamilt9"
    r=praw.Reddit(user_agent)
    r.set_oauth_app_info(
            client_id=var1,
            client_secret=var2, 
            redirect_uri='http://127.0.0.1:65010/authorize_callback'
            )
    access_information={
            u'access_token': var3, 
            u'scope': set([
                u'edit', 
                u'read', 
                u'mysubreddits', 
                u'submit', 
                u'identity'
                ]), 
            u'refresh_token': var4
            }
    r.set_access_credentials(**access_information)
    return r



#Takes a comment as an argument (parent) as well as the level of the comment (level) and the score of the parent (parentScore)
#Recursivly traverses all replies to the comment, if the score is higher than the parent score, it's considered a "karma
#assassin", and added to the list
def commentCrawl(parent, level, parentScore):
    if parent.replies==[]:
        return parent
    else:
        for i in parent.replies:
            try:
                score=i.score
                body=i.body
                if score>parentScore and parentScore>0:
                    commentassassins[i.permalink]=score-parentScore
                commentCrawl(i, level+1, score)
            except AttributeError:
                pass


#Takes a post, and runs commentCrawl on all top level comments.
def getReplies(sub):
    for i in sub.comments:
        try:
            commentCrawl(i, 1, i.score)
        except AttributeError:
            pass


commentassassins={}

def main(url=None):
    r=setup()
    submission=r.get_submission('https://www.reddit.com/r/mildlyinteresting/comments/41v9uo/i_saw_these_very_bad_kids_at_a_convenience_store/')
    submission.replace_more_comments(0)

    getReplies(submission)

    for i in commentassassins:
        print i, commentassassins[i]

main()
