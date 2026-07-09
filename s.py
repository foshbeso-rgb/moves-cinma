from markupsafe import Markup

def get_servers(media_type, id, season=1, episode=1):
    base_params = "&lang=ar&sublang=ar"

    if media_type == 'movie':
        return [
            {'name': 'سيرفر 1 - VidSrc', 'url': f"https://vidsrc.to/embed/movie/{id}"},
            {'name': 'سيرفر 2 - SuperEmbed', 'url': f"https://multiembed.mov/?video_id={id}&tmdb=1{base_params}"},
            {'name': 'سيرفر 3 - MoviesAPI', 'url': f"https://moviesapi.club/movie/{id}{base_params}"},
            {'name': 'سيرفر 4 - MultiEmbed', 'url': f"https://multiembed.mov/directstream.php?video_id={id}&tmdb=1{base_params}"},
            {'name': 'سيرفر 5 - Smashes', 'url': f"https://smashes.to/e/{id}{base_params}"},
            {'name': 'سيرفر 6 - VidEasy', 'url': f"https://player.videasy.net/movie/{id}"}, # الجديد
            {'name': 'سيرفر 7 - AutoEmbed', 'url': f"https://player.autoembed.cc/embed/movie/{id}"}, # الجديد
        ]
    else: # tv
        return [
            {'name': 'سيرفر 1 - VidSrc', 'url': f"https://vidsrc.to/embed/tv/{id}/{season}/{episode}"},
            {'name': 'سيرفر 2 - SuperEmbed', 'url': f"https://multiembed.mov/?video_id={id}&tmdb=1&s={season}&e={episode}{base_params}"},
            {'name': 'سيرفر 3 - MoviesAPI', 'url': f"https://moviesapi.club/serie/{id}/{season}/{episode}{base_params}"},
            {'name': 'سيرفر 4 - MultiEmbed', 'url': f"https://multiembed.mov/directstream.php?video_id={id}&tmdb=1&s={season}&e={episode}{base_params}"},
            {'name': 'سيرفر 5 - Smashes', 'url': f"https://smashes.to/e/{id}?s={season}&e={episode}{base_params}"},
            {'name': 'سيرفر 6 - VidEasy', 'url': f"https://player.videasy.net/tv/{id}/{season}/{episode}"}, # الجديد
            {'name': 'سيرفر 7 - AutoEmbed', 'url': f"https://player.autoembed.cc/embed/tv/{id}-{season}-{episode}"}, # الجديد
        ]

def get_servers_html(media_type, id, season=1, episode=1):
    servers = get_servers(media_type, id, season, episode)
    html = ""
    for i, server in enumerate(servers):
        active = "active" if i == 0 else ""
        html += f'''
        <div class="server-btn {active}">
            <button onclick="loadServer('{server['url']}', this)">{server['name']}</button>
        </div>
        '''
    if not html:
        html = '<p class="no-servers">كل السيرفرات واقعة للفيلم ده حاليا 😢</p>'
    return Markup(html)