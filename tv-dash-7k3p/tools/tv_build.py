"""Build the @tripvibeuz dashboard from the Mukhlisa dashboard skeleton + tripvibe data."""
import re, sys, importlib.util, html
sys.path.insert(0, "/home/claude/tv")
from tv_topics import TOPICS, FORMATS

SRC = "/home/claude/app/index.html"
OUT = "/home/claude/tv/index.html"
BOT = "timurblog222024_bot"
E = html.escape
s = open(SRC, encoding="utf-8").read()


def section(sid, inner):
    global s
    a = s.index(f'<section id="{sid}"')
    a2 = s.index(">", a) + 1
    b = s.index("</section>", a2)
    s = s[:a2] + inner + s[b:]


# ---------- head / header ----------
s = s.replace("<title>Mukhlisa · дешборд аккаунта</title>", "<title>Timur · @tripvibeuz дешборд</title>")
s = re.sub(r'<div class="ava">M</div>\s*<div>\s*<div class="h-name">@mukhlisasadikova_</div>\s*<div class="h-sub">.*?</div>',
           '<div class="ava" style="background:linear-gradient(135deg,#9cc8f5,#1c5cab)">T</div>\n  <div>\n    <div class="h-name">@tripvibeuz</div>\n    <div class="h-sub">2 429 подписчиков · 80 публикаций · данные Windsor на 4 ноября 2026</div>',
           s, count=1, flags=re.S)
s = s.replace("--accent:#c2457a; --accent-soft:#fbeaf1;", "--accent:#1c5cab; --accent-soft:#e8f1fc;")

# ---------- overview ----------
section("s-overview", '''
  <h2>Последние 30 дней</h2>
  <p class="lead">5 октября – 3 ноября. Сравнение с прошлым срезом Windsor (21 июля – 19 августа).</p>
  <div class="kpis">
    <div class="kpi"><div class="l">Просмотры</div><div class="v">1 813 349</div><div class="d"><span class="pill up">▲ ×24</span> было 76 173</div></div>
    <div class="kpi"><div class="l">Новые подписчики</div><div class="v">+778</div><div class="d"><span class="pill up">▲ ×15</span> было +51</div></div>
    <div class="kpi"><div class="l">Подписок на 1 000 просмотров</div><div class="v">0,43</div><div class="d"><span class="pill down">⚠ низко</span> цель — 1,0+</div></div>
    <div class="kpi"><div class="l">Взаимодействия</div><div class="v">193 405</div><div class="d"><span class="pill up">✓ 10,7%</span> ER к просмотрам</div></div>
    <div class="kpi"><div class="l">Репосты</div><div class="v">15 691</div><div class="d">главный двигатель охвата</div></div>
    <div class="kpi"><div class="l">Подписчики сейчас</div><div class="v">2 429</div><div class="d"><span class="pill up">▲ +769</span> с 20 августа (1 660)</div></div>
  </div>
  <div class="card">
    <h3>Просмотры по дням</h3>
    <div class="chart" id="viewsChart"><div class="tip"></div></div>
    <p class="muted">Пик 19–22 октября — «Sakinat» (1,49 млн). После хита «пол» вырос в 5 раз: 5,7 тыс. просмотров в день до 19 октября → 28 тыс. с 26 октября.</p>
  </div>
  <div class="card">
    <h3>Главное в трёх пунктах</h3>
    <ul class="clean">
      <li><b>Вирусность есть, конверсии нет.</b> Просмотров в день стало в 5 раз больше, а подписчиков в обычный день — те же ~11 (10,7 до хита, 11,4 после). Профиль не объясняет, зачем подписываться.</li>
      <li><b>Охват держат 4 ролика из 24 — 95% просмотров.</b> 15 роликов ниже 5 тыс. Решают первые 3 секунды: при уходе &lt;35% медиана 271 тыс., при ≥50% — 2,2 тыс. (12 роликов).</li>
      <li><b>Пауза в самый дорогой момент.</b> С 30 октября — ни одного ролика, при том что «пол» после хита ещё высокий. План: 4 Reels в неделю по форматам F1–F4.</li>
    </ul>
  </div>
''')

