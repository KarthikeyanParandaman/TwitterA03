import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model import Twitter_model
from model import Tweet_all
import os
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)
class DeleteEdit(webapp2.RequestHandler):
    def get(self,id):
        self.response.headers['Content-Type'] = 'text/html'
        myid=id
        email = users.get_current_user().email()
        model_key = ndb.Key('Twitter_model', email)
        model = model_key.get()
        list=model.tweets
        list=list[::-1]
        template_values={'model':model,'list':list}
        template=JINJA_ENVIRONMENT.get_template('deletedit.html')
        self.response.write(template.render(template_values))
    def post(self,id):
        react = self.request.get('button')
        email = users.get_current_user().email()
        model_key = ndb.Key('Twitter_model', email)
        model = model_key.get()
        tweetallkey =ndb.Key('Tweet_all','1')
        twee=tweetallkey.get()
        myid=id
        twts=None
        if react == 'delete':
            list=model.tweets
            list=list[::-1]
            del list[int(self.request.get('index')) - 1]
            list=list[::-1]
            model.tweets=list
            model.put()
            twts=self.request.get('users_name')
            twee.alltweets.remove(twts)
            twee.put()
            self.redirect('/deletedit/%s'%(myid))
        if react=='Submit':
            twts=self.request.get('users_name')
            list1=model.tweets
            list1=list1[::-1]
            twts1=list1[int(self.request.get('index'))-1]
            list=model.tweets
            list=list[::-1]
            list[int(self.request.get('index'))-1]=self.request.get('users_name')
            list=list[::-1]
            model.tweets=list
            model.put()
            twee.alltweets[twee.alltweets.index(twts1)]=twts
            twee.put()
            self.redirect('/deletedit/%s'%(myid))
