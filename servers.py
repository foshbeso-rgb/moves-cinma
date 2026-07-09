def get_servers(media_type, media_id, season=None, episode=None):
    if media_type == "movie":
        return [
            {"name": "سيرفر 1", "url": f"https://vidsrc.xyz/embed/movie/{media_id}"},
            {"name": "سيرفر 2", "url": f"https://vidlink.pro/movie/{media_id}"},
            {"name": "سيرفر 3", "url": f"https://multiembed.mov/directstream.php?video_id={media_id}"},
            {"name": "سيرفر 4", "url": f"https://www.2embed.cc/embed/{media_id}"},
            {"name": "سيرفر 5", "url": f"https://smashy.stream/m/{media_id}"},
        ]
    else:
        return [
            {"name": "سيرفر 1", "url": f"https://vidsrc.xyz/embed/tv/{media_id}/{season}-{episode}"},
            {"name": "سيرفر 2", "url": f"https://vidlink.pro/tv/{media_id}/{season}/{episode}"},
            {"name": "سيرفر 3", "url": f"https://multiembed.mov/directstream.php?video_id={media_id}&s={season}&e={episode}"},
            {"name": "سيرفر 4", "url": f"https://www.2embed.cc/embedtv/{media_id}&s={season}&e={episode}"},
            {"name": "سيرفر 5", "url": f"https://smashy.stream/s/{media_id}/{season}/{episode}"},
        ]