# ---------- content ----------
section("s-content", '''
  <h2>Что работает, а что нет</h2>
  <p class="lead">24 ролика за 90 дней (30 августа – 30 октября). Сравнения — по медиане, чтобы один хит не искажал картину.</p>
  <div class="card"><h3>Ключевые сравнения</h3><div class="cmp" id="cmp"></div></div>
  <div class="card">
    <h3>Публикации по месяцам</h3>
    <table class="t"><thead><tr><th>Месяц</th><th class="r">Роликов</th><th class="r">Медиана</th><th class="r">Сумма просмотров</th></tr></thead>
    <tbody>
      <tr><td>Август (с 30-го)</td><td class="r">2</td><td class="r">2 589</td><td class="r">5 177</td></tr>
      <tr><td>Сентябрь</td><td class="r">7</td><td class="r">2 727</td><td class="r">256 440</td></tr>
      <tr><td>Октябрь</td><td class="r">15</td><td class="r">4 413</td><td class="r">1 995 993</td></tr>
      <tr><td>Ноябрь</td><td class="r">0</td><td class="r">—</td><td class="r">—</td></tr>
    </tbody></table>
    <p class="muted">Медиана ролика — 3 381 просмотр. 4 ролика больше 100 тыс., 15 — меньше 5 тыс.</p>
  </div>
  <div class="card"><h3>Топ-6 по просмотрам</h3><div id="top"></div></div>
  <div class="card"><h3>Топ по сохранениям</h3><div id="saves"></div></div>
  <div class="card"><h3>Провалы: чему не повторяться</h3><div id="flop"></div>
    <p class="muted">Общее: первый кадр без вопроса и без «вау», в подписи только эмодзи или длинное эссе, половина зрителей уходит в первые 3 секунды. Ролик про Claude/Instagram — не тема @tripvibeuz.</p></div>
''')

# ---------- audience ----------
section("s-aud", '''
  <h2>Кто подписан</h2>
  <p class="lead">Данные по всем подписчикам. Пол Instagram определил у 1 384 из 2 424.</p>
  <div class="kpis">
    <div class="kpi"><div class="l">Мужчины (где пол известен)</div><div class="v">77%</div><div class="d">1 069 из 1 384</div></div>
    <div class="kpi"><div class="l">Возраст 25–44</div><div class="v">62%</div><div class="d">1 496 подписчиков</div></div>
  </div>
  <div class="card"><h3>Возраст</h3><div class="bars" id="ages"></div></div>
  <div class="card"><h3>Топ городов</h3><div class="bars" id="cities"></div>
    <p class="muted">Ташкент — 4%, основная аудитория — регионы (Янгиер, Зарафшан, Ургенч, Ромитан, Навои). За рубежом: Москва, Семнан и Мешхед (Иран), Стамбул, Шымкент. Для контента: цены в сумах, вылеты из Ташкента, поезда из регионов.</p></div>
''')

