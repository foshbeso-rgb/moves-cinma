from flask import url_for
from s import get_servers, get_servers_html
from markupsafe import Markup
import tmdb

def footer():
    return Markup("""
    <footer style="background: #0a0a0a; color: #ccc; padding: 30px 20px; text-align: center; margin-top: 50px; border-top: 1px solid #222;">
    
        <div class="footer-links" style="margin-bottom: 20px;">
            <a href="/" style="color: #ccc; text-decoration: none; margin: 0 15px; transition:0.3s;" onmouseover="this.style.color='#e50914'" onmouseout="this.style.color='#ccc'">الرئيسية</a>
            <a href="/favorites" style="color: #ccc; text-decoration: none; margin: 0 15px; transition:0.3s;" onmouseover="this.style.color='#e50914'" onmouseout="this.style.color='#ccc'">المفضلة</a>
            <a href="/about" style="color: #ccc; text-decoration: none; margin: 0 15px; transition:0.3s;" onmouseover="this.style.color='#e50914'" onmouseout="this.style.color='#ccc'">من نحن</a>
            <a href="/privacy" style="color: #ccc; text-decoration: none; margin: 0 15px; transition:0.3s;" onmouseover="this.style.color='#e50914'" onmouseout="this.style.color='#ccc'">سياسة الخصوصية</a>
            <a href="/contact" style="color: #ccc; text-decoration: none; margin: 0 15px; transition:0.3s;" onmouseover="this.style.color='#e50914'" onmouseout="this.style.color='#ccc'">اتصل بنا</a>
        </div>
    
        <div class="social-icons" style="margin: 20px 0;">
            <a href="https://facebook.com" target="_blank" style="margin: 0 10px; font-size: 22px; color: #ccc; transition:0.3s;" onmouseover="this.style.color='#1877F2'" onmouseout="this.style.color='#ccc'"><i class="fab fa-facebook-f"></i></a>
            <a href="https://twitter.com" target="_blank" style="margin: 0 10px; font-size: 22px; color: #ccc; transition:0.3s;" onmouseover="this.style.color='#1DA1F2'" onmouseout="this.style.color='#ccc'"><i class="fab fa-twitter"></i></a>
            <a href="https://instagram.com" target="_blank" style="margin: 0 10px; font-size: 22px; color: #ccc; transition:0.3s;" onmouseover="this.style.color='#E4405F'" onmouseout="this.style.color='#ccc'"><i class="fab fa-instagram"></i></a>
        </div>

        <p>© 2026 داخلين سينما. جميع الحقوق محفوظة.</p>
        <p style="margin-top:8px;">تم التطوير بواسطة: <b style="color: white;">Fouad Abbas</b></p>
    </footer>
    """)

