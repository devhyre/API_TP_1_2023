from urllib import request

URL = 'http://localhost:8080'
response = request.urlopen(URL)
print(response.read())