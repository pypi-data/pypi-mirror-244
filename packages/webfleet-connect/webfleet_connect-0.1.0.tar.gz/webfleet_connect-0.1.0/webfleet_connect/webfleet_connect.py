from dotenv import load_dotenv
from session import Session
from credentials import Credentials
from concurrent import Config

class WebfleetConnect:
  @classmethod
  def create(params = {}):
    load_dotenv()
    credentials = Credentials(params)
    config = Config(params)
    return Session(credentials, config)
