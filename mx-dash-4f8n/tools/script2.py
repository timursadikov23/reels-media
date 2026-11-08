"""Full production pack for topic 4 -> Picked + Script sections of the dashboard."""
import html, re, sys

E = html.escape
N = 2
TITLE = "Первая реклама провалилась"
HOOK = "Birinchi reklamam 14 ming ko'rish oldi. Reklamasiz oddiy videom esa ertasi kuni 461 ming oldi."

CODE, ALT = "BLOG", "БЛОГ"
BONUS = "Brendga reklama taklif qilish: tayyor xabar shabloni"
DATE_PICK, DATE_FULL = "08.11", "08.11.2026"

STEPS = [
 ("0–7 с", "1. Хук",
  "Birinchi reklamam 14 ming ko'rish oldi. Reklamasiz oddiy videom esa ertasi kuni 461 ming oldi.",
  "Birinchi reklama — 14 ming",
  "Говоришь в камеру. Слева всплывает карточка статистики рекламы @ollee.uz 26.04.2026 (13 999), затем — ролика 27.04.2026 (461 043). Крупно: «14 MING KO'RISH», «461 MING»."),
 ("7–16 с", "2. Как все",
  "Ollee.uz birinchi marta yozganda juda xursand bo'ldim. Hamma blogerlar qanday qilsa, men ham shunday qildim: mahsulotni ko'rsatdim, brendni maqtadim, «ssilka storisda».",
  "Hamma qilgandek",
  "Говоришь в камеру, можно жестами показать «как все»."),
 ("16–20 с", "3. Ошибка",
  "Natija — 14 ming. Deyarli yarmi birinchi 3 soniyada tashlab ketdi.",
  "46% tashlab ketdi",
  "Снова карточка первой рекламы: 46,4% зрителей ушли в первые 3 секунды. Крупно: «46% TASHLAB KETDI»."),
 ("20–27 с", "4. Вывод",
  "Keyin tushundim: odamlar reklamani emas, natijani ko'rishni xohlaydi. Avval mening muammom va natijam — brend esa keyin.",
  "Avval natija, keyin brend",
  "Прямо в камеру, теплее и увереннее. Крупно: «NATIJA»."),
 ("27–43 с", "5. Результат + CTA",
  "Avgustda xuddi shu brend uchun shu formatda video qildim — 552 ming ko'rish. Tashlab ketganlar esa 46 emas, 22 foiz. Brendga qanday yozishni bilmoqchimisiz? Kommentga «BLOG» deb yozing — tayyor shablonni Direktga yuboraman.",
  "552 ming · «BLOG»",
  "Карточка ролика @ollee.uz 16.08.2026 (552 372, ушли 22,3%). Крупно: «552 MING KO'RISH», «46% EMAS / 22%», в конце «BLOG»."),
]

MUSIC = [
 "0–16 с: лёгкая фоновая музыка, голос впереди (−20 дБ).",
 "16–20 с: музыка тише на «46% tashlab ketdi»; 0,5 с паузы перед «Keyin tushundim».",
 "20–27 с: нарастание, пик на «natija».",
 "27–43 с: уверенный, светлый финал; на «552 MING» — акцент (уже есть в зелёном шаблоне).",
 "Плашки глав сверху справа, карточки статистики слева, крупные цифры внизу — всё в шаблоне.",
 "Субтитры — добавь свои в Edits/CapCut, в шаблоне их нет.",
]

CAPTION = ("Birinchi reklamam 14 ming ko'rish oldi — oddiy videom esa 461 ming 😶\n\n"
 "Hamma qilgandek qildim: mahsulot, maqtov, «ssilka storisda».\n"
 "Natija: odamlarning deyarli yarmi 3 soniyada tashlab ketdi.\n"
 "Keyin tushundim: odamlar reklamani emas, natijani ko'rishni xohlaydi.\n"
 "Shu brend uchun shu formatdagi video — 552 ming ko'rish 🤍\n\n"
 "Birinchi reklamangiz qanday bo'lgan?\n\n"
 "👇 Kommentga «BLOG» yozing — brendga yoziladigan tayyor xabar shablonini Direktga yuboraman")

PINNED = "«BLOG» deb yozing — brendga yoziladigan tayyor xabar shablonini Direktga yuboraman 💌\nBirinchi reklamangiz qanday o'tgan? 👇"

FUNNEL = [
 ("Триггер", "BLOG, Blog, blog, БЛОГ, Блог, блог. В ChatPlace — <b>точное совпадение</b> (комментарий целиком = слово): «blog» встречается в обычных комментариях."),
 ("Ответ ×3", "1) «Direktni tekshiring 💌» 2) «Yubordim ✨» 3) «Shablon Direktda 🤍»"),
 ("Карточка", "«Salom! 🤍 Va'da qilgan shablonni tayyorlab qo'ydim. Olish uchun tugmani bosing 👇» + кнопка «Olish 🎁»"),
 ("Подписка?", "Нет → «Shablonni faqat obunachilarimga yuboraman 🙈 @mukhlisasadikova_ ga obuna bo'ling va pastdagi tugmani bosing» + кнопка «Obuna bo'ldim ✅»"),
 ("Бонус", "Да → «Mana shablon 💌 👉 [ссылка на пост в Telegram-канале]\nKanalda barcha topilmalarimning ssilkalari bor 🤍»"),
 ("В течение 24 ч", "«Siz qaysi brend bilan ishlashni xohlaysiz? Yozib qoldiring 🤍» — ответы = идеи для следующих роликов."),
]

