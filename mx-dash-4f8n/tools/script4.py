"""Full production pack for topic 4 -> Picked + Script sections of the dashboard."""
import html, re, sys

E = html.escape
N = 4
TITLE = "Стала мамой — потеряла себя"
HOOK = "Ona bo'ldim va [3] oy davomida ko'zguga bir marta ham qaramadim."
CODE, ALT = "ONA", "ОНА"
BONUS = "3 daqiqalik makiyaj: 5 ta mahsulot va qadamlar"
DATE_PICK, DATE_FULL = "02.11", "02.11.2026"

STEPS = [
 ("0–4 с", "1. Хук",
  "Ona bo'ldim — va [3] oy davomida ko'zguga bir marta ham qaramadim.",
  "[3] oy ko'zgusiz",
  "Крупный план, смотрит в камеру без улыбки. В углу — фото, где она уставшая, с малышом на руках [реальное фото]."),
 ("4–20 с", "2. Нарастание",
  "Hamma vaqtim bolamga ketardi. Tunda uyg'onish, emizish, yig'i… O'zimga 10 daqiqa ham qolmasdi. "
  "Har kuni «bugun o'zimga vaqt ajrataman» derdim — [va har safar nima xalal bergan: bola uyg'onib ketardi / uy ishlari]. "
  "Kunlar shunday o'tib ketaverdi.",
  "O'zimga 10 daqiqa ham yo'q",
  "Вставки: ночное кормление или детская кроватка в полутьме, часы [реальное время ночью], растрёпанный пучок в зеркале."),
 ("20–38 с", "3. Второй конфликт",
  "Keyin bir kuni telefonimda [tug'ruqdan oldingi] rasmimni ko'rib qoldim. Va yig'lab yubordim. "
  "«Qayerga ketdi u qiz?» [Agar bo'lgan bo'lsa: kimdir nima degani — masalan, «charchagan ko'rinasan»]. "
  "Eng og'iri — o'zimni o'zim tanimay qoldim.",
  "Qayerga ketdi u qiz?",
  "В углу — её старое фото до родов [реальное], потом резкая смена на сегодняшний кадр без макияжа. Пауза 1 секунда без музыки перед кульминацией."),
 ("38–55 с", "4. Кульминация",
  "O'shanda tushundim: o'zimga vaqt ajratish — xudbinlik emas. Bolamga charchagan emas, baxtli ona kerak. "
  "Va qaror qildim: kuniga atigi 3 daqiqa — bola uxlaguncha — faqat o'zim uchun.",
  "Baxtli ona = baxtli bola",
  "Говорит прямо в камеру, теплее и тише. В углу — спящий малыш (лица можно не показывать) и таймер «3:00» на телефоне."),
 ("55–75 с", "5. Развязка + CTA",
  "Mana [N] oydirki, har kuni 3 daqiqada mana shunday bo'laman. Bor-yo'g'i [5] ta mahsulot. "
  "Ro'yxat va qadamlarni xohlasangiz — kommentga «ONA» deb yozing, Direktga yuboraman 💌",
  "Kommentga «ONA» yozing",
  "Таймлапс макияжа с таймером 3:00 в углу → финальный кадр «после», улыбка. Кодовое слово крупно на последних 3 секундах."),
]

MUSIC = [
 "0–20 с: тихая лиричная подложка (пианино / lo-fi), голос впереди, музыка на −20 дБ.",
 "20–38 с: музыка чуть темнее; перед кульминацией — 1 секунда тишины.",
 "38–55 с: музыка нарастает и выходит на пик на фразе «Baxtli ona kerak».",
 "55–75 с: светлый, тёплый финал; на таймлапсе темп быстрее.",
 "Субтитры на каждое слово; плашка шага сверху (как в видео-примере); цвет акцента — розовый аккаунта.",
 "Вставки из прошлого — маленьким окном в верхнем углу, 1–3 секунды каждая.",
]

