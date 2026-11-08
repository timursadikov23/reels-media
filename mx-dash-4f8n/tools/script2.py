"""Full production pack for topic 4 -> Picked + Script sections of the dashboard."""
import html, re, sys

E = html.escape
N = 2
TITLE = "Первая реклама провалилась"
HOOK = "Birinchi reklamam [2 ming] ko'rish oldi. Brend menga boshqa yozmadi."
CODE, ALT = "BLOG", "БЛОГ"
BONUS = "Brendga reklama taklif qilish: tayyor xabar shabloni"
DATE_PICK, DATE_FULL = "08.11", "08.11.2026"

STEPS = [
 ("0–4 с", "1. Хук",
  "Birinchi reklamam [2 ming] ko'rish oldi. Va brend menga boshqa hech qachon yozmadi.",
  "Birinchi reklama — [2 ming]",
  "Крупный план, серьёзное лицо. В углу — скриншот статистики того самого ролика [реальный]."),
 ("4–20 с", "2. Нарастание",
  "Reklama — orzuim edi. Birinchi brend yozganda [qanday xursand bo'lganingiz]. Hamma blogerlar qanday qilsa, men ham shunday suratga oldim: qadoq, brend haqida gap, «albatta sotib oling».",
  "Hamma qilgandek qildim",
  "Вставки: кусок той первой рекламы (распаковка, упаковка крупно) [реальный ролик], переписка с брендом без имени бренда."),
 ("20–38 с", "3. Второй конфликт",
  "Video chiqdi — [2 ming] ko'rish. Brend jim. Uyaldim. O'zimga «sendan bloger chiqmaydi» dedim va [necha kun / hafta] hech narsa joylamadim.",
  "Brend jim qoldi",
  "Пустой директ на экране телефона, ты смотришь в сторону. Перед кульминацией — 1 секунда тишины."),
 ("38–55 с", "4. Кульминация",
  "Keyin tushundim: odamlar reklamani emas, natijani ko'rishni xohlaydi. Avval mening muammom va natijam — brend esa keyin.",
  "Avval natija, keyin brend",
  "Говоришь прямо в камеру, теплее и увереннее. Музыка выходит на пик на слове «natija»."),
 ("55–75 с", "5. Развязка + CTA",
  "Shu formatda @ollee.uz uchun video qildim — 551 ming ko'rish. Endi brendlar o'zi yozadi. Brendga qanday yozishni bilmoqchimisiz? Kommentga «BLOG» deb yozing — tayyor xabar shablonini Direktga yuboraman 💌",
  "551 000 ko'rish · «BLOG»",
  "Вставка: ролик @ollee.uz и скриншот его статистики (551 тыс. — реальная цифра). Кодовое слово крупно на последних 3 секундах."),
]

MUSIC = [
 "0–20 с: лёгкая фоновая музыка, голос впереди (−20 дБ).",
 "20–38 с: музыка темнее и тише; перед кульминацией — 1 секунда полной тишины.",
 "38–55 с: нарастание, пик на «Avval natija».",
 "55–75 с: уверенный, светлый финал; на цифре «551 000» — звук-акцент.",
 "Субтитры по одному слову; плашка шага сверху; «551 000» — крупной цифрой.",
 "Вставки из прошлого — маленьким окном в верхнем углу, 1–3 с каждая.",
]

CAPTION = ("Birinchi reklamam [2 ming] ko'rish oldi — brend boshqa yozmadi 😶\n\n"
 "Hamma qilgandek qildim: qadoq, maqtov, «sotib oling».\n"
 "Keyin tushundim: odamlar reklamani emas, natijani ko'rishni xohlaydi.\n"
 "Shu formatdagi keyingi video — 551 ming ko'rish 🤍\n\n"
 "Siz ham blog yuritasizmi? Birinchi reklamangiz qanday bo'lgan?\n\n"
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
 "Заполнить [скобки]: сколько просмотров было у первой рекламы, как радовалась, сколько дней не выкладывала.",
 "Найти реальные вставки: первая реклама, её статистика, ролик @ollee.uz и его статистика (551 тыс.).",
 "Имя бренда первой рекламы не называть.",
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
