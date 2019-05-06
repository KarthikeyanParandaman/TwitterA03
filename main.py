import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from uploadhander import UploadHandler
from downloadhander import DownloadHandler
from model import Twitter_model
from model import Tweet_all
from username import Username
from edit import Edit
from profile import Profile
from deleteedit import DeleteEdit
import os

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        model = None
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            email = users.get_current_user().email()
            model = ndb.Key('Twitter_model', email)
            model = model.get()
            tweetallkey =ndb.Key('Tweet_all','1')
            twee=tweetallkey.get()
            if twee==None:
                twee=Tweet_all(id='1')
                twee.put()
            if model == None:
                welcome = 'Welcome to the application'
                model = Twitter_model(id=email)
                model.put()
            if model.users==None:
                self.redirect('/username')
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
        qry=qry = Twitter_model.query().fetch()
        proname=self.request.get('usersearch')
        fuser=None
        query1=0
        tsearch=self.request.get('tweetsearch')
        ftweet=[]
        query2=0
        react=self.request.get('button')
        if react=='Search':
            for i in qry:
                if i.users==proname:
                    query1=query1+1
                    fuser=proname
        if react=='Tweet Search':
            for i in qry:
                for j in i.tweets:
                    if tsearch in j:
                        query2=query2+1
                        ftweet.append(j)
        followers=0
        following=0
        if model!=None:
            for i in model.followers:
                    followers=followers+1
            for j in model.following:
                    following=following+1

        tweetall_key = ndb.Key('Tweet_all', '1')
        tweetall_key = tweetall_key.get()
        tweetofall=[]
        usernametweets=[]
        if tweetall_key!=None:
            for i in reversed(tweetall_key.alltweets):
                tweetofall.append(i)
            tweetofall = tweetofall[:50]
            for j in reversed(tweetall_key.username):
                usernametweets.append(j)
            usernametweets=usernametweets[:50]
        usertweets = map(' : '.join,zip(usernametweets,tweetofall))
        template_values = {'url' : url,'url_string' : url_string,'user' : user,'welcome' : welcome,'model' : model,'query1':query1,'fuser':fuser,'query2':query2,'ftweet':ftweet,'followers':followers,'following':following,'usertweets':usertweets,'upload_url' : blobstore.create_upload_url('/upload')}
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))
app = webapp2.WSGIApplication([('/', MainPage),('/username', Username),('/edit',Edit),('/profile/(.*)',Profile),('/deletedit/(.*)',DeleteEdit),('/upload', UploadHandler),
('/download', DownloadHandler)], debug=True)
