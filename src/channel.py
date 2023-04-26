import os
import json

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        __channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = __channel["items"][0]["snippet"]["title"]
        self.description = __channel["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/channel/" + self.__channel_id
        self.subscriber_count = __channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = __channel["items"][0]["statistics"]["videoCount"]
        self.view_count = __channel["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    @classmethod
    def get_service(cls) -> None:
        """Выводит в консоль информацию о канале."""
        return cls.youtube

    @property
    def channel_id(self):
        """получает приватную переменную channel_id"""
        return self.__channel_id

    def to_json(self, file):
        """записывает информацию о канале в json файл"""
        with open(file, "w") as json_file:
            data = {"id": self.__channel_id,
                    "title": self.title,
                    "description": self.description,
                    "url": self.url,
                    "subscriberCount": self.subscriber_count,
                    "videoCount": self.video_count,
                    "viewCount": self.view_count}
            json_file.write(json.dumps(data, ensure_ascii=False))




