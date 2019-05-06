import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from model import Tweet_all
from google.appengine.ext.webapp import blobstore_handlers
class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        index = int(self.request.get('index'))
        mk=ndb.Key('Tweet_all','1')
        m=mk.get()
        self.send_blob(m.blobs[index])
