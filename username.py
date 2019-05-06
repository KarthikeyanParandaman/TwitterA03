import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model import Twitter_model
from model import Tweet_all
import os

class Username(webapp2.RequestHandler):
    def get(self):
        email = users.get_current_user().email()
        myuser_key = ndb.Key('Twitter_model', email)
        myuser = myuser_key.get()
        self.response.out.write("<html><head></head><body>")
        self.response.out.write("""<h2 align="center">Create your profile</h2>""")
        self.response.out.write("""<form method='get' action='/username'>""")
        self.response.out.write("""<h4>Enter UserName:&nbsp;&nbsp<input type='text' name='input' required='True'/></h4>""")
        self.response.out.write("""<h4>About:&nbsp;&nbsp<input type='text' name='input1' required='True' maxlength="280"/><br>""")
        self.response.out.write("""<br><input type='submit' name='button' value='Submit'/>""")
        self.response.out.write("""</form>""")
        action=self.request.get('button')
        url = users.create_logout_url(self.request.uri)
        if action == 'Submit':
                username=self.request.get('input')
                bio=self.request.get('input1')
                myuser.users=username
                myuser.about=bio
                myuser.put()
                self.redirect('/')

        self.response.out.write("</body></html>")
