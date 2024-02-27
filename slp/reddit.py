# Takes top comments from top 50 posts from each UC subreddit and writes them to a file

import requests

# UCs
SUBREDDITS = ["r/UCI", "r/berkeley", "r/ucla", "r/UCSD", "r/UCSC", "r/UCDavis", "r/UCR", "r/UCSantaBarbara", "r/UCMerced"]

# Top 10 US colleges by subreddit member count
# https://www.researchgate.net/figure/Top-16-US-college-subreddits-by-member-count-June-2018-These-subreddits-customize_tbl1_354743946
# SUBREDDITS = ["r/UIUC", "r/berkeley", "r/aggies", "r/gatech", "r/UTAustin", "r/OSU", "r/ucf", "r/UCSD", "r/rutgers", "r/VirginiaTech"]

POST_COUNT = 10
FILE_PATH = "/Users/rohil/GitHub-Repositories/slang-tracker/texts/reddit/uc-timestamped/"

def get_top_posts(subreddit):
    """Fetch the top posts from a subreddit."""

    url = f'https://www.reddit.com/{subreddit}/top/.json?count={POST_COUNT}&t=all'
    headers = {'User-agent': 'your bot 0.1'}
    response = requests.get(url, headers=headers)
    posts = response.json()["data"]["children"]
    return [post["data"]["permalink"] for post in posts]

def write_comments_to_file(posts):
    """Write the comments of the top posts to a file."""

    for post in posts:
        url = f'https://www.reddit.com{post}.json?sort=top'
        headers = {'User-agent': 'your bot 0.1'}
        response = requests.get(url, headers=headers)
        comments = response.json()[1]["data"]["children"]
        for comment in comments:
            try:
                timestamp = int(comment["data"]["created_utc"])
                body = comment["data"]["body"]
            except:
                continue

            with open(f"{FILE_PATH}{timestamp}.txt", "w") as f:
                try:
                    f.write(body)
                except:
                    pass

def main():
    """Main function to orchestrate the process."""

    for subreddit in SUBREDDITS:
        top_posts = get_top_posts(subreddit)
        write_comments_to_file(top_posts)

if __name__ == "__main__":
    main()