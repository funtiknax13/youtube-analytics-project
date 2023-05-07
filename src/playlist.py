from datetime import timedelta
import isodate


from src.channel import Youtube


class PlayList(Youtube):

    def __init__(self, playlist_id: str) -> None:
        self.playlist_id = playlist_id
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id
        playlist_items = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                          part='contentDetails, snippet',
                                                          maxResults=50,
                                                          ).execute()
        channel_id = playlist_items["items"][0]["snippet"]["channelId"]
        playlists = self.youtube.playlists().list(channelId=channel_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()
        self.title = ""
        for playlist in playlists['items']:
            if playlist["id"] == playlist_id:
                self.title = playlist["snippet"]["title"]
                break

        video_ids = []
        for video in playlist_items['items']:
            video_ids.append(video['contentDetails']['videoId'])
        self.__video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)).execute()

    @property
    def total_duration(self):
        total_duration = timedelta()
        for video in self.__video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        best_video_like_count = 0
        best_video_id = ""
        for video in self.__video_response['items']:
            like_count = int(video["statistics"]["likeCount"])
            if like_count > best_video_like_count:
                best_video_like_count = like_count
                best_video_id = video["id"]

        return "https://youtu.be/" + best_video_id