def base(content, title="داخلين سينما"):
    return Markup(f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
    
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
        *{{margin:0; padding:0; box-sizing:border-box; font-family:'Cairo', sans-serif;}}
        body{{background:#141414; color:#fff; overflow-x:hidden; padding-top:80px;}}
        a{{color:inherit; text-decoration:none;}}
        
        /* Navbar */
        .navbar{{position:fixed; top:0; width:100%; z-index:999; background: linear-gradient(180deg, rgba(0,0,0,.9) 0%, rgba(0,0,0,0) 100%); padding: 20px 4%; display:flex; justify-content:space-between; align-items:center; transition: background .3s;}}
        .navbar.scrolled{{background:#141414;}}
        .nav-left{{display:flex; align-items:center; gap:30px;}}
        .nav-right{{display:flex; align-items:center; gap:20px;}}
        .logo{{color:#E50914; font-size:28px; font-weight:900; text-decoration:none;}}
        .nav-links{{display:flex; gap:20px;}}
        .nav-links a{{color:#e5e5e5; text-decoration:none; font-weight:500; font-size:15px;}}
        .nav-links a:hover{{color:#fff;}}

        /* Dropdown Fix */
        .dropdown{{position:relative;}}
        .dropdown-content{{display:none; position:absolute; background:#181818; padding:10px; border-radius:4px; top:100%; right:0; min-width:180px; margin-top:5px; z-index:1000;}}
        .dropdown:hover .dropdown-content{{display:block;}}
        .dropdown-content a{{display:block; padding:8px 5px;}}
        .dropdown-content a:hover{{background:#222;}}

        /* Search */
        .search-form{{display:flex; background:#222; border-radius:4px; overflow:hidden;}}
        .search-form input{{background:transparent; border:none; color:#fff; padding:8px 15px; width:220px; outline:none;}}
        .search-form input::placeholder{{color:#aaa;}}
        .search-form button{{background:#E50914; border:none; color:#fff; padding:8px 15px; cursor:pointer; font-size:16px;}}
        .search-form button:hover{{background:#b0060f;}}
        
        /* Hero */
        .hero{{height:85vh; background-size:cover; background-position:center; position:relative; margin-top:-80px;}}
        .hero-overlay{{position:absolute; top:0; left:0; right:0; bottom:0; background:linear-gradient(to top, #141414 10%, transparent 90%);}}
        .hero-inner{{position:absolute; bottom:15%; right:4%; width:40%; z-index:2;}}
        .hero-inner h1{{font-size:3vw; margin-bottom:20px;}}
        .hero-desc{{font-size:1.1vw; margin-bottom:20px; line-height:1.5;}}
        .hero-meta{{display:flex; gap:15px; margin-bottom:20px;}}
        .rate-badge{{background:#E50914; padding:5px 10px; border-radius:4px; font-weight:700;}}
        .btn{{padding:10px 25px; border:none; border-radius:4px; font-size:1.1vw; font-weight:700; cursor:pointer; margin-left:10px; background:#333; color:#fff;}}
        .btn.play{{background:#fff; color:#000;}}
        .btn.play:hover{{background:#e6e6e6;}}
        .btn.fav{{background:rgba(109,109,110,.7); color:#fff;}}
        .btn.fav:hover{{background:rgba(109,109,110,.9);}}
        .btn.active{{background:#E50914;}}
        a.btn{{display:inline-block;}}
        
        /* Back Button */
        .back-btn{{position:absolute; top:100px; right:4%; z-index:100; background:rgba(109,109,110,.7); padding:10px 20px; border-radius:30px; color:#fff; font-weight:700; text-decoration:none; backdrop-filter: blur(10px); display:flex; align-items:center; gap:8px;}}
        .back-btn:hover{{background:rgba(109,109,110,.9);}}

        /* Cards */
        .section{{padding:30px 0;}} /* شلت 4% من هنا */
        .section h2{{margin-bottom:15px; font-size:1.4vw; padding:0 4%;}} /* حطيت البادينج على العنوان */
        
        .cards-container.grid{{display:grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap:15px; padding: 0 4%;}}
        
        .card{{position:relative; overflow:hidden; transition:transform .3s; border-radius:4px;}}
        .card:hover{{transform:scale(1.08); z-index:10;}}
        .card img{{width:100%; border-radius:4px; aspect-ratio:2/3; object-fit:cover;}}
        .card-info{{
            position:absolute; bottom:0; left:0; right:0;
            background:linear-gradient(to top, rgba(0,0,0,.95) 0%, transparent 100%);
            padding:10px; opacity:0; transition:all .3s;
            transform:translateY(100%);
        }}
        .card:hover .card-info{{opacity:1; transform:translateY(0);}}
        .card-info h3{{font-size:14px; margin-bottom:5px; color:#fff;}}
        .card-meta{{font-size:12px; color:#E50914; margin-bottom:5px; font-weight:700;}}
        .card-info p{{font-size:11px; color:#ccc; margin-bottom:8px; height:35px; overflow:hidden;}}
        .card-info .btn{{font-size:12px; padding:6px 10px; width:100%; margin:0;}}

        /* اسكرول للرئيسية */
        .row-container{{position:relative; display:flex; align-items:center; padding:0 4%;}} /* البادينج هنا */
        .cards-container.scroll{{
            display:flex; 
            overflow-x:auto; 
            overflow-y:hidden;
            gap:15px; 
            padding:10px 0; /* مسافة فوق وتحت بس */
            scroll-behavior:smooth;
            width:100%;
        }}
        .cards-container.scroll::-webkit-scrollbar{{display:none;}}
        .cards-container.scroll .card{{width:200px; min-width:200px; flex-shrink:0;}} /* min-width مهم جدا */

        .scroll-btn{{position:absolute; z-index:20; background:rgba(0,0,0,.7); border:none; color:#fff; font-size:30px; width:50px; height:100%; cursor:pointer; opacity:0; transition:opacity .3s; top:0;}}
        .row-container:hover .scroll-btn{{opacity:1;}}
        .scroll-btn.left{{left:0;}} 
        .scroll-btn.right{{right:0;}}

        /* Cast */
        .cast-container{{display:flex; gap:15px; overflow-x:auto; padding-bottom:10px; padding: 0 4%;}}
        .cast-container::-webkit-scrollbar{{display:none;}}
        .cast-card{{min-width:120px; width:120px; text-align:center; flex-shrink:0;}}
        .cast-card img{{width:100%; border-radius:8px; aspect-ratio:2/3; object-fit:cover;}}
        .cast-card h3{{font-size:12px; margin-top:8px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}}

        /* Pagination */
        .pagination{{display:flex; justify-content:center; gap:10px; padding:40px;}}
        .pagination a{{padding:10px 15px; background:#333; border-radius:4px;}}
        .pagination a.active{{background:#E50914;}}

        /* Footer */
        .footer{{background:#000; padding:40px 4%; margin-top:50px; border-top:1px solid #222; text-align:center;}}
        .footer-links{{display:flex; justify-content:center; gap:20px; margin-bottom:20px; flex-wrap:wrap;}}
        .footer-links a{{color:#757575; font-size:14px;}}
        .footer-links a:hover{{color:#fff; text-decoration:underline;}}
        .footer p{{color:#757575; font-size:13px;}}
        
        /* ده كان مبوظ الدنيا - مسحته */
        @media(max-width:900px){{.search-form input{{width:120px;}}}}
        @media(max-width:768px){{
            .nav-links{{display:none;}}
            .search-form{{display:none;}}
            .hero-inner{{width:90%;}}
            .hero-inner h1{{font-size:6vw;}}
            .hero-desc{{font-size:3vw;}}
            .btn{{font-size:3.5vw;}}
            .cards-container.grid{{grid-template-columns: repeat(2, 1fr);}}
            .cards-container.scroll .card{{width:45%; min-width:45%;}} /* خليته سكرول برضو في الموبايل */
        }}
        </style>
    </head>
    
    <body>
        {navbar()}
        {content}
        {footer()}
        <script>
        document.querySelectorAll('.row-container').forEach(row => {{
            const container = row.querySelector('.cards-container.scroll');
            const btnLeft = row.querySelector('.scroll-btn.left');
            const btnRight = row.querySelector('.scroll-btn.right');
            
            if(container && btnLeft && btnRight){{
                btnRight.addEventListener('click', () => {{
                    container.scrollBy({{left: 400, behavior: 'smooth'}});
                }});
                btnLeft.addEventListener('click', () => {{
                    container.scrollBy({{left: -400, behavior: 'smooth'}});
                }});
            }}
        }});

        async function addFav(id){{
            let [type, id_num] = id.split('-');
            let res = await fetch(`/add_favorite/${{type}}/${{id_num}}`);
            let data = await res.json();
            if(data.status == 'added'){{
                alert('تمت الاضافة للمفضلة');
            }} else {{
                alert('تم الحذف من المفضلة');
            }}
        }}

        window.onscroll = function() {{
            let navbar = document.getElementById("navbar");
            if(navbar){{
                if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {{
                    navbar.classList.add("scrolled");
                }} else {{
                    navbar.classList.remove("scrolled");
                }}
            }}
        }};
        </script>
    </body>
    </html>
    """)

def navbar():
    return Markup("""
    <div class="navbar" id="navbar">
        <div class="nav-left">
            <a href="/" class="logo">داخلين سينما</a>
            <div class="nav-links">
                <a href="/">الرئيسية</a>
                
                <div class="dropdown">
                    <a href="#">أفلام ▾</a>
                    <div class="dropdown-content">
                        <b style="padding:8px 5px; color:#E50914; display:block;">حسب الدولة</b>
                        <a href="/discover/movie?with_original_language=ar">🇪🇬 افلام عربي</a>
                        <a href="/discover/movie?with_origin_country=US">🇺🇸 افلام اجنبي</a>
                        <a href="/discover/movie?with_origin_country=TR">🇹🇷 افلام تركي</a>
                        <a href="/discover/movie?with_origin_country=KR">🇰🇷 افلام كوري</a>
                        <a href="/discover/movie?with_origin_country=JP">🇯🇵 افلام ياباني</a>
                        <a href="/discover/movie?with_origin_country=CN">🇨🇳 افلام صيني</a>
                        <a href="/discover/movie?with_origin_country=IN">🇮🇳 افلام هندي</a>
                    </div>
                </div>

                <div class="dropdown">
                    <a href="#">مسلسلات ▼</a>
                    <div class="dropdown-content">
                        <b style="padding:8px 5px; color:#E50914; display:block;">حسب الدولة</b>
                        <a href="/discover/tv?with_origin_country=EG">🇪🇬 مسلسلات مصري</a>
                        <a href="/discover/tv?with_origin_country=TR">🇹🇷 مسلسلات تركي</a>
                        <a href="/discover/tv?with_origin_country=KR">🇰🇷 دراما كوري</a>
                        <a href="/discover/tv?with_origin_country=CN">🇨🇳 دراما صيني</a>
                        <a href="/discover/tv?with_origin_country=JP">🇯🇵 دراما ياباني</a>
                        <a href="/discover/tv?with_genres=16">🧸 انمي</a>
                    </div>
                </div>
                
                <a href="/favorites">❤️ المفضلة</a>
            </div>
        </div>
        <div class="nav-right">
            <form action="/search" method="get" class="search-form">
                <input type="text" name="q" placeholder="ابحث..." required>
                <button type="submit">🔍</button>
            </form>
        </div>
    </div>
    """)

def get_hero(item):
    if not item or not isinstance(item, dict): return Markup('')
    title = item.get('title') or item.get('name') or 'بدون عنوان'
    overview = item.get('overview', 'لا يوجد وصف')
    backdrop = f"{tmdb.IMG_BASE}original{item['backdrop_path']}" if item.get('backdrop_path') else ''
    year = item.get('release_date', item.get('first_air_date', ''))[:4]
    rate = round(item.get('vote_average', 0), 1)
    id = item.get('id', 0)
    m_type = item.get('media_type', 'movie')
    return Markup(f"""
    <a href="javascript:history.back()" class="back-btn">⬅️ رجوع</a>
    <div class="hero" style="background-image:url('{backdrop}');">
        <div class="hero-overlay"></div>
        <div class="hero-inner">
            <h1>{title}</h1>
            <div class="hero-meta">
                <span class="rate-badge">⭐ {rate}</span>
                <span class="year">{year}</span>
            </div>
            <p class="hero-desc">{overview[:250]}...</p>
            <button class="btn play" onclick="window.location.href='/watch/{m_type}/{id}'">▶ تشغيل</button>
            <button class="btn fav" onclick="addFav('{m_type}-{id}')">❤️ المفضلة</button>
        </div>
    </div>
    """)

def get_card(item):
    if not item or not isinstance(item, dict): return ''
    
    title = item.get('title') or item.get('name') or "بدون اسم"
    poster = item.get('poster_path')
    img = f"{tmdb.IMG_BASE}w500{poster}" if poster else "https://placehold.co/500x750/141414/555?text=No+Image"
    
    id = item.get('id', 0)
    m_type = item.get('media_type') 
    if not m_type:
        m_type = 'tv' if item.get('first_air_date') else 'movie'
        
    rate = round(item.get('vote_average', 0), 1)
    year = (item.get('release_date') or item.get('first_air_date') or '')[:4]
    overview = (item.get('overview', '')[:90] + '...') if item.get('overview') else ''

    return f"""
    <div class="card">
        <a href="/watch/{m_type}/{id}">
            <img src="{img}" alt="{title}">
            <div class="card-info">
                <h3>{title}</h3>
                <div class="card-meta">⭐ {rate} | {year}</div>
                <p>{overview}</p>
                <button class="btn play">▶ تشغيل</button>
            </div>
        </a>
    </div>
    """

def get_cards(items, media_type, title, scroll=True):
    if not items: return ''
    container_class = "scroll" if scroll else "grid"
    cards_html = "".join([get_card(item) for item in items])
    
    more_link = "#"
    if title == "⭐ الاعلى تقييماً": 
        more_link = "/genre/0?sort=vote_average.desc"
    elif title == "🎬 قريبا في السينما": 
        more_link = "/upcoming"
    elif title == "⚽ انمي كورة": 
        more_link = "/discover/tv?with_genres=16&with_keywords=football"
    elif title == "🔥 الاكثر رواجاً":
        more_link = "/"
    
    return Markup(f"""
    <div class="section">
        <h2>{title} <a href="{more_link}" style="font-size:14px; color:#E50914; float:left;">عرض الكل ›</a></h2>
        <div class="row-container">
            <button class="scroll-btn left">‹</button>
            <div class="cards-container {container_class}">
                {cards_html}
            </div>
            <button class="scroll-btn right">›</button>
        </div>
    </div>
    """)

from markupsafe import Markup

def get_player(servers_html):
    return Markup(f'''
    <div class="section">
        <h2>السيرفرات</h2>
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:20px;">
            {servers_html}
        </div>
        <div class="player" id="player-container">
            <button onclick="toggleFullscreen()" style="position:absolute; top:10px; right:10px; z-index:100; padding:8px 12px; background:#E50914; color:#fff; border:none; border-radius:6px; cursor:pointer; font-weight:bold;">⛶ تكبير</button>
            <iframe id="player-frame" src="" frameborder="0" allowfullscreen allow="autoplay; fullscreen; picture-in-picture; encrypted-media" style="width:100%; height:80vh; border-radius:8px; background:#000;"></iframe>
        </div>
    </div>
    <script>
    function loadServer(url, btn){{
        document.getElementById('player-frame').src = url;
        document.querySelectorAll('.server-btn').forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');
    }}

    function toggleFullscreen() {{
        let elem = document.getElementById("player-container");
        if (!document.fullscreenElement) {{
            elem.requestFullscreen();
        }} else {{
            document.exitFullscreen();
        }}
    }}

    window.onload = () => {{
        let firstBtn = document.querySelector('.server-btn');
        if(firstBtn) firstBtn.click();
    }}
    </script>
    <style>
    .server-btn {{
        padding:10px 15px; background:#222; color:#fff; border:none; 
        border-radius:6px; cursor:pointer; font-weight:bold;
    }}
    .server-btn.active {{ background:#E50914 !important; }}
    .server-btn:hover {{ background:#333; }}
    .player{{position:relative;}}
    #player-frame {{height:80vh;}}
    </style>
    ''')

    def get_servers(id, media_type, season=1, episode=1):
    if media_type == 'movie':
        return [
            ('▶️ سيرفر 1 - Vidsrc.su AR', f'https://vidsrc.su/embed/movie/{id}/ar'),
            ('▶️ سيرفر 2 - SuperEmbed', f'https://multiembed.mov/?video_id={id}&tmdb=1&lang=ar&sublang=ar'),
            ('▶️ سيرفر 3 - VidSrc.to', f'https://vidsrc.to/embed/movie/{id}'),
            ('▶️ سيرفر 4 - Smiles', f'https://www.2embed.cc/embed/movie/{id}'),
            ('▶️ سيرفر 5 - VidLink', f'https://vidlink.pro/movie/{id}'),
        ]
    else:
        return [
            ('▶️ سيرفر 1 - Vidsrc.su AR', f'https://vidsrc.su/embed/tv/{id}/{season}/{episode}/ar'),
            ('▶️ سيرفر 2 - SuperEmbed', f'https://multiembed.mov/?video_id={id}&tmdb=1&s={season}&e={episode}&lang=ar&sublang=ar'),
            ('▶️ سيرفر 3 - VidSrc.to', f'https://vidsrc.to/embed/tv/{id}/{season}/{episode}'),
            ('▶️ سيرفر 4 - Smiles', f'https://www.2embed.cc/embed/tv/{id}&s={season}&e={episode}'),
            ('▶️ سيرفر 5 - VidLink', f'https://vidlink.pro/tv/{id}/{season}/{episode}'),
        ]

def get_servers_html(servers, id, media_type, season=1, episode=1):
    html = ''
    for name, url in servers:
        html += f'<button class="server-btn" onclick="loadServer(\'{url}\', this)">{name}</button>'
    return html
        
def get_cast(cast):
    if not cast: return Markup('')
    actors = ''.join([f'<a href="/search?q={c["name"]}" class="cast-card"><img src="{tmdb.IMG_BASE}w185{c["profile_path"]}"><h3>{c["name"]}</h3></a>' for c in cast[:15] if c.get('profile_path')])
    return Markup(f'<div class="section"><h2>الممثلين</h2><div class="cast-container">{actors}</div></div>')

def get_pagination(page, total_pages, base_url):
    if '?' in base_url:
        links = ''.join([f'<a href="{base_url}&page={i}" class="{"active" if i==page else ""}">{i}</a>' for i in range(1, min(total_pages+1, 11))])
    else:
        links = ''.join([f'<a href="{base_url}?page={i}" class="{"active" if i==page else ""}">{i}</a>' for i in range(1, min(total_pages+1, 11))])
    return Markup(f'<div class="pagination">{links}</div>')

def get_episodes(seasons, show_id, current_season, current_episode):
    html = '<div style="padding:20px; direction:rtl;">'
    for season in seasons:
        season_num = season['season_number']
        if season_num == 0: continue
        season_data = tmdb.get_season_details(show_id, season_num)
        episodes = season_data.get('episodes', [])
        html += f'<h3 style="color:#e50914; margin-top:30px;">الموسم {season_num}</h3>'
        html += '<div style="display:flex; flex-wrap:wrap; gap:10px;">'
        for ep in episodes:
            ep_num = ep['episode_number']
            ep_name = ep.get('name', f'الحلقة {ep_num}')
            active = 'background:#e50914; color:white;' if season_num == current_season and ep_num == current_episode else 'background:#222; color:#ddd;'
            html += f'<a href="/watch/tv/{show_id}/{season_num}/{ep_num}" style="padding:10px 15px; border-radius:8px; text-decoration:none; font-weight:bold; {active}" title="{ep_name}">{ep_num}</a>'
        html += '</div>'
    html += '</div>'
    return Markup(html)

def get_favorites():
    return Markup("""
    <div style="padding-top:20px;">
        <h2 style='padding:0 4% 20px;'>❤️ قائمة المفضلة</h2>
        <div id='fav-container' class='cards-container grid' style='padding:0 4%;'>
            <p>جاري تحميل المفضلة...</p>
        </div>
    </div>
    <script>
    async function removeFav(id, type, cardElement){
        if(confirm('عايز تحذف ده من المفضلة؟')){
            let res = await fetch(`/remove_favorite/${type}/${id}`);
            let data = await res.json();
            if(data.status == 'removed'){
                cardElement.remove();
                alert('تم الحذف من المفضلة');
            }
        }
    }
    async function loadFavs(){
        let res = await fetch('/api/favorites');
        let favs = await res.json();
        let container = document.getElementById('fav-container');
        if(favs.length === 0){
            container.innerHTML = "<p>لسه مضفتش حاجة للمفضلة</p>";
            return;
        }
        container.innerHTML = '';
        favs.forEach(item => {
            let title = item.title || item.name;
            let img = item.poster_path ? 'https://image.tmdb.org/t/p/w500' + item.poster_path : '';
            let rate = item.vote_average ? item.vote_average.toFixed(1) : '0';
            let year = item.release_date ? item.release_date.substring(0,4) : item.first_air_date ? item.first_air_date.substring(0,4) : '';
            let link = `/watch/${item.media_type}/${item.id}`;
            container.innerHTML += `
            <div class="card" id="fav-${item.media_type}-${item.id}">
                <a href="${link}">
                    <img src="${img}" alt="${title}">
                    <div class="card-info">
                        <h3>${title}</h3>
                        <div class="card-meta">⭐ ${rate} | ${year}</div>
                        <button class="btn play">▶ تشغيل</button>
                    </div>
                </a>
                <button onclick="removeFav(${item.id}, '${item.media_type}', this.closest('.card'))" 
                        style="position:absolute; top:5px; left:5px; z-index:20; background:#E50914; color:#fff; border:none; padding:5px 10px; border-radius:4px; cursor:pointer; font-size:12px;">
                    🗑️ حذف
                </button>
            </div>`;
        });
    }
    loadFavs();
    </script>
    """)
