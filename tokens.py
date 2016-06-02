import webapp2
import tweepy
import yaml
import traceback
import logging
import jwt
import time

# Setup RS256 Algorithm
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm
jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))

# Load Config File
with open("config.yaml", 'r') as stream:
    try:
        secrets = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Encodes UIDs
def encodeTokenFromUID(uid):
  return jwt.encode({
  'iss': secrets["service_account_email"], # Service email address
  'sub': secrets["service_account_email"], # Service email address
  'aud': "https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit", # Specified in Docs
  'iat': int(time.time()), # Epoch
  'exp': int(time.time()) + 30 * 60, # Expiration date (30 mins in future)
  'uid': uid # UID
  }, secrets["firebase_private_key"], algorithm='RS256')

# Handles token requests
class TokenRequest(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        # Generate OAuth Handler from provided keys
        auth = tweepy.OAuthHandler(secrets["twitter_consumer_key"], secrets["twitter_consumer_secret"])
        auth.set_access_token(self.request.get("auth_token"), self.request.get("auth_token_secret"))
        
        try:
          # Create an API client from those keys
          api = tweepy.API(auth)
          # Validates the credentials (throws exception if invalid)
          user = api.verify_credentials()
          # Gets the UID
          uid = user.id
          # Encodes the UID in a token
          token = encodeTokenFromUID(str(uid))
          # Responds with token
          self.response.write(token)
        except tweepy.TweepError as e:
          # Prints exception to log
          logging.error(traceback.format_exc())
          # Responds with invalid
          self.response.write("invalid")

# Start web server
app = webapp2.WSGIApplication([
    ('/token', TokenRequest),
], debug=True)
