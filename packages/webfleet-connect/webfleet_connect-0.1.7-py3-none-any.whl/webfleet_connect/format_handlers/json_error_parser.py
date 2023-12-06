class JsonErrorParser():
  def is_error_found(self, response):
    json = response.json
    if isinstance(json, list):
      return False
    return 'errorCode' in json
