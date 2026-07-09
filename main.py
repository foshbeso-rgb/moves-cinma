from s import get_servers_html # التعديل 1: صلحنا الاسم
from flask import Blueprint, render_template, request, make_response
import sections
import tmdb
import s as servers

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    trending = tmdb.get_trending('all') # دي الاكثر رواجا

    # لو فاضية هات الشائع
    if not trending:
        trending = tmdb.get_tmdb("/movie/popular", params={"language": "ar-EG"}).get('results', [])

    movies_ar = tmdb.get_discover('movie', 'with_original_language=ar')[:10]
    series_ar = tmdb.get_discover('tv', 'with_original_language=ar')[:10]
    series_kr = tmdb.get_discover('tv', 'with_origin_country=KR')[:10]
    series_cn = tmdb.get_discover('tv', 'with_origin_country=CN')[:10]
    series_jp = tmdb.get_discover('tv', 'with_origin_country=JP')[:10]

    # 1. انمي كورة = هنسمي انمي ياباني كده
    anime_jp = tmdb.get_discover('tv', 'with_genres=16&with_origin_country=JP')[:15] # زودتها 15

    anime_cn = tmdb.get_discover('tv', 'with_genres=16&with_origin_country=CN')[:10]
    anime_kr = tmdb.get_discover('tv', 'with_genres=16&with_origin_country=KR')[:10]

    html = sections.get_hero(trending[0] if trending else None)

    # 2. هنا ضفنا "الاكثر رواجا" و "انمي كورة"
    html += sections.get_cards(trending[:15], "all", "🔥 الاكثر رواجاً") # 1
    html += sections.get_cards(movies_ar, "movie", "🎬 افلام عربي")
    html += sections.get_cards(series_ar, "tv", "📺 مسلسلات عربي")
    html += sections.get_cards(anime_jp, "tv", "⚽ انمي كورة") # 2 غيرت الاسم بس
    html += sections.get_cards(series_kr, "tv", "🇰🇷 مسلسلات كورية")
    html += sections.get_cards(series_cn, "tv", "🇨🇳 مسلسلات صينية")
    html += sections.get_cards(series_jp, "tv", "🇯🇵 مسلسلات يابانية")
    html += sections.get_cards(anime_cn, "tv", "🇨🇳 انمي صيني")
    html += sections.get_cards(anime_kr, "tv", "🇰🇷 انمي كوري")

    return sections.base(html, "داخلين سينما")

@main_bp.route("/search")
def search():
    query = request.args.get("q")
    if not query: return sections.base("", "بحث")
    data = tmdb.get_tmdb("/search/multi", params={"query": query, "language": "ar-EG"})
    results = data.get("results", [])
    html = sections.get_cards(results, "all", f"نتائج البحث عن: {query}")
    return sections.base(html, f"بحث: {query}")

@main_bp.route("/genre/<int:genre_id>")
@main_bp.route("/genre/<int:genre_id>/page/<int:page>")
def genre(genre_id, page=1):
    genres = {
        28: "اكشن", 12: "مغامرة", 16: "انمي", 35: "كوميدي", 80: "جريمة",
        18: "دراما", 10751: "عائلي", 14: "خيال", 36: "تاريخ", 27: "رعب",
        10402: "موسيقي", 9648: "غموض", 10749: "رومانسي", 878: "خيال علمي",
        10770: "تلفزيوني", 53: "اثارة", 10752: "حرب", 37: "ويسترن",
        10759: "مسلسلات", 10762: "اطفال", 10764: "واقع",
        10765: "خيال علمي و فانتازيا", 10766: "دراما"
    }

    name = genres.get(genre_id, "التصنيف")

    if genre_id in [10759, 18, 35, 10765]:
        results = tmdb.get_tmdb(f"/discover/tv", params={"with_genres": genre_id, "page": page, "sort_by": "popularity.desc", "language": "ar-EG"}).get('results', [])
        media_type = 'tv'
    else:
        results = tmdb.get_tmdb(f"/discover/movie", params={"with_genres": genre_id, "page": page, "sort_by": "popularity.desc", "language": "ar-EG"}).get('results', [])
        media_type = 'movie'

    cards = sections.get_cards(results, media_type, f'{name}')

    pagination = '<div class="pagination">'
    for p in range(1, 6):
        if p == page: pagination += f'<span class="active">{p}</span>'
        else: pagination += f'<a href="/genre/{genre_id}/page/{p}">{p}</a>'
    pagination += '</div>'

    html = f"<div class='watch-container'>{cards}{pagination}</div>"
    return sections.base(html, name)

@main_bp.route("/country/<country_code>")
@main_bp.route("/country/<country_code>/page/<int:page>")
def country(country_code, page=1):
    countries = {"KR": "كوري", "CN": "صيني", "JP": "ياباني", "US": "غربي", "GB": "بريطاني", "EG": "عربي", "TR": "تركي"}
    name = countries.get(country_code, "اجنبي")

    if country_code in ["KR", "JP", "CN", "TR"]:
        results = tmdb.get_tmdb(f"/discover/tv", params={"with_origin_country": country_code, "page": page, "sort_by": "popularity.desc", "language": "ar-EG"}).get('results', [])
        media_type = 'tv'
    else:
        results = tmdb.get_tmdb(f"/discover/movie", params={"with_origin_country": country_code, "page": page, "sort_by": "popularity.desc", "language": "ar-EG"}).get('results', [])
        media_type = 'movie'

    cards = sections.get_cards(results, media_type, f'{name}')

    pagination = '<div class="pagination">'
    for p in range(1, 6):
        if p == page: pagination += f'<span class="active">{p}</span>'
        else: pagination += f'<a href="/country/{country_code}/page/{p}">{p}</a>'
    pagination += '</div>'

    html = f"<div class='watch-container'>{cards}{pagination}</div>"
    return sections.base(html, f"{name}")