CAPTION = ("Ona bo'ldim va [3] oy ko'zguga qaramadim 🥹\n\n"
 "Hamma vaqtim bolamga ketardi, o'zimga 10 daqiqa ham qolmasdi.\n"
 "Bir kuni eski rasmimni ko'rib yig'lab yubordim.\n"
 "Endi har kuni bola uxlaguncha 3 daqiqa — faqat o'zim uchun 🤍\n\n"
 "Onalar, sizda ham shunaqami?\n\n"
 "👇 Kommentga «ONA» yozing — 3 daqiqalik makiyaj qadamlarini Direktga yuboraman")

PINNED = "«ONA» deb yozing — 5 ta mahsulot va qadamlarni Direktga yuboraman 💌\nOnalar, o'zingizga kuniga qancha vaqt ajratasiz? 👇"

FUNNEL = [
 ("Триггер", "ONA, Ona, ona, ОНА, Она, она. В ChatPlace включить <b>точное совпадение</b> (комментарий целиком = слово): «ona» — частое слово, иначе бот ответит на «men ham ona bo'ldim»."),
 ("Ответ ×3", "1) «Direktni tekshiring 💌» 2) «Yubordim, onajon 🤍» 3) «Direktga qarang ✨»"),
 ("Карточка", "«Salom! 🤍 Va'da qilgan 3 daqiqalik makiyaj ro'yxatini tayyorlab qo'ydim. Olish uchun tugmani bosing 👇» + кнопка «Olish 🎁»"),
 ("Подписка?", "Нет → «Bu ro'yxatni faqat obunachilarimga yuboraman 🙈 @mukhlisasadikova_ ga obuna bo'ling va pastdagi tugmani bosing» + кнопка «Obuna bo'ldim ✅»"),
 ("Бонус", "Да → «Mana ro'yxat 💌 👉 [ссылка на пост в Telegram-канале]\nKanalda barcha topilmalarimning ssilkalari bor 🤍»"),
 ("В течение 24 ч", "«Yana qaysi mavzuda video qilay? Yozib qoldiring 🤍» — ответы = идеи для следующих Reels."),
]

BONUS_POST = ("⏱ 3 daqiqalik makiyaj — bola uxlaguncha\n"
 "Yosh onalar uchun, bor-yo'g'i 5 ta mahsulot 🤍\n\n"
 "1. [Krem / SPF] — [nomi], [narxi] — teri namlanadi, asos tayyor\n"
 "2. [Konsiler] — [nomi], [narxi] — ko'z ostidagi charchoqni yopadi\n"
 "3. [Qosh qalami yoki geli] — [nomi], [narxi]\n"
 "4. [Tush] — [nomi], [narxi]\n"
 "5. [Rumyan / lab uchun 2-in-1] — [nomi], [narxi]\n\n"
 "Qadamlar:\n"
 "0:00–0:30 — krem\n"
 "0:30–1:15 — konsiler faqat ko'z osti va qizargan joylarga, barmoq bilan\n"
 "1:15–1:45 — qosh\n"
 "1:45–2:30 — tush, bitta qatlam\n"
 "2:30–3:00 — rumyan yonoqqa va labga\n\n"
 "💡 Hammasini bitta kosmetichkada, ko'zgu yonida saqlang — vaqt tejaladi.\n"
 "Ssilkalar: [havolalar]")

CHECK = [
 "Заполнить все [скобки] реальными фактами: сколько месяцев, что мешало, старое фото, 5 своих средств.",
 "Пост-бонус опубликован в Telegram-канале, ссылка вставлена в ChatPlace.",
 "В ChatPlace — точное совпадение для «ONA», сценарий проверен комментарием с чужого аккаунта.",
 "Хук проверен без звука: за 1 секунду понятно, о чём видео.",
 "После публикации — свой комментарий с кодом, закрепить.",
 "Через 48 ч записать: комментарии с кодом, новые подписки, переходы в Telegram.",
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
    <p class="muted" style="margin:8px 0 0">Длительность ~75 сек · говорящая голова + вставки из прошлого в верхнем углу · субтитры + плашка шага. Рубрика «3 daqiqa, bola uxlaguncha» — это первый выпуск.</p></div>
  <div class="card"><h3>🎬 Текст для съёмки (по 5 шагам)</h3>{steps_html}
    <p class="muted" style="margin:8px 0 0">Говорить своими словами можно, смысл и порядок шагов сохранить.</p></div>
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
