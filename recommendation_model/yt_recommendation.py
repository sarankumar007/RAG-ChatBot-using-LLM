from youtubesearchpython import VideosSearch


def top_url(keyword):
    query = f"{keyword} full tutorial"
    videos_search = VideosSearch(query, limit=1)
    results = videos_search.result()

    if results and 'result' in results and results['result']:
        top_video = results['result'][0]
        video_url = top_video['link']
        return video_url

    return None

def video_keywords(keywords):
    # Use Chrome as the browser (you need to have chromedriver installed)

        video_url = top_url(keywords)

        if video_url:
            return f"Sure, let me open the course for your skillset! \n {video_url}"
        else:
            return (f"No tutorial found for the keyword: {keywords}")





