import requests
from .webfleet_connect_error import WebfleetconnectError
from .webfleet_connect_response import WebfleetConnectResponse
from .format_handlers.csv_error_parser import CsvErrorParser
from .format_handlers.json_error_parser import JsonErrorParser

class Connection:
  def __init__(self, session):
    self._session = session
    self._error_parser = self._build_error_parser(session)

  def exec(self, url):
    response = requests.get(url)
    is_json = self.session.has_json()
    if self._is_error_found(response):
      raise WebfleetconnectError(response, url, is_json)
    return WebfleetConnectResponse(response, url, is_json)
  
  def _is_error_found(self):
    return self._error_parser.is_error_found()

  def _build_error_parser(self, session):
    if session.has_json():
      return JsonErrorParser()
    return CsvErrorParser()
