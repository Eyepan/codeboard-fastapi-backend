# GET /api/rankings/START80A?itemsPerPage=10000&order=asc&page=1&sortBy=rank HTTP/2
# Host': 'www.codechef.com


import requests

headers = {
    'Cookie': 'SESS93b6022d778ee317bf48f7dbffe03173=74faa6408dc8cc6fd6f07ba3cfa584fe; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjb2RlY2hlZi5jb20iLCJzdWIiOiIzNTQxNDQ1IiwidXNlcm5hbWUiOiJpYW10ZW9nZ3kiLCJpYXQiOjE2Nzg1ODgzNzAsIm5iZiI6MTY3ODU4ODM3MCwiZXhwIjoxNjgwNTgyNzcwfQ.lpv5CRXuuLqfTO5NoM7dNbT1S_UMyAdaPehpUig2t00; uid=3541445',
    'x-csrf-token': '76313213fb21041a17d3281f49b7be049a4cf6f127645eebe0bd7c393a035721',
}

response = requests.get(
    url='https://www.codechef.com/api/rankings/START80A?itemsPerPage=10000&order=asc&page=1&sortBy=rank', headers=headers)
print(response.json())