# ---------- audit ----------
section("s-audit", '''
  <h2>Жёсткий разбор профиля</h2>
  <p class="lead">Промт 1. Шапка и подписи взяты из Windsor. Аватар и Highlights API не отдаёт — пришли скриншот в бот, допишу.</p>
  <div class="card">
    <h3>1. Первый экран: впечатление за 3 секунды</h3>
    <ul class="clean">
      <li><b>Имя «TIMUR SADIKOV | O'ZBEKISTON VA DUNYO BO'YLAB SAYOHAT🇺🇿» слишком длинное</b> и в Reels обрезается. Слово «sayohat» для поиска полезное, остальное — шум.</li>
      <li><b>В шапке нет обещания.</b> «Dunyo bo'ylab sayohat / Parvozlar, mehmonxonalar va Lifehacklar» — так может написать любой. В августе было «aniq raqamlar» (точные цифры) — это и было твоим отличием, сейчас его нет. Фирменной фразы «Shuncha pulga?!» тоже нет.</li>
      <li><b>Ссылка ведёт на YouTube.</b> Там 1 видео, монетизации в Узбекистане нет. Новому человеку из Reels нужно что-то получить сразу: локации, списки, Telegram.</li>
      <li><b>Вирусные ролики — спокойные пейзажи</b> («Sakinat», «🐻»), а шапка обещает лайфхаки. Зритель не видит связи и уходит.</li>
    </ul>
    <p style="margin:12px 0 6px;font-weight:600;font-size:14px">Вариант шапки:</p>
    <div class="bio">Имя: Timur | Sayohat byudjeti 🇺🇿
Био:
Qayerga borish va qancha ketishini aniq raqamlarda ko'rsataman ✈️
«Shuncha pulga?!» — har hafta yangi yo'nalish
🎁 Lokatsiyalar va ro'yxatlar — Telegramda 👇
Hamkorlik: Direct</div>
  </div>
  <div class="card">
    <h3>2. Контент и подача</h3>
    <ul class="clean">
      <li><b>Хиты случаются, но не повторяются.</b> 4 из 24 роликов дают 95% просмотров, медиана — 3,4 тыс.</li>
      <li><b>Первые 3 секунды слабые в половине роликов.</b> 12 из 24 теряют ≥50% зрителей сразу, их медиана — 2,2 тыс.</li>
      <li><b>Экспертность сидит в подписи, а не в видео.</b> «4 мифа» и «самое безопасное место в самолёте» — сильные тексты, но уход 45–56%: в первых кадрах нет причины остаться.</li>
      <li><b>Что работает:</b> вопрос-хук на сильном кадре («Qaysi birini tanlarding?» — 1 173 комментария), полезный список («Kerakli ilovalar» — 3,3% сохранений, в 12 раз выше медианы), код «+» на локацию (651 комментарий на 10,5 тыс.).</li>
      <li><b>Офф-ниша.</b> Ролик про Claude и Windsor («HA») — 608 просмотров, уход 79%. Аудитория пришла за путешествиями; такие темы — в личный блог.</li>
      <li><b>3 формата (F1–F3), выбранные 31 октября, ещё не вышли</b> — с 30 октября пауза.</li>
    </ul>
  </div>
  <div class="card">
    <h3>3. Топ-3 ошибки, которые прямо сейчас мешают росту</h3>
    <div class="err"><div class="num">1</div><div>
      <b>Вирусные просмотры не превращаются в подписчиков.</b> 1,49 млн на «Sakinat» дали ~460 подписок за 4 дня (0,3 на 1 000). В обычные дни — те же 11 подписок, что и до хита.
      <div class="fix">На каждый F4-ролик (локация + вопрос) — код «+» и ChatPlace с проверкой подписки: локацию получает только подписчик. Шапка с обещанием (вариант выше). Закрепить 3: «Sakinat», «Kerakli ilovalar», «Qaysi birini tanlarding?».</div>
    </div></div>
    <div class="err" style="margin-top:14px"><div class="num">2</div><div>
      <b>Половина роликов теряет зрителя в первые 3 секунды.</b>
      <div class="fix">Первый кадр — самый сильный кадр ролика + вопрос или сумма до 6 слов. Никаких вступлений и стен текста. Проверка: без звука за 1 секунду понятно, о чём видео.</div>
    </div></div>
    <div class="err" style="margin-top:14px"><div class="num">3</div><div>
      <b>Нет ритма, и темы разъезжаются.</b> Пауза после хита и ролики вне ниши размывают, «о чём аккаунт».
      <div class="fix">4 Reels в неделю: пн F1 «Бюджет», ср F2 «Топ-5», пт F3 «Секрет», вс F4 «Локация + вопрос». Всё, что не про путешествия, — в @sadikovtimur_.</div>
    </div></div>
  </div>
''')

# ---------- TA ----------
section("s-ta", '''
  <h2>Целевая аудитория: 4 сегмента</h2>
  <p class="lead">Промт 2. Блог — путешествия по Узбекистану и миру с точными цифрами: куда ехать и сколько это стоит. Деньги — реклама турагентств, банков, eSIM, авиа. Сегменты — по данным аудитории из Windsor.</p>
  <div id="segs"></div>
''')

