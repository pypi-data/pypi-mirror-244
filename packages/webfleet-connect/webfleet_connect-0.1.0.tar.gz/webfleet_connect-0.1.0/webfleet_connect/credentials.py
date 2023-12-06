import os

class Credentials:
  def __init__(self, params = {}):
    merged = self._default_params().update(params)
    self._accound = merged['account']
    self._username = merged['username']
    self._password = merged['password']
    self._apikey = merged['apikey']

  def __str__(self):
    return f'{self.account()}&{self.username()}&{self.password()}&{self.apikey()}'

  def _default_params():
    return {
      'account': os.getenv('WEBFLEET_CONNECT_ACCOUNT'),
      'username': os.getenv('WEBFLEET_CONNECT_USERNAME'),
      'password': os.getenv('WEBFLEET_CONNECT_PASSWORD'),
      'apikey': os.getenv('WEBFLEET_CONNECT_APIKEY')
    }

  def account(self):
    return f'account={self._account}'
  
  def username(self):
    return f'username={self._username}'
  
  def password(self):
    return f'password={self._password}'
  
  def apikey(self):
    return f'apikey={self._apikey}'
