"""
Inspired from https://github.com/wandera/1password-client
"""

from utils import read_bash_return
import json
import re

class OnePassword:
  def __init__(self, domain=None, email=None, secret=None, shorthand=None):
    self.accounts = {}
    if email is not None:
      self.signin(self.add_account(domain, email, secret, shorthand))

  def __del__(self):
    for account_shorthand in iter(self.accounts.keys()):
      self.signout(account_shorthand=account_shorthand, forget=True)

  def add_account(self, domain, email, secret, shorthand=None):
    account = { 'domain': domain, 'email': email, 'secret': secret, 'session_token': None }
    account_shorthand = shorthand if shorthand is not None else re.match(r"^(.*?)\.", domain)[1]
    self.accounts[account_shorthand] = account
    return account_shorthand

  def account_shorthand(self, account_shorthand=None):
    if (account_shorthand is None) and (len(self.accounts.keys()) is 1):
      account_shorthand = next(iter(self.accounts.keys()))
    return account_shorthand

  def signin(self, account_shorthand=None):
    account_shorthand = self.account_shorthand(account_shorthand)
    account = self.accounts[account_shorthand]
    cmd = "op signin {} {} {} --shorthand {} --raw".format(account['domain'], account['email'], account['secret'], account_shorthand)
    session_token = read_bash_return(cmd)
    self.accounts[account_shorthand]['session_token'] = session_token

  def signout(self, account_shorthand=None, forget=False):
    session_token = self.accounts[self.account_shorthand(account_shorthand)]['session_token']
    cmd = "op signout --session {}".format(session_token)
    if forget is True:
      self.accounts.pop(account_shorthand)
      cmd = "{} --forget".format(cmd)
    return read_bash_return(cmd)

  def get_item(self, uuid, vault, account_shorthand=None):
    session_token = self.accounts[self.account_shorthand(account_shorthand)]['session_token']
    return json.loads(read_bash_return("op get item {} --vault={} --session {}".format(uuid, vault, session_token)))

  def list_documents(self, account_shorthand=None):
    session_token = self.accounts[self.account_shorthand(account_shorthand)]['session_token']
    return json.loads(read_bash_return("op list documents --session {}".format(session_token)))

  def get_document(self, docUuid, docname, filename, vault="Private", account_shorthand=None):
    session_token = self.accounts[self.account_shorthand(account_shorthand)]['session_token']
    cmd = "op get document {} --vault={} --output '{}' --session {}".format(docUuid, vault, filename.replace("'", "\'"), session_token)
    return read_bash_return(cmd, single=False)

  def put_document(self, filename, title, tags, vault="Private", account_shorthand=None):
    session_token = self.accounts[self.account_shorthand(account_shorthand)]['session_token']
    filename, title, tags = filename.replace("'", "\'"), title.replace("'", "\'"), ','.join(tags).replace("'", "\'")
    if tags is '':
      cmd = "op create document '{}' --title='{}' --vault={} --session {}".format(filename, title, vault, session_token)
    else:
      cmd = "op create document '{}' --title='{}' --tags='{}' --vault={} --session {}".format(filename, title, tags, vault, session_token)
    return read_bash_return(cmd)
