import requests


url = 'http://localhost:8000/api/codechef/contest/START'

for i in range(58, 81):
    print("Fetching data for contest " + str(i) + "A")
    response = requests.get(url + str(i) + 'A')
    print(response.status_code, response.json())

    print("Fetching data for contest " + str(i) + "B")
    response = requests.get(url + str(i) + 'B')
    print(response.status_code, response.json())

    print("Fetching data for contest " + str(i) + "C")
    response = requests.get(url + str(i) + 'C')
    print(response.status_code, response.json())

    print("Fetching data for contest " + str(i) + "D")
    response = requests.get(url + str(i) + 'D')
    print(response.status_code, response.json())
