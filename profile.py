import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model import Twitter_model
from model import Tweet_all
import os

class Profile(webapp2.RequestHandler):
    def get(self,id):
        self.response.headers['Content-Type'] = 'text/html'
        myid=id
        query = Twitter_model.query(Twitter_model.users == myid)
        list=[]
        for i in query:
            for j in reversed(i.tweets):
                list.append(j)
        list = list[:50]
        template_values={'query':query,'list':list}
        template=JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))
    def post(self,id):
        email = users.get_current_user().email()
        model_key = ndb.Key('Twitter_model', email)
        model = model_key.get()
        uname=model.users
        myid=id
        mails=None
        funame=None
        query = model.query(model.users == myid)
        for i in query:
            mails=i.key.id()
        react=self.request.get('button')
        if action == 'FOLLOW':
                user_keys = ndb.Key('Twitter_model', mails)
                users = user_keys.get()
                funame=users.users
                if uname==users.users:
                        self.redirect('/profile/%s'%(myid))
                else:
                    if uname in users.followers:
                            self.redirect('/profile/%s'%(myid))
                    else:
                            users.followers.append(uname)
                            model.following.append(funame)
                            model.put()
                            users.put()
                            self.redirect('/profile/%s'%(myid))
        if action == 'UNFOLLOW':
            user_keys = ndb.Key('Twitter_model', mails)
            users = user_keys.get()
            funame=users.users
            if uname in users.followers:
                users.followers.remove(uname)
                users.put()
                if funame in user.following:
                    user.following.remove(funame)
                    user.put()
            self.redirect('/profile/%s'%(myid))
