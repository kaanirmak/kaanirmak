import os
import requests
import re

def get_github_stats(username, token):
    headers = {"Authorization": f"token {token}"} if token else {}
    
    # Get user profile stats
    user_url = f"https://api.github.com/users/{username}"
    user_resp = requests.get(user_url, headers=headers)
    if user_resp.status_code != 200:
        raise Exception(f"Failed to fetch user data: {user_resp.text}")
    user_data = user_resp.json()
    
    followers = user_data.get("followers", 0)
    public_repos = user_data.get("public_repos", 0)
    
    # Get repositories to calculate total stars
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    repos_resp = requests.get(repos_url, headers=headers)
    if repos_resp.status_code != 200:
        raise Exception(f"Failed to fetch repos: {repos_resp.text}")
    repos_data = repos_resp.json()
    
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
    
    return {
        "followers": followers,
        "public_repos": public_repos,
        "total_stars": total_stars
    }

def update_readme(stats):
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    stats_markdown = f"""
<div align="center">
  <img src="https://img.shields.io/badge/Depolar_(Repos)-{stats['public_repos']}-blue?style=for-the-badge&logo=github"/>
  <img src="https://img.shields.io/badge/Yıldızlar_(Stars)-{stats['total_stars']}-yellow?style=for-the-badge&logo=github"/>
  <img src="https://img.shields.io/badge/Takipçi_(Followers)-{stats['followers']}-success?style=for-the-badge&logo=github"/>
</div>
"""
    
    # Replace content between <!-- START_STATS --> and <!-- END_STATS -->
    pattern = r"<!-- START_STATS -->.*<!-- END_STATS -->"
    new_content = re.sub(
        pattern,
        f"<!-- START_STATS -->\n{stats_markdown}\n<!-- END_STATS -->",
        content,
        flags=re.DOTALL
    )
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    USERNAME = "kaanirmak"
    TOKEN = os.getenv("GITHUB_TOKEN")
    
    stats = get_github_stats(USERNAME, TOKEN)
    update_readme(stats)