# ---------- plan ----------
section("s-plan", '''
  <h2>Контент-план: 5 ноября – 4 декабря</h2>
  <p class="lead">Промт 3. Цель месяца: <b>+1 000 подписчиков</b> (сейчас +778 с вирусным хитом) и <b>1 подписка на 1 000 просмотров</b> (сейчас 0,43). Ритм — 4 Reels в неделю (твой лимит), Stories каждый день.</p>
  <div class="card">
    <div class="chips" id="fType">
      <button class="chip" aria-pressed="true" data-v="all">Все</button>
      <button class="chip" aria-pressed="false" data-v="E">Развлекательный</button>
      <button class="chip" aria-pressed="false" data-v="X">Экспертный</button>
      <button class="chip" aria-pressed="false" data-v="S">Продающий</button>
      <button class="chip" aria-pressed="false" data-v="Stories">Stories-день</button>
    </div>
    <div id="plan"></div>
  </div>
  <div class="card"><h3>Stories каждый день — шаблон</h3><ul class="clean">
    <li><b>Утро:</b> опрос «куда бы поехали: 1 или 2» — даёт ответы и охват.</li>
    <li><b>День:</b> закулисье: съёмка, расчёт бюджета, поиск билетов на экране.</li>
    <li><b>Вечер:</b> репост нового Reels + вопрос.</li>
    <li>Раз в неделю — «Savol bering» → ответы превращаются в F3 «Секрет».</li></ul></div>
  <div class="card"><h3>Правила хука</h3><ul class="clean">
    <li>Первый кадр — самый сильный кадр ролика, а не «salom».</li>
    <li>Текст на экране — до 6 слов: сумма, вопрос или «sir».</li>
    <li>В хуке есть цифра: «3 million», «5 ta», «30 km».</li>
    <li>Вопрос-выбор («Qaysi birini tanlarding?») — твой рекорд по комментариям.</li>
    <li>Проверка без звука: за 1 секунду понятно, о чём видео?</li></ul></div>
  <div class="card"><h3>Банк CTA</h3><ul class="clean">
    <li>«Lokatsiya kerak bo'lsa — kommentga + yozing» (F4).</li>
    <li>«Saqlab qo'ying, sayohatdan oldin kerak bo'ladi» (F2).</li>
    <li>«Shuncha pulga?! Siz qaysi variantni tanlardingiz?» (F1).</li>
    <li>«Kim bilan borardingiz? Belgilang» (F4, репосты).</li>
    <li>❌ «Obuna bo'ling» как хук — «Obuna boling» дал 1,9 тыс. (данные июля).</li></ul></div>
''')

# ---------- picked / script (empty) ----------
section("s-picked", '''
  <h2>Выбранные темы</h2>
  <p class="lead">Сюда попадают только темы, которые ты выбрал и отправил в бот. По каждой — статус и переход к сценарию.</p>
  <!-- PICKED:START -->
  <div class="card" id="picked-empty"><b>Пока ничего не выбрано.</b><div class="td" style="color:var(--ink2);font-size:14px;margin-top:4px">Вкладка «Темы» → «☆ Выбрать» → «Отправить ✈», или напиши номер темы в бот. Сценарий появится в течение часа.</div></div>
  <!-- PICKED:END -->
''')
sc = s[s.index('<section id="s-script"'):]
sc_style = re.search(r"<style>#s-script.*?</style>", sc, flags=re.S).group(0)
section("s-script", f'''
  {sc_style}
  <h2>Сценарий от и до</h2>
  <p class="lead">Полный сценарий под формат выбранной темы: текст для съёмки (узбекский, твой голос, ~2,6 слова/с), что на экране, реальные медиа (Pexels / Commons / App Store), описание (UZ + RU/EN), закреп, ChatPlace и чек-лист. Все цифры — со свежими источниками и датой.</p>
  <!-- SCRIPT:START -->
  <div class="card" id="script-empty"><b>Сценария пока нет.</b><div style="color:var(--ink2);font-size:14px;margin-top:4px">Появится здесь в течение часа после выбора темы.</div></div>
  <!-- SCRIPT:END -->
''')

