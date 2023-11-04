from googleapiclient.discovery import build
import re
import pandas as pd

api_key = ""

def get_video_comments(youtube_link):
    # Extract the video ID from the YouTube link
    video_id = re.search(r'(?<=v=)[^&]+', youtube_link)
    if video_id:
        video_id = video_id.group(0)
    else:
        # Handle invalid or unsupported YouTube link
        return []

    # Initialize the YouTube Data API
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Request video comments
    comments = []
    nextPageToken = None
    while True:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            pageToken=nextPageToken
        ).execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break
    comments = pd.DataFrame({'Comment': comments})
    return comments

#comments = get_video_comments("https://www.youtube.com/watch?v=x5trGVMKTdY&list=PLhQjrBD2T380xvFSUmToMMzERZ3qB5Ueu&index=8")
#print(comments.head(5))
#print(comments.columns)