from serverchan import ServerChan
from serverchan.channel import Channels

secret = 'SCU114xxxxx'
serverchan = ServerChan(secret)
response = serverchan.push(title="test", desp='just for test', channel='{}|{}'.format(Channels.WECHAT_SERVICE_ACCOUNT, Channels.PUSHDEER))
print(response.text)
print(response.text.encode().decode('unicode_escape'))