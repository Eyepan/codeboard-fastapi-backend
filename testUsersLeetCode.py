import json
import requests

# await fetch("https://leetcode.com/graphql/", {
#     "credentials": "include",
#     "headers": {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
#         "Accept": "*/*",
#         "Accept-Language": "en-US,en;q=0.5",
#         "content-type": "application/json",
#         "x-csrftoken": "QjJsZm6urEXDo212hQZR8Mc91ciKUUmvapy4ZM5zhy7n9Ueez2FtQIDYZqt0Vu3n",
#         "authorization": "",
#         "random-uuid": "d0792f49-266b-e147-5458-ee0cbe7a0286",
#         "sentry-trace": "24f981f574184ff2b57168ee76338ed4-9e46955a74bb8a84-0",
#         "baggage": "sentry-environment=production,sentry-release=063216d900eee35bfb6478546cf86d4fbf2322c5,sentry-transaction=%2Fu%2F%5Busername%5D,sentry-public_key=2a051f9838e2450fbdd5a77eb62cc83c,sentry-trace_id=24f981f574184ff2b57168ee76338ed4,sentry-sample_rate=0.004",
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin"
#     },
#     "referrer": "https://leetcode.com/pan-iyappan/",
#     "body": "{query:    query userProblemsSolved($username: String!) {  allQuestionsCount {    difficulty    count  }  matchedUser(username: $username) {    problemsSolvedBeatsStats {      difficulty      percentage    }    submitStatsGlobal {      acSubmissionNum {        difficulty        count      }    }  }}    ,variables:{username:pan-iyappan}}",
#     "method": "POST",
#     "mode": "cors"
# });

# write the above as a python requests
import requests
import sys

username = sys.argv[1]

data = {
    "query": """
        query APIReq($username: String!) {
            allQuestionsCount {
                difficulty
                count
            }
            matchedUser(username: $username) {
                username
                profile {
                    ranking
                }
                problemsSolvedBeatsStats {      
                    difficulty      
                    percentage    
                }
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
        }
        """,
    "variables": {"username": f"{username}"}
}

response = requests.post("https://leetcode.com/graphql/", json=data)
