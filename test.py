import requests
import threading
import random
import string
import concurrent.futures


def generate_random_student():
    name = ''.join(random.choices(string.ascii_uppercase, k=6))
    dept = random.choice(
        ["CSE", "IT", "ECE", "EEE", "MECH", "CIVIL", "AIDS", "CSBS"])
    batch = str(random.randint(2023, 2025))
    leetcode_username = ''.join(random.choices(string.ascii_lowercase, k=10))
    codechef_username = ''.join(random.choices(string.ascii_lowercase, k=10))
    codeforces_username = ''.join(random.choices(string.ascii_lowercase, k=10))
    s = {
        "name": name,
        "dept": dept,
        "batch": batch,
        "leetcode_username": leetcode_username,
        "codechef_username": codechef_username,
        "codeforces_username": codeforces_username
    }
    return s


data = [generate_random_student() for _ in range(200)]
url = "http://localhost:8000/api/students"
success = True


def send_request(data):
    response = requests.post(url, json=data)
    if response.status_code != 200:
        global success
        success = False
        print(f"TEST FAILED FOR {data}")
    print(response.status_code, response.json())


if __name__ == '__main__':
    max_threads = 1000
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(send_request, item) for item in data]
        concurrent.futures.wait(futures)
    if success:
        print("ALL TESTS PASSED")
