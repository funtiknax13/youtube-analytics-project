import os

from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id
        __video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                         id=video_id).execute()
        self.title = __video["items"][0]["snippet"]["title"]
        self.url = "https://www.youtube.com/video/" + self.__video_id
        self.view_count = __video["items"][0]["statistics"]["viewCount"]
        self.like_count = __video["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
