from client import OnePassword

def main():
  SOURCE_ACCOUNT = 'source'
  TARGET_ACCOUNT = 'target'

  message = "Input {} account information"
  email_message = "1Password email account: "
  domain_message = "1Password domain: "
  secret_message = "1Password secret: "

  # Use personal account to get documents
  # Use family account to store new documents
  op = OnePassword()
  for account_shorthand in [SOURCE_ACCOUNT, TARGET_ACCOUNT]:
    print(message.format(account_shorthand))
    op.signin(op.add_account(email=input(email_message), domain=input(domain_message), secret=input(secret_message), shorthand=account_shorthand))
    print("")

  # API call here
  docs = op.list_documents(account_shorthand=SOURCE_ACCOUNT)
  count = len(docs)

  # iterate over docs
  for idx, doc in enumerate(docs):
    uuid, title, vaultUuid = doc['uuid'], doc['overview']['title'], doc['vaultUuid']
    tags = doc['overview']['tags'] if 'tags' in doc['overview'] else []
    
    # Get more info in order to find filename
    fileName = op.get_item(uuid, vaultUuid, account_shorthand=SOURCE_ACCOUNT)['details']['documentAttributes']['fileName']

    print("{}/{}\t{}\t{}\t{}".format(idx+1, count, title, fileName, tags))
    fileName = "./{}/{}".format('1Password_files', fileName)
    
    # API call here
    op.get_document(uuid, title, fileName, vault=vaultUuid, account_shorthand=SOURCE_ACCOUNT)
    op.put_document(fileName, title, tags, account_shorthand=TARGET_ACCOUNT)

  # Create documents
  for account_shorthand in [SOURCE_ACCOUNT, TARGET_ACCOUNT]:
    op.signout(forget=True, account_shorthand=account_shorthand)

main()