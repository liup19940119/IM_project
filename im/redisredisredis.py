import redis
import requests

r1 = redis.Redis(host='127.0.0.1', port=6379)
r1.set('lesson', 'python')
r2 = redis.Redis(host='127.0.0.1', port=6380)
print(r2.get('lesson'))

re = requests.request('POST', 'http://127.0.0.1:6379')
print(re)