# ---------- references tab (new) ----------
refs = '''
<!-- РЕФЕРЕНСЫ -->
<section id="s-refs" data-title="Референсы">
  <h2>Референсы</h2>
  <p class="lead">Присылай в бот видео-референсы (до 20 МБ) или ссылки. Я разбираю структуру, хук, монтаж и добавляю новый формат с 10 темами во вкладку «Темы». Референсы с аккаунта жены не используются.</p>
  <!-- REFS:START -->
  <div class="card" id="refs-empty"><b>Пока пусто.</b><div style="color:var(--ink2);font-size:14px;margin-top:4px">Базовые форматы F1–F3 — из твоих референсов от 31 октября; F4 — из данных аккаунта.</div></div>
  <!-- REFS:END -->
</section>
'''
s = s.replace("\n<!-- ВЫБРАННЫЕ -->", refs + "\n<!-- ВЫБРАННЫЕ -->", 1)

# ---------- tasks ----------
section("s-tasks", '''
  <h2>Задачи на эту неделю</h2>
  <p class="lead">Отмечай выполненное — прогресс сохранится на этом устройстве.</p>
  <div class="card">
    <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:600"><span>Прогресс</span><span id="pct">0 из 0</span></div>
    <div class="progress"><i id="bar"></i></div>
  </div>
  <div class="card" id="tasks"></div>
''')

# ---------- main script data ----------
a = s.index("<script>\nconst tg"); b = s.index("</script>", a)
js = s[a:b]

def rep(start, new):
    global js
    i = js.index(start); j = js.index("];", i) + 2
    js = js[:i] + new + js[j:]

