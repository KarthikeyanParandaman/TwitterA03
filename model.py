from google.appengine.ext import ndb
class Twitter_model(ndb.Model):
      users = ndb.StringProperty()
      about = ndb.StringProperty()
      tweets = ndb.StringProperty(repeated=True)
      followers= ndb.StringProperty(repeated=True)
      following = ndb.StringProperty(repeated=True)

class Tweet_all(ndb.Model):
    alltweets=ndb.StringProperty(repeated=True)
    blobs = ndb.BlobKeyProperty(repeated=True)
    username=ndb.StringProperty(repeated=True)
