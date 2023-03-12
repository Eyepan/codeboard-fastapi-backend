import requests


url = 'http://localhost:8000/api/leetcode/contest/weekly-contest-'

for i in range(287, 336):
    print("Fetching data for contest " + str(i))
    response = requests.get(url + str(i))
    print(response.status_code, response.json())
