import dropbox, logging

class DropboxHelper():
  '''
  '''
  def __init__(self, access_token):
    '''
    @brief connect to dropbox account via access token.
    It will check with any problem and raise error
    @param access_token: token needed to connect into your dropbox account
    '''
    self.client = dropbox.client.DropboxClient(access_token)
    try:
      self.client.account_info()
      logging.info("Client dropbox connected")
    except dropbox.rest.ErrorResponse as e:
      logging.error("Unable to connect dropbox with access token: %s", e)
      raise dropbox.rest.ErrorResponse

  def __del__(self):
    pass

  def uploadFile(self, directory, destination, filename):
    '''
    @brief:
    @param directory: directory where is the file (like ./zero/toto/)
    @param destination: destinationPath in dropbox (like /subDir/zero/toto/yourfile.png)
    @param filename: filename (like yourfile.png)
    @return: False if any error, else True
    '''
    try:
      f = open(directory + filename, 'rb')
      self.client.put_file(destination, f)
      logging.info("[%s] uploaded into dropbox client: [%s]", filename, destination)
      return True
    except dropbox.rest.ErrorResponse as e:
      logging.warning("[%s]: Unable to upload into your dropbox: %s", destination, e)
      return False
    except BaseException as e:
      logging.warning("[%s]: Unable to open the path: %s", filename, e)
      return False