rep("const daily=", "const daily=[13337,5059,8870,6686,6721,5718,3497,3388,5091,6811,5934,2579,1871,3665,249080,729298,139709,171833,73180,68363,49548,22950,32328,38352,34124,30363,28164,24104,22615,20111];")
rep("const follows=", "const follows=[6,3,4,4,3,6,2,1,13,55,41,4,3,5,59,215,136,50,31,16,18,14,14,19,10,14,10,8,6,8];")
js = js.replace("max=80000;", "max=800000;").replace("[0,20000,40000,60000,80000]", "[0,200000,400000,600000,800000]")
js = js.replace("new Date(2026,9,3+i)", "new Date(2026,9,5+i)").replace("['3 окт','10 окт','17 окт','24 окт','31 окт']", "['5 окт','12 окт','19 окт','26 окт','2 ноя']")
js = js.replace('aria-label="Просмотры по дням, 3 октября – 1 ноября"', 'aria-label="Просмотры по дням, 5 октября – 3 ноября"')
rep("const cmp=", """const cmp=[
 {t:'Удержание в первые 3 секунды',a:['Уходят < 35% (3 ролика)',270672],b:['Уходят ≥ 50% (12 роликов)',2222]},
 {t:'Сохранения: полезный список против остальных',a:['«Kerakli ilovalar»',328,'3,3%'],b:['Медиана роликов',28,'0,28%']},
 {t:'Комментарии: код «+» на локацию',a:['Ролик с кодом «+»',651],b:['Медиана роликов',13]},
];""")
js = js.replace("<div class=\"val\">${fmt(r[1])}</div>", "<div class=\"val\">${r[2]||fmt(r[1])}</div>")
rep("const topP=", "const topP=[P('Sakinat 🇺🇿','Deq8OsTsHpz',1490777,7080,7640,33),P('Qaysi birini tanlarding? (1 173 комм.)','DeCkhWLKOhW',270672,376,2448,35),P('🐻','DcvABFTKTXo',220755,1576,4590,57),P('Shu yerga kim bilan borardingiz?','DewtUr-qUoO',166899,640,4969,42),P('Sayohat uchun eng kerakli ilovalar','DdqvOVNMhWh',23419,769,839,49),P(\"Eng qimmat o'rindiq O'zbekistonda\",'Des6IElMklo',15457,43,164,38)];")
rep("const sav=", "const sav=[P('Sakinat 🇺🇿','Deq8OsTsHpz',1490777,7080,7640,33),P('🐻','DcvABFTKTXo',220755,1576,4590,57),P('Sayohat uchun eng kerakli ilovalar — 3,3%','DdqvOVNMhWh',23419,769,839,49),P('Shu yerga kim bilan borardingiz?','DewtUr-qUoO',166899,640,4969,42),P('Qaysi birini tanlarding?','DeCkhWLKOhW',270672,376,2448,35)];")
rep("const flop=", "const flop=[P('Instagram tahlil — kommentga «HA» (Claude)','De1GRMxqQ4G',608,3,1,79),P('Kechasi palatka qoyib…','DdW_zO3KKr5',1168,2,4,57),P('🌄⛰️🇺🇿 Uzbekistan','DcyjczLsXbQ',1390,4,5,83),P(\"Toshkentda bunaqa osmonni ko'rmaysiz\",'Deb-RXLsU7j',1824,2,1,49),P('Bu Shveysariya emas','DewMTrbqknj',1947,2,5,75)];")
js = re.sub(r"bars\('ages',\[.*?\]\);", "bars('ages',[['13–17',71,'3%'],['18–24',554,'23%'],['25–34',979,'40%'],['35–44',517,'21%'],['45–54',193,'8%'],['55+',110,'5%']]);", js, flags=re.S)
js = re.sub(r"bars\('cities',\[.*?\]\);", "bars('cities',[['Янгиер',254,'10,5%'],['Ташкент',100,'4,1%'],['Зарафшан',86,'3,5%'],['Ургенч',83,'3,4%'],['Ромитан',78,'3,2%'],['Навои',71,'2,9%'],['Самарканд',69,'2,8%'],['Москва',27,'1,1%'],['Стамбул',15,'0,6%']]);", js, flags=re.S)
rep("const segs=", """const segs=[
 {tag:'≈40% · мужчины 25–34',n:'Первая поездка за границу (регионы)',
  pain:'Не знает, с чего начать; боится переплатить и быть обманутым; виза, язык, пересадки.',
  want:'Съездить за границу без переплаты и показать семье, что это реально.',
  obj:'«Это дорого», «я не знаю английский», «обманут в турагентстве».',
  topics:['F1 «3 / 6 / 10 млн сум — куда на 3 дня»','F2 «5 стран без визы»','F2 «5 переводчиков» (ты учитель английского)']},
 {tag:'≈23% · 18–24 и друзья',n:'Выходные в горах и приключения',
  pain:'На заграницу денег нет, выходные скучные, не знают локаций и дороги.',
  want:'Приключение с друзьями, кадры «как в Швейцарии», рядом и недорого.',
  obj:'«Не знаю дорогу», «негде ночевать», «опасно».',
  topics:['F4 «Чарвак / Арашан / Урунгач» с кодом на локацию','F2 «5 гор в 2 часах от Ташкента»','F1 «Выходные в горах: сколько»']},
 {tag:'≈21% · 35–44',n:'Семейный отдых',
  pain:'Бюджет на 4 человек, безопасность, комфорт с детьми.',
  want:'Отдых без стресса, где детям хорошо, по понятной цене.',
  obj:'«С детьми сложно», «за границей дорого».',
  topics:['F1 «Семья в горах на 2 дня: сколько»','F1 «Хива и Бухара на поезде»','F3 «3 вещи об аэропорте»']},
 {tag:'Покупатель рекламы',n:'Бренды: турагентства, банки, eSIM, авиа',
  pain:'Нужен реальный охват в регионах и нативная подача.',
  want:'Цифры и кейсы: кто смотрит, сколько, что делает.',
  obj:'«2,4 тыс. подписчиков».',
  topics:['Медиакит: 1,8 млн просмотров/мес, 77% мужчины, 62% — 25–44','F3 «Оплата картой за границей» — нативно для банка','F2 «eSIM» — нативно для eSIM-сервиса']}
];""")
rep("const plan=", r"""const plan=[
['5 ноя','ср','Reels','X','F2 · Топ-5 приложений для дешёвых билетов','Arzon aviachipta topish uchun 5 ta ilova — 1-o\'rin hammani hayron qoldiradi','Kommentga «CHIPTA» — ro\'yxat Direktga'],
['7 ноя','пт','Reels','X','F3 · 3 вещи об аэропорте','Aeroportda turistlar bilmaydigan 3 narsa 🤫','Kommentga «AEROPORT»'],
['9 ноя','вс','Reels','E','F4 · Чарвак','Shu yerga kim bilan borardingiz? 💙','Lokatsiya — kommentga + (ChatPlace + проверка подписки)'],
['10 ноя','пн','Reels','X','F1 · 3 / 6 / 10 млн сум — куда на 3 дня','3 kunga 3, 6 va 10 million so\'m bilan qayerga?','Qaysi biri sizga: 1, 2 yoki 3?'],
['11 ноя','вт','Stories','Stories','Опрос «куда следующий F1?» + закулисье расчёта','Keyingi videoda qaysi davlat?','Опрос'],
['12 ноя','ср','Reels','X','F2 · Топ-5 eSIM','Chet elda rouming emas — 5 ta eSIM ilova','Kommentga «ESIM»'],
['14 ноя','пт','Reels','X','F3 · Когда реально дешевеют билеты','Aviachipta qachon arzonlashadi? Sir — kun emas','Kommentga «NARX»'],
['16 ноя','вс','Reels','E','F4 · Озёра Арашан','Bu Shveysariya emas — bu O\'zbekiston','Kommentga «ARASHAN»'],
['17 ноя','пн','Reels','X','F1 · Стамбул на 3 дня','Istanbulga 3 kun — shuncha pulga?!','Kommentga «ISTANBUL»'],
['19 ноя','ср','Reels','X','F2 · 5 гор в 2 часах от Ташкента','Toshkentdan 2 soatda 5 ta tog\' joyi','Kommentga «TOG»'],
['21 ноя','пт','Reels','S','F3 · Оплата картой за границей (место под банк)','Chet elda karta bilan to\'laganda pulingiz qayerga ketadi?','Kommentga «KARTA»'],
['23 ноя','вс','Reels','E','F4 · Чимган зимой','Qishda shu yerga kim bilan chiqardingiz? ❄️','Kommentga «CHIMGAN»'],
['24 ноя','пн','Reels','X','F1 · Дубай: эконом / средний / люкс','Dubayga 3 kun: 5 vs 10 vs 20 million','Qaysi variant siznikiga o\'xshaydi?'],
['26 ноя','ср','Reels','X','F2 · 5 стран без визы','O\'zbek pasporti bilan vizasiz 5 davlat','Kommentga «VIZA»'],
['27 ноя','чт','Stories','S','Медиакит в Highlights «Hamkorlik»: охват, аудитория, кейсы','Brendlar uchun','Hamkorlik: Direct'],
['28 ноя','пт','Reels','X','F3 · Пересадка: 3 секрета','Tranzit reysda turistlar qiladigan 3 xato','Kommentga «TRANZIT»'],
['30 ноя','вс','Reels','E','F4 · Хива ночью','Xivani kechasi ko\'rganmisiz?','Kommentga «XIVA»'],
['1 дек','пн','Reels','X','F1 · Куда на одну зарплату','Bitta oylik maosh bilan qayerga borish mumkin?','Shuncha pulga?!'],
['3 дек','ср','Reels','X','F2 · 5 мест в Узбекистане зимой','Qishda borish kerak bo\'lgan 5 joy','Kommentga «QISH»'],
];""")
rep("const tasks=", """const tasks=[
 ['Сегодня','Нажать /start в боте @timurblog222024_bot','Без этого бот не может писать тебе и принимать задачи.'],
 ['До 5 ноя','Обновить имя и шапку','Вариант — во вкладке «Аудит профиля»: обещание «aniq raqamlar», «Shuncha pulga?!», Telegram вместо YouTube.'],
 ['До 5 ноя','Закрепить 3 ролика','«Sakinat», «Kerakli ilovalar», «Qaysi birini tanlarding?».'],
 ['До 6 ноя','ChatPlace на код «+» для локаций','С проверкой подписки: локацию получает только подписчик.'],
 ['5 ноя','Выложить F2 «Топ-5 приложений для билетов»','Первый ролик плана, через tripvibe-engine.'],
 ['До 10 ноя','4 Reels за неделю по плану','F2 → F3 → F4 → F1.'],
 ['Всегда','Проверять хук без звука','Первый кадр — сильнейший, текст ≤6 слов.'],
 ['Всегда','Вне travel — не в @tripvibeuz','Claude, SMM, Windsor — в @sadikovtimur_.'],
 ['Когда будут','Скинуть референсы в бот','Разберу и добавлю формат с 10 темами.'],
];""")
js = js.replace("const KEY='mukhlisa_tasks_v1'", "const KEY='tripvibe_tasks_v1'")
s = s[:a] + js + s[b:]

