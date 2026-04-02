import os
import re
import feedparser
import requests

def update_section(content, marker_name, new_data):
    start_marker = f"<!-- {marker_name}-START -->"
    end_marker = f"<!-- {marker_name}-END -->"
    pattern = re.compile(rf"{start_marker}.*?{end_marker}", re.DOTALL)
    return pattern.sub(f"{start_marker}\n{new_data}\n{end_marker}", content)

def get_latest_posts(feed_url):
    feed = feedparser.parse(feed_url)
    # كياخد آخر 5 مقالات
    posts = [f"- [{item.title}]({item.link}) (_{item.published[:16]}_)" for item in feed.entries[:5]]
    return "\n".join(posts) if posts else "No posts found."

def get_latest_releases(username):
    # كيجيب آخر ريليزات من GitHub API
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)
    releases = []
    if response.status_code == 200:
        events = response.json()
        for event in events:
            if event['type'] == 'CreateEvent' and event['payload'].get('ref_type') == 'tag':
                repo_name = event['repo']['name']
                tag_name = event['payload']['ref']
                releases.append(f"- 🚀 New release **{tag_name}** in [{repo_name}](https://github.com/{repo_name})")
            if len(releases) >= 5: break
    return "\n".join(releases) if releases else "No recent releases found."

def main():
    # 1. قرا الـ README الحالي
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    # 2. جيب البيانات الجديدة
    wp_feed = os.environ.get("WP_FEED", "https://woodruff.dev/category/blog/feed/")
    gh_user = os.environ.get("GH_USER", "ayoub-lamliti")

    blog_posts = get_latest_posts(wp_feed)
    gh_releases = get_latest_releases(gh_user)

    # 3. حدث الأقسام (باستعمال الـ Markers اللي درنا ف الـ README)
    readme = update_section(readme, "BLOG", blog_posts)
    readme = update_section(readme, "RELEASES", gh_releases)
    # LinkedIn غالباً كيحتاج Webhook، خليه خاوي دابا ولا دير فيه مساج بسيط
    readme = update_section(readme, "LINKEDIN", "Check my latest newsletters on [LinkedIn](https://www.linkedin.com/).")

    # 4. حفظ التغييرات
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

if __name__ == "__main__":
    main()
