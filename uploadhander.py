from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.api import users
from model import Twitter_model
from model import Tweet_all
from google.appengine.ext.webapp import blobstore_handlers
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]
        blobinfo = blobstore.BlobInfo(upload.key())
        filename = blobinfo.filename
        email = users.get_current_user().email()
        myuser_key = ndb.Key('Twitter_model', email)
        myuser = myuser_key.get()
        name=myuser.users
        mk=ndb.Key('Tweet_all','1')
        m=mk.get()
        m.alltweets.append(filename)
        m.blobs.append(upload.key())
        m.username.append(name)
        m.put()
        email = users.get_current_user().email()
        myuser_key = ndb.Key('Twitter_model', email)
        myuser = myuser_key.get()
        myuser.tweets.append(filename)
        #m.blobs.append(upload.key())
        myuser.put()
        self.redirect('/')
