import requests

def get_comments_from_youtube(video_id, api_key):
    url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100'
    response = requests.get(url)
    data = response.json()
    comments = []

    for item in data.get('items', []):
        top_comment = item['snippet']['topLevelComment']['snippet']
        comments.append({
            'author': top_comment['authorDisplayName'],
            'text': top_comment['textDisplay']
        })

    return comments

VIDEO_ID = '4n-lkYFqXGM'
API_KEY = 'AIzaSyCtRterjnnJxCGDpW4IZ4OrrgL7B5SzzXg'
comments = get_comments_from_youtube(VIDEO_ID, API_KEY)
for comment in comments:
    print(comment['author'], ":", comment['text'])