BONUS_POST = ("💌 Brendga reklama taklif qilish — tayyor xabar\n\n"
 "Assalomu alaykum! Men — [ism], @[akkaunt] blogeri. [Mavzu: beauty / ona hayoti].\n\n"
 "📊 Oxirgi 30 kun: [ko'rishlar soni] ko'rish, [obunachilar] obunachi, auditoriya: [asosiy yosh va shaharlar].\n"
 "🎬 Eng yaxshi ishim: [video havolasi] — [ko'rishlar] ko'rish.\n\n"
 "Sizning [mahsulot] bilan [format: natija o'zimda / sharh] formatida video qilishni taklif qilaman.\n"
 "Natijani ko'rsatib, sizni ham [nima beradi: sotuv / obunachi] bilan qo'llab-quvvatlayman.\n\n"
 "Batafsil narx va shartlarni yuboraymi? 🤍\n\n"
 "💡 3 qoida: 1) har bir brendga alohida yozing; 2) raqamlarni albatta qo'shing; 3) bitta eng yaxshi videoni ko'rsating.")

CHECK = [
 "Цифры из Instagram-статистики (Windsor, 08.11.2026): 26.04 @ollee.uz — 13 999 просм., ушли за 3 с 46,4%; 27.04 — 461 043; 16.08 @ollee.uz — 552 372, ушли 22,3%.",
 "Подтвердить: ollee.uz написал первым; ролик 16.08 был для ollee.",
 "Видео: снять дубль по тексту, наложить зелёный шаблон mx_birinchi_reklama_GREEN.mp4 (хромакей) или прислать дубль — смонтирую под него.",
 "Пост-бонус опубликован в Telegram-канале, ссылка вставлена в ChatPlace.",
 "ChatPlace: точное совпадение для «BLOG», проверка комментарием с чужого аккаунта.",
 "После публикации — свой комментарий с кодом, закрепить. Через 48 ч: комментарии с кодом, подписки, переходы в Telegram.",
]

br = lambda s: E(s).replace("\n", "<br>")

picked = f'''<div class="card seg" id="picked-{N}">
  <div style="display:flex;justify-content:space-between;gap:8px;align-items:flex-start">
    <span class="tag">Тема {N} · выбрана {DATE_PICK}</span>
    <span class="pill up">✅ Сценарий готов</span>
  </div>
  <h3>{E(TITLE)}</h3>
  <div class="hook2">{E(HOOK)}</div>
  <div class="funnel"><div class="frow"><span>🔑 Код</span><span><b>{CODE}</b> <span class="muted">/ {ALT}</span></span></div>
  <div class="frow"><span>🎁 Бонус</span>{E(BONUS)}</div></div>
  <button class="pick" style="margin-top:10px" onclick="openScript('script-{N}')">Открыть сценарий →</button>
</div>'''

steps_html = "".join(
 f'<div class="day sstep"><div class="dt">{E(t)}<span>{E(lbl)}</span></div><div>'
 f'<div class="topic">«{E(say)}»</div><div class="scr">{E(scr)}</div><div class="shot">{E(shot)}</div></div></div>'
 for t, lbl, say, scr, shot in STEPS)

article = f'''<article id="script-{N}">
  <div class="card seg"><span class="tag">Тема {N} · подготовлено {DATE_FULL}</span><h3>{E(TITLE)}</h3>
    <div class="hook2">{E(HOOK)}</div>
    <p class="muted" style="margin:8px 0 0">Длительность ~75 сек · говорящая голова + вставки из прошлого в верхнем углу · субтитры + плашка шага. Работает и на подписчиц-блогеров, и на бренды: показывает, что она умеет делать рекламу, которая смотрится.</p></div>
  <div class="card"><h3>🎬 Текст для съёмки (по 5 шагам)</h3>{steps_html}
    <p class="muted" style="margin:8px 0 0">Говорить своими словами можно, смысл и порядок шагов сохранить. [Скобки] — заполнить реальными фактами.</p></div>
  <div class="card"><h3>🎵 Музыка и монтаж</h3><ul class="clean">{"".join(f"<li>{E(m)}</li>" for m in MUSIC)}</ul></div>
  <div class="card"><h3>✍️ Описание к Reels</h3><div class="bio">{br(CAPTION)}</div></div>
  <div class="card"><h3>📌 Закреплённый комментарий</h3><div class="bio">{br(PINNED)}</div></div>
  <div class="card"><h3>🤖 Воронка ChatPlace</h3><div class="funnel">{"".join(f'<div class="frow"><span>{E(a)}</span><span>{b if "<b>" in b else br(b)}</span></div>' for a, b in FUNNEL)}</div></div>
  <div class="card"><h3>🎁 Пост-бонус для Telegram-канала</h3><div class="bio">{br(BONUS_POST)}</div></div>
  <div class="card"><h3>✅ Чек-лист перед публикацией</h3><ul class="clean">{"".join(f"<li>{E(c)}</li>" for c in CHECK)}</ul></div>
</article>'''


def insert(s, start, end, block, empty_id, item_id):
    a = s.index(start) + len(start); b = s.index(end)
    inner = s[a:b]
    inner = re.sub(r'\s*<div class="card" id="%s">.*?</div></div>' % empty_id, "", inner, flags=re.S)
    inner = re.sub(r'\s*<(div|article)[^>]*id="%s".*?</\1>' % item_id, "", inner, flags=re.S) if f'id="{item_id}"' in inner else inner
    return s[:a] + "\n" + block + inner.rstrip() + "\n  " + s[b:]


p = sys.argv[1]
s = open(p, encoding="utf-8").read()
s = insert(s, "<!-- PICKED:START -->", "<!-- PICKED:END -->", picked, "picked-empty", f"picked-{N}")
s = insert(s, "<!-- SCRIPT:START -->", "<!-- SCRIPT:END -->", article, "script-empty", f"script-{N}")
open(p, "w", encoding="utf-8").write(s)
print("ok", 'id="picked-empty"' in s, 'id="script-empty"' in s)
