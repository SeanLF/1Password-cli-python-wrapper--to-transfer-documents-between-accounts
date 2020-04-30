# 1Password python wrapper

Light python wrapper for [1Password CLI](https://support.1password.com/command-line-reference/), inspired by [wandera](https://github.com/wandera/1password-client).

## Getting started

On a Mac, assuming you have homebrew, and python3 installed

- `brew cask install 1password-cli`
- `python3 main.py`

### Additional info

- `transfer_documents.py` contains the executable code to transfer documents from one account to another.
  - Some errors can occur, and will be shown in the console.
  - Transferred document includes the user-defined tags, title and the original uploaded filename.
- `client.py` contains the wrapper for the 1Password CLI.
  - implementation allows for multiple users logged in at once, using session tokens.
- `utils.py` contains the code to interact with the command line.
  - this code was taken from [wandera](https://github.com/wandera/1password-client/blob/master/onepassword/utils.py)
