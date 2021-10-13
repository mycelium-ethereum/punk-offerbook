from client import webhook

def alert(msg: str):
    webhook.send(msg)