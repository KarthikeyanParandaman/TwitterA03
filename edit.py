import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model import Twitter_model
from model import Tweet_all
import os

class Edit(webapp2.RequestHandler):
    def get(self):
        email = users.get_current_user().email()
        model_key = ndb.Key('Twitter_model', email)
        model = model_key.get()
        self.response.out.write("<html><head></head><body><br>")
        self.response.out.write("""<br><h3 align="center">Edit your information below:</h3><br/>""")
        self.response.out.write("""<form method='get' action='/edit'>""")
        self.response.out.write("""<h3 align="center">About: &nbsp;<input type='text' name='input1' required='True' maxlength="280"/> <input type='submit' name='button' value='Submit'/></h3>""")
        self.response.out.write("""""")
        self.response.out.write("""</form>""")
        self.response.out.write("""<h4 align="center"><a href='/'>Home</a></h4>""")
        react=self.request.get('button')
        if react == 'Submit':
            about=self.request.get('input1')
            model.about=about
            model.put()
            self.redirect('/')
        self.response.out.write("</body></html>")
    def post(self):
        email = users.get_current_user().email()
        model_key = ndb.Key('Twitter_model', email)
        model = model_key.get()
        react=self.request.get('button')
        tweetallkey =ndb.Key('Tweet_all','1')
        twee=tweetallkey.get()
        uname=model.users
        if react == 'Submit':
            tweet=self.request.get('tweet')
            model.tweets.append(tweet)
            twee.alltweets.append(tweet)
            twee.username.append(uname)
            twee.put()
            model.put()
            self.redirect('/')