@main_bp.route("/anime/<country_code>")
@main_bp.route("/anime/<country_code>/page/<int:page>")
def anime(country_code, page=1):
    countries = {"JP": "ياباني", "CN": "صيني", "KR": "كوري"}
    name = countries.get(country_code, "انمي")

    results = tmdb.get_tmdb(f"/discover/tv", params={
        "with_genres": 16,
        "with_origin_country": country_code,
        "page": page,
        "sort_by": "popularity.desc",
        "language": "ar-EG"
    }).get('results', [])

    cards = sections.get_cards(results, 'tv', f'انمي {name}')

    pagination = '<div class="pagination">'
    for p in range(1, 6):
        if p == page: pagination += f'<span class="active">{p}</span>'
        else: pagination += f'<a href="/anime/{country_code}/page/{p}">{p}</a>'
    pagination += '</div>'

    html = f"<div class='watch-container'>{cards}{pagination}</div>"
    return sections.base(html, f"انمي {name}")

@main_bp.route("/watch/<type>/<id>")
@main_bp.route("/watch/<type>/<id>/<int:season>/<int:episode>")
def watch(type, id, season=1, episode=1):
    details = tmdb.get_details(type, id)
    if not details: return sections.base("<h2>مش موجود</h2>", "خطأ")

    credits = tmdb.get_credits(type, id)
    servers_html = get_servers_html(type, id, season, episode) # التعديل 2: استخدمنا get_servers_html

    content = sections.get_hero(details)

    if type == 'tv' and details.get('seasons'):
        content += sections.get_seasons(details['seasons'], id, season)

    content += sections.get_player(servers_html) # التعديل 3: بعتنا html
    content += sections.get_cast(credits.get('cast', []))

    title = details.get('title') or details.get('name')
    return sections.base(content, title)

@main_bp.route("/watch/tv/<int:id>/season/<int:season>")
def watch_season(id, season):
    details = tmdb.get_tmdb(f"/tv/{id}", params={"language": "ar-EG"})
    season_details = tmdb.get_tmdb(f"/tv/{id}/season/{season}", params={"language": "ar-EG"})
    html = sections.hero(details) + sections.episodes_list(season_details.get('episodes', []), id, season)
    return sections.base(html, f"{details.get('name')} - الموسم {season}")

@main_bp.route("/watch/tv/<int:id>/season/<int:season>/episode/<int:episode>")
def watch_episode(id, season, episode):
    details = tmdb.get_tmdb(f"/tv/{id}", params={"language": "ar-EG"})
    title = details.get('name')
    season_details = tmdb.get_tmdb(f"/tv/{id}/season/{season}", params={"language": "ar-EG"})
    episodes = season_details.get('episodes', [])
    next_url = f"/watch/tv/{id}/season/{season}/episode/{episode + 1}" if episode + 1 <= len(episodes) else ""
    servers_html = get_servers_html("tv", id, season, episode) # التعديل 4: استخدمنا get_servers_html
    next_btn = f'<a href="{next_url}" class="btn next-ep">الحلقة التالية {episode + 1} ▶️</a>' if next_url else ""
    script_tag = f'<script>setTimeout(()=>{{if(confirm("تشغيل الحلقة التالية الان؟")){{window.location.href="{next_url}"}}}},5000)</script>' if next_url else ""
    html = f"""<div class="watch-container"><h1>{title} - الموسم {season} الحلقة {episode}</h1><div style="display:flex;gap:10px;margin-bottom:20px"><a href="/watch/tv/{id}/season/{season}" class="btn back">الرجوع للمواسم</a>{next_btn}</div><div class="player-section"><h2>اختر السيرفر</h2><div class="servers">{servers_html}</div><div class="player-box"><iframe id="player" src="" allowfullscreen></iframe></div></div></div>{script_tag}"""
    return sections.base(html, f"{title} - S{season}E{episode}")

@main_bp.route("/favorites")
def favorites():
    fav_ids = request.cookies.get("favorites", "")
    fav_list = [f for f in fav_ids.split(",") if f and "-" in f]
    results = []
    for fav in fav_list:
        media_type, id = fav.split("-")
        try:
            details = tmdb.get_tmdb(f"/{media_type}/{id}", params={"language": "ar-EG"})
            details['media_type'] = media_type
            if details.get('poster_path'): results.append(details)
        except: continue
    html = sections.get_cards(results, "all", "❤️ المفضلة بتاعتي") if results else """<div class="watch-container" style="text-align:center; padding:50px;"><h2>❤️ المفضلة فاضية</h2></div>"""
    return sections.base(html, "المفضلة")