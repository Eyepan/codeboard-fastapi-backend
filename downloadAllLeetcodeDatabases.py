from time import sleep
import requests


url = 'http://localhost:8000/api/leetcode/contest/weekly-contest-'

for i in range(275, 336):
    print("Fetching data for contest " + str(i))
    response = requests.get(url + str(i))
    # sleep for an unsuspicious amount of time
    sleep(0.5)
    print(response.status_code, response.json())