# ---------- topics tab ----------
spec = importlib.util.spec_from_file_location("stories", "/home/claude/scripts/stories.py")
st = importlib.util.module_from_spec(spec); spec.loader.exec_module(st)
st.T = TOPICS; st.FORMATS = FORMATS
st.METHOD = [("Факты", "Каждая цифра, цена и правило — из свежего источника с датой; без подтверждения цифра не используется."),
             ("Медиа", "Только реальные: свои кадры, Pexels, Wikimedia Commons, скриншоты App Store. Никаких нарисованных интерфейсов и чужих видео."),
             ("Голос", "Узбекский (латиница), разговорный, твой голос; «Shuncha pulga?!» где уместно; ~2,6 слова/с."),
             ("Сборка", "F1–F3 — через tripvibe-engine: new → stills → render → дубль с твоей съёмкой → финал −14 LUFS + .srt.")]
st.RULES = ["Не больше 4 Reels в неделю.", "Субтитры UZ + RU/EN на ключевых моменты — для Москвы, Стамбула, Казахстана.",
            "Не вкладывать в твои уста опыт, которого не было.", "Каждый ролик заканчивается кодом для ChatPlace с проверкой подписки."]
tab = st.html_tab()
tab = (tab.replace("mukhlisa_story_pick_v1", "tripvibe_pick_v1").replace("mukhlisa22092024_bot", BOT)
          .replace("<h3>3 формата</h3>", "<h3>4 формата</h3>").replace("Темы: 3 формата + воронка", "Темы: 4 формата + воронка")
          .replace("Полный сценарий под выбранный формат появится во вкладке «Сценарий» в течение часа. 50 тем в трёх форматах: сторителлинг, тренд-туториал и экспертный кейс. Для историй и кейсов выбирай то, что реально было.",
                   "Полный сценарий под формат появится во вкладке «Сценарий» в течение часа. 40 тем в 4 форматах: F1–F3 — твои фиксированные форматы, F4 — «локация + вопрос», подтверждённый данными.")
          .replace("<h3>Схема истории</h3>", "<h3>Производство</h3>")
          .replace("Kanalda barcha topilmalar ssilkalari bor", "Kanalda barcha lokatsiyalar va ro'yxatlar bor")
          .replace("Va'da qilganimni tayyorlab qo'ydim", "Va'da qilgan ma'lumotni tayyorlab qo'ydim"))
m = re.search(r"\n<!-- ИСТОРИИ -->.*?</section>\n", s, flags=re.S)
s = s[:m.start()] + tab + s[m.end():]

# leftovers
s = s.replace("@mukhlisasadikova_", "@tripvibeuz")
open(OUT, "w", encoding="utf-8").write(s)
left = [w for w in ["Мухлис", "Muxlisa", "mukhlisa", "ollee", "Selfut", "бьюти"] if w in s]
print("ok", len(s), "leftovers:", left)
