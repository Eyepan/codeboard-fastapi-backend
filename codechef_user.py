import requests


response = requests.get('https://www.codechef.com/users/iamteoggy')

with open('something', 'w') as f:
    f.write(response.text)
