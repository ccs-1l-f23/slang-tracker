# Takes top comments from top 50 posts from each UC subreddit and writes them to a file

import requests
uc_subreddits = ["r/UCI", "r/berkeley", "r/ucla", "r/UCSD", "r/UCSC", "r/UCDavis", "r/UCR", "r/UCSantaBarbara", "r/UCMerced"]

top_posts = {}
for sub in uc_subreddits:
    top_posts[sub] = []

for sub in uc_subreddits:
    r = requests.get('https://www.reddit.com/' + sub + '/top/.json?count=50&t=all', headers = {'User-agent': 'your bot 0.1'})
    for i in range(len(r.json()["data"]["children"])):
        top_posts[sub].append(r.json()["data"]["children"][i]["data"]["permalink"])

for sub in uc_subreddits:
    f = open("texts/reddit/" + sub[2:] + ".txt", "w")

    for top in top_posts[sub]:
        r = requests.get('https://www.reddit.com' + top + '.json?sort=top', headers = {'User-agent': 'your bot 0.1'})
        for i in range(len(r.json()[1]["data"]["children"])):
            try:
                f.write(r.json()[1]["data"]["children"][i]["data"]["body"])
            except:
                pass
            f.write("\n")

    f.close()