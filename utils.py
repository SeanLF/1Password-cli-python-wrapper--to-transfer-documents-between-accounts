"""
Author: wandera
URL: https://github.com/wandera/1password-client/blob/master/onepassword/utils.py
"""

import os

def read_bash_return(cmd, single=True):
  process = os.popen(cmd)
  preprocessed = process.read()
  process.close()
  if single:
      return str(preprocessed.split("\n")[0])
  else:
      return str(preprocessed)