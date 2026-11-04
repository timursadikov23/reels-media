"""10 storytelling topics (5-step method) -> Telegram messages + Mini App tab."""
import json, re, subprocess, sys, time

METHOD = [
    ("1. Хук", "В первой фразе — конкретная проблема и конфликт, с цифрами и фактами. В видео-примере: «Мне 32, нет мужа и детей»."),
    ("2. Нарастание", "Чего героиня хочет и что мешает. Что пробовала и почему не получалось."),
    ("3. Второй конфликт", "Примерно в середине ролика становится ещё хуже. Зритель задаётся новым вопросом: что она будет делать дальше?"),
    ("4. Кульминация", "Главный внутренний перелом: решение, осознание. Музыка доходит до пика."),
    ("5. Развязка", "Ответ на главный вопрос из хука и результат. Сюда же — мягкий мостик к продукту или CTA."),
]
RULES = [
    "Длина 60–100 секунд, говорящая голова плюс маленькие вставки из прошлого (фото и видео) в верхнем углу.",
    "Субтитры каждого слова и крупная плашка шага сверху (жёлтая в видео-примере).",
    "Только реальные истории. Если чего-то не было — тему пропускаем, не выдумываем. Цифры в хуках — пример, ставим свои настоящие.",
    "CTA в стиле видео: «Kommentga SO'Z yozing — ssilkani yuboraman» — даёт комментарии и ведёт в Telegram.",
    "Почему это нужно аккаунту: скетчи дают просмотры, но не подписки (0,28 на 1 000). История делает автора запоминающимся — именно этого не хватает для подписок.",
]

T = [
 dict(t="Волосы после родов", type="Продающий (нативно)",
  hook="Tug'ruqdan keyin sochim tutam-tutam to'kildi. 5 oyda ko'zguga qarolmay qoldim.",
  s=["Хотела снова нравиться себе: маски, витамины, советы мамы и подруг.",
     "Стало ещё хуже: дорогое средство не помогло, кто-то сказал «soching siyraklashibdi».",
     "Перестала хвататься за всё подряд: выбрала одну систему и дала ей время.",
     "Результат через N недель на камеру + что именно помогло (бренд нативно)."],
  cta="Kommentga «SOCH» yozing — ro'yxatni yuboraman"),
 dict(t="Первая реклама провалилась", type="Экспертный",
  hook="Birinchi reklamam 2 ming ko'rish oldi. Brend menga boshqa yozmadi.",
  s=["Мечтала о рекламе: первый бренд, радость, сняла «как у всех».",
     "Ролик провалился, было стыдно, решила, что не умею.",
     "Поняла: реклама не должна выглядеть как реклама — сначала моя проблема и результат на мне.",
     "Ролик @ollee.uz в этом формате — 551 тыс. просмотров. Теперь бренды пишут сами."],
  cta="Blogerlik yo'lini davom ettiraymi? «+» yozing"),
 dict(t="Отказала бренду", type="Продающий (доверие)",
  hook="Menga reklama taklif qilishdi — va men rad etdim. Holbuki pul juda kerak edi.",
  s=["Молодая мама, каждая сумма на счету — предложение казалось подарком.",
     "Условия — хвалить то, что сама бы не купила, и много эксклюзива. Давили, торопили.",
     "Решила: доверие подписчиц дороже одного гонорара. Рекламирую только то, что проверила на себе.",
     "С тех пор — «halol sharh». Показать честный обзор и пообещать проверять всё на себе."],
  cta="Siz qaysi brendni sinab ko'rishimni xohlaysiz? Yozing"),
 dict(t="Стала мамой — потеряла себя", type="Развлекательный/личный",
  hook="Ona bo'ldim va 3 oy davomida ko'zguga bir marta ham qaramadim.",
  s=["Всё внимание малышу, на себя — ноль. Хотела хотя бы 10 минут в день.",
     "Увидела своё старое фото и расплакалась: «qayerga ketdi u qiz?»",
     "Поняла: 3 минуты на себя — не эгоизм, малышу нужна счастливая мама.",
     "Ритуал «3 daqiqa, bola uxlaguncha» — стартовая рубрика, первый выпуск."],
  cta="Onalar, sizda ham shunaqami? 🤍 qoldiring"),
 dict(t="Верила, что дорогое = лучше", type="Экспертный",
  hook="Bir kremga 600 ming berdim. Yuzimga toshma toshdi.",
  s=["Была уверена: хорошая кожа стоит дорого, копила на люкс.",
     "Дорогой крем дал реакцию, деньги на ветер, кожа хуже, чем было.",
     "Цена ≠ подходит именно тебе. Начала читать составы.",
     "Средство за 60 тыс. сум, которое реально работает, + сравнение «до/после»."],
  cta="Kommentga «ARZON» yozing — ro'yxatni yuboraman"),
 dict(t="Магистратура + малыш + блог", type="Развлекательный/личный",
  hook="Magistratura, 5 oylik bola va blog. Bir hafta ichida hammasi qulab tushdi.",
  s=["Хотела всё успевать: учёба, блог, мама на 100%.",
     "Одна неделя: экзамен, малыш заболел, дедлайн бренда — сорвала всё.",
     "Перестала тащить всё одна: попросила помощи (муж, семья), составила план.",
     "Моя система недели + быстрый макияж «на экзамен за 5 минут»."],
  cta="Sizning eng og'ir haftangiz qanday bo'lgan? Yozing"),
 dict(t="Купила подделку", type="Экспертный",
  hook="Original deb qalbaki krem oldim. Bilganimda kech edi.",
  s=["Хотела любимое средство подешевле, нашла «оригинал» у продавца.",
     "Реакция кожи, продавец всё отрицает, деньги не вернули.",
     "Научилась проверять: упаковка, код, запах, текстура.",
     "6 признаков подделки на камеру (затем карусель)."],
  cta="Kommentga «ORIGINAL» yozing — chek-listni yuboraman"),
 dict(t="Кожа и прыщи", type="Экспертный/личный",
  hook="Yillar davomida husnbuzar sabab rasmga tushishdan qochardim.",
  s=["Хотела чистую кожу: перепробовала всё, что советовали.",
     "От «народных» средств стало хуже, прятала лицо на фото.",
     "Перестала экспериментировать: простой уход + специалист.",
     "Кожа сейчас без фильтра + мой базовый уход из 3 шагов."],
  cta="Saqlab qo'ying — kerak bo'ladi"),
 dict(t="Надо мной смеялись, когда начала блог", type="Развлекательный/личный",
  hook="Blog ochaman desam ustimdan kulishdi: «sendan bloger chiqmaydi».",
  s=["Хотела делиться находками и найти своё дело.",
     "Первые видео — 300 просмотров, поддержки ноль, хотелось удалить аккаунт.",
     "Решила снимать для тех 300, а не для тех, кто смеётся.",
     "Сегодня ролики набирают 300–550 тыс. и пишут бренды (реальные цифры аккаунта)."],
  cta="Sizga ham shunday deyishganmi? Yozing"),
 dict(t="Макияж, в котором меня не узнали", type="Развлекательный",
  hook="To'yda meni tanimay qolishdi. Va bu maqtov emas edi.",
  s=["Хотела выглядеть идеально на важном событии, доверилась мастеру.",
     "Тяжёлый макияж, «как маска», стеснялась фото весь вечер.",
     "Поняла: красиво — значит «ты, но отдохнувшая», а не другой человек.",
     "Лёгкий праздничный макияж за 10 минут — сравнение «тогда/сейчас»."],
  cta="«TO'Y» yozing — 10 daqiqalik makiyajni alohida chiqaraman"),
]


FUN = [('SOCH', 'СОЧ', "Tug'ruqdan keyin soch parvarishi: men ishlatgan vositalar va tartib"), ('BLOG', 'БЛОГ', 'Brendga reklama taklif qilish: tayyor xabar shabloni'), ('HALOL', 'ҲАЛОЛ', "O'zimda sinab ko'rgan va tavsiya qiladigan 10 ta mahsulot"), ('ONA', 'ОНА', '3 daqiqalik makiyaj: 5 ta mahsulot va qadamlar'), ('ARZON', 'АРЗОН', "60 ming so'mgacha ishlaydigan 10 ta vosita"), ('REJA', 'РЕЖА', 'Yosh onaning haftalik rejasi — shablon'), ('ORIGINAL', 'ОРИГИНАЛ', 'Qalbakini aniqlash: 6 belgili chek-list'), ('TERI', 'ТЕРИ', 'Muammoli teri uchun 3 bosqichli parvarish'), ('START', 'СТАРТ', 'Blogni noldan boshlash: mening birinchi 10 qadamim'), ('TOY', 'ТОЙ', '10 daqiqalik bayram makiyaji: qadamlar va mahsulotlar')]
ACC = ["soch parvarishi ro'yxatini", 'reklama xabari shablonini', "10 ta mahsulot ro'yxatini", '3 daqiqalik makiyaj qadamlarini', "10 ta arzon vosita ro'yxatini", 'haftalik reja shablonini', '6 belgili chek-listni', '3 bosqichli parvarishni', 'birinchi 10 qadamimni', 'bayram makiyaji qadamlarini']
import os as _os, sys as _sys
_sys.path.insert(0,_os.path.dirname(_os.path.abspath(__file__)))
from topics2 import T2, FUN2, ACC2
T += T2; FUN += FUN2; ACC += ACC2
from topics3 import T3, T4, FUN3, FUN4, ACC3, ACC4, FORMATS
for _t in T: _t.setdefault("fmt", "story")
T += T3 + T4; FUN += FUN3 + FUN4; ACC += ACC3 + ACC4
for _x,(_c,_a,_b),_n in zip(T,FUN,ACC):
    _x.update(code=_c,alt=_a,bonus=_b,cta=f"Kommentga «{_c}» yozing — {_n} Direktga yuboraman 💌")

def tg_messages():
    m1 = ("🎬 <b>Изучил приём: сторителлинг Reels в 5 шагов</b>\n"
          "(видео, которое ты прислал, — приём «принёс 50 млн просмотров»)\n\n"
          + "\n".join(f"<b>{a}</b> — {b}" for a, b in METHOD)
          + "\n\n<b>Как применять</b>\n" + "\n".join("• " + r for r in RULES))
    msgs = [m1]
    cur = "📝 <b>10 тем для @mukhlisasadikova_ по этой схеме</b>\n"
    for i, x in enumerate(T, 1):
        block = (f"\n<b>{i}. {x['t']}</b> · <i>{x['type']}</i>\n"
                 f"🪝 <code>{x['hook']}</code>\n"
                 f"↗️ {x['s'][0]}\n⚡️ {x['s'][1]}\n💥 {x['s'][2]}\n✅ {x['s'][3]}\n"
                 f"💬 {x['cta']}\n")
        if len(cur) + len(block) > 3900:
            msgs.append(cur); cur = ""
        cur += block
    msgs.append(cur + "\nВ Mini App появилась вкладка «Истории». Снимаем только то, что было на самом деле.")
    return msgs


def html_tab():
    def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")
    steps = "".join(f"<li><b>{esc(a)}</b> — {esc(b)}</li>" for a, b in METHOD)
    rules = "".join(f"<li>{esc(r)}</li>" for r in RULES)
    labels = ["Нарастание", "Второй конфликт", "Кульминация", "Развязка"]
    cards = ""
    for i, x in enumerate(T, 1):
        beats = "".join(f"<li><b>{l}:</b> {esc(s)}</li>" for l, s in zip(labels, x["s"]))
        cards += (f'<div class="card seg"><span class="tag">{i} · {esc(x["type"])}</span><h3>{esc(x["t"])}</h3>'
                  f'<div class="day" style="display:block;border:0;padding:0"><div class="hook">{esc(x["hook"])}</div></div>'
                  f'<ul class="clean" style="margin-top:8px;font-size:14px">{beats}</ul>'
                  f'<div class="day" style="display:block;border:0;padding:0"><div class="cta">{esc(x["cta"])}</div></div></div>')
    return (f'\n<!-- ИСТОРИИ -->\n<section id="s-stories" data-title="Истории">\n'
            f'  <h2>Сторителлинг в 5 шагов</h2>\n'
            f'  <p class="lead">Приём из видео-разбора: голливудская трёхактная структура в Reels на 60–100 секунд. Ниже — 10 тем для аккаунта.</p>\n'
            f'  <div class="card"><h3>Схема</h3><ul class="clean">{steps}</ul></div>\n'
            f'  <div class="card"><h3>Правила</h3><ul class="clean">{rules}</ul></div>\n'
            f'  {cards}\n</section>\n')


FLOW = [
    ("Триггер", "Комментарий под конкретным Reels содержит кодовое слово. Добавить варианты: латиница, кириллица, строчные буквы."),
    ("Ответ в комментарии", "Публично, 3 чередующихся варианта, чтобы не выглядело как спам: «Direktga yubordim 💌» · «Direktni tekshiring 🤍» · «Yubordim, qarang ✨»."),
    ("Директ 1 — карточка", "«Salom! 🤍 Va'da qilganimni tayyorlab qo'ydim» + кнопка «Olish 🎁». Только карточка: по правилу Instagram первым сообщением по комментарию ссылку не отправить."),
    ("Проверка подписки", "Не подписана → «Bonusni faqat obunachilarimga yuboraman 🙈 Obuna bo'ling va «Obuna bo'ldim» tugmasini bosing» + кнопка «Obuna bo'ldim ✅»."),
    ("Выдача бонуса", "Подписана → ссылка на пост с бонусом в Telegram-канале + «Kanalda barcha topilmalar ssilkalari bor 👇»."),
    ("Дожим в чате", "В течение 24 часов: «Yana qaysi mavzuda video qilay? Yozib qoldiring» — получаем идеи для следующих роликов."),
]
CHECK = [
    "Бонус (пост в Telegram-канале) готов ДО публикации Reels.",
    "В конце видео (развязка): CTA голосом и плашкой на экране, кодовое слово крупно.",
    "В подписи первая строка — хук, последняя — «👇 Kommentga «КОД» yozing».",
    "Сразу после публикации — свой комментарий с кодовым словом, закрепить его.",
    "Проверить сценарий комментарием с ЧУЖОГО аккаунта: комментарии владельца Instagram отфильтровывает.",
    "Через 48 часов записать: комментарии с кодом, новые подписки, переходы в Telegram.",
]

def tg_messages():
    esc = lambda x: x.replace("&", "&amp;").replace("<", "&lt;")
    m1 = ("🎬 <b>Сторителлинг + воронка ChatPlace</b>\n\n<b>Схема ролика</b>\n"
          + "\n".join(f"<b>{a}</b> — {b}" for a, b in METHOD)
          + "\n\n<b>Воронка (одна на все ролики, меняется только кодовое слово и бонус)</b>\n"
          + "\n".join(f"{i}. <b>{a}</b>: {esc(b)}" for i, (a, b) in enumerate(FLOW, 1))
          + "\n\n<b>Чек-лист публикации</b>\n" + "\n".join("☐ " + esc(c) for c in CHECK))
    msgs = [m1]
    cur = "📝 <b>10 тем: история + кодовое слово + бонус</b>\n"
    for i, x in enumerate(T, 1):
        block = (f"\n<b>{i}. {x['t']}</b> · <i>{x['type']}</i>\n"
                 f"🪝 <code>{x['hook']}</code>\n"
                 f"↗️ {x['s'][0]}\n⚡️ {x['s'][1]}\n💥 {x['s'][2]}\n✅ {x['s'][3]}\n"
                 f"🔑 Код: <b>{x['code']}</b> / {x['alt']}\n🎁 Бонус: {x['bonus']}\n"
                 f"💬 CTA: <code>{x['cta']}</code>\n")
        if len(cur) + len(block) > 3900:
            msgs.append(cur); cur = ""
        cur += block
    msgs.append(cur + "\n👉 Отметь темы в Mini App: вкладка «Истории», кнопка «Выбрать». Снимаем только реальные истории.")
    return msgs


def html_tab():
    def esc(x): return x.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")
    steps = "".join(f"<li><b>{esc(a)}</b> — {esc(b)}</li>" for a, b in METHOD)
    rules = "".join(f"<li>{esc(r)}</li>" for r in RULES)
    flow = "".join(f'<div class="fstep"><div class="fn">{i}</div><div><b>{esc(a)}</b><div class="td">{esc(b)}</div></div></div>' for i, (a, b) in enumerate(FLOW, 1))
    chk = "".join(f"<li>{esc(c)}</li>" for c in CHECK)
    labels = ["Нарастание", "Второй конфликт", "Кульминация", "Развязка"]
    cards = ""
    for i, x in enumerate(T):
        F = FORMATS[x["fmt"]]
        beats = "".join(f"<li><b>{l}:</b> {esc(s_)}</li>" for l, s_ in zip(F["labels"], x["s"]))
        tagtxt = f'{i+1} · {F["short"]}' + ('' if x["fmt"] != "story" else f' · {x["type"]}')
        cards += (f'<div class="card seg story" data-fmt="{x["fmt"]}" data-i="{i}" data-code="{esc(x["code"])}" data-title="{esc(x["t"])}" data-bonus="{esc(x["bonus"])}" data-cta="{esc(x["cta"])}" data-hook="{esc(x["hook"])}">'
                  f'<div style="display:flex;justify-content:space-between;gap:8px;align-items:flex-start"><span class="tag">{esc(tagtxt)}</span>'
                  f'<button class="pick" aria-pressed="false">☆ Выбрать</button></div>'
                  f'<h3>{esc(x["t"])}</h3><div class="hook2">{esc(x["hook"])}</div>'
                  f'<ul class="clean" style="margin-top:8px;font-size:14px">{beats}</ul>'
                  f'<div class="funnel"><div class="frow"><span>🔑 Код</span><span><b>{esc(x["code"])}</b> <span class="muted">/ {esc(x["alt"])}</span></span></div>'
                  f'<div class="frow"><span>🎁 Бонус</span>{esc(x["bonus"])}</div>'
                  f'<div class="frow"><span>💬 CTA</span><i>{esc(x["cta"])}</i></div></div></div>')
    cnt = {f: sum(1 for x in T if x["fmt"] == f) for f in FORMATS}
    chips = ('<div class="chips" id="fmtChips"><button class="chip" aria-pressed="true" data-f="all">Все · ' + str(len(T)) + '</button>'
             + "".join(f'<button class="chip" aria-pressed="false" data-f="{f}">{esc(FORMATS[f]["name"])} · {cnt[f]}</button>' for f in FORMATS) + '</div>')
    fmts = ('<div class="card"><h3>3 формата</h3>' + "".join(
        f'<div class="fstep"><div class="fn">{n}</div><div><b>{esc(F["name"])}</b> <span class="muted">· {cnt[f]} тем</span><div class="td" style="font-size:13px;color:var(--ink2)">{esc(F["about"])}</div></div></div>'
        for n, (f, F) in enumerate(FORMATS.items(), 1)) + '<p class="muted" style="margin:8px 0 0">В каждом формате в конце — кодовое слово для ChatPlace: комментарий → проверка подписки → бонус в Telegram.</p></div>')
    css = ('<style>.pick{flex:none;border:1px solid var(--line);background:var(--card);border-radius:999px;padding:6px 11px;font:600 12px/1 inherit;color:var(--ink2);cursor:pointer}'
           '.pick[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff}'
           '.story.picked{box-shadow:0 0 0 2px var(--accent)}'
           '.hook2{font-size:14px;background:#faf9f7;border-radius:8px;padding:7px 9px;margin-top:4px}.hook2::before{content:"Хук: ";color:var(--ink3);font-weight:600}'
           '.funnel{margin-top:10px;background:var(--accent-soft);border-radius:12px;padding:9px 11px;font-size:13px}'
           '.frow{display:grid;grid-template-columns:72px 1fr;gap:6px;margin:3px 0}.frow>span:first-child{color:var(--ink2);font-weight:600}'
           '.fstep{display:flex;gap:10px;padding:8px 0;border-top:1px solid var(--line)}.fstep:first-child{border-top:0}'
           '.fn{width:24px;height:24px;border-radius:50%;background:var(--accent);color:#fff;font-weight:700;font-size:12px;display:grid;place-items:center;flex:none}'
           '.selbar{position:sticky;top:56px;white-space:nowrap;z-index:4;display:flex;gap:8px;align-items:center;justify-content:space-between;background:var(--ink);color:#fff;border-radius:14px;padding:10px 12px;margin-bottom:12px;font-size:13px}'
           '.selbar button{border:0;border-radius:999px;padding:7px 10px;font:600 12px/1 inherit;cursor:pointer;background:#fff;color:var(--ink)}'
           '.selbar .ghost{background:transparent;color:#fff;border:1px solid #ffffff55}</style>')
    js = r"""<script>
(function(){
 var KEY='mukhlisa_story_pick_v1',st={};try{st=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
 var cards=[].slice.call(document.querySelectorAll('.story')),only=false,fmt='all';
 var tgw=window.Telegram&&window.Telegram.WebApp;
 function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
 function draw(){var n=0;cards.forEach(function(c){var on=!!st[c.dataset.i];if(on)n++;c.classList.toggle('picked',on);
   var b=c.querySelector('.pick');b.setAttribute('aria-pressed',on);b.textContent=on?'★ Выбрано':'☆ Выбрать';c.style.display=((only&&!on)||(fmt!=='all'&&c.dataset.fmt!==fmt))?'none':'';});
   document.getElementById('selN').textContent='★ '+n+'/'+cards.length;
   document.getElementById('selOnly').textContent=only?'Все':'Фильтр';}
 cards.forEach(function(c){c.querySelector('.pick').onclick=function(){st[c.dataset.i]=!st[c.dataset.i];save();draw();try{tgw&&tgw.HapticFeedback&&tgw.HapticFeedback.impactOccurred('light')}catch(e){}};});
 document.getElementById('selOnly').onclick=function(){only=!only;draw();};
 [].slice.call(document.querySelectorAll('#fmtChips .chip')).forEach(function(b){b.onclick=function(){fmt=b.dataset.f;[].slice.call(document.querySelectorAll('#fmtChips .chip')).forEach(function(x){x.setAttribute('aria-pressed',x===b)});draw();};});
 document.getElementById('selCopy').onclick=function(){var t=cards.filter(function(c){return st[c.dataset.i]}).map(function(c,k){
   return (k+1)+'. '+c.dataset.title+'\nХук: '+c.dataset.hook+'\nКод: '+c.dataset.code+'\nБонус: '+c.dataset.bonus+'\nCTA: '+c.dataset.cta;}).join('\n\n');
   var btn=this;if(!t){btn.textContent='Ничего не выбрано';setTimeout(function(){btn.textContent='Копия'},1400);return;}
   var done=function(){btn.textContent='Скопировано ✓';setTimeout(function(){btn.textContent='Копия'},1400)};
   try{navigator.clipboard.writeText(t).then(done,function(){fallback(t);done();})}catch(e){fallback(t);done();}};
 function fallback(t){var a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(e){};a.remove();}
 document.getElementById('selSend').onclick=function(){var ids=cards.filter(function(c){return st[c.dataset.i]}).map(function(c){return +c.dataset.i+1});
   var btn=this;if(!ids.length){btn.textContent='Выбери тему';setTimeout(function(){btn.textContent='Отправить ✈'},1400);return;}
   var url='https://t.me/mukhlisa22092024_bot?start=pick_'+ids.join('-');
   btn.textContent='Отправлено ✓';var nt=document.getElementById('sentNote');if(nt){nt.style.display='block';}
   setTimeout(function(){try{if(tgw&&tgw.openTelegramLink){tgw.openTelegramLink(url);return;}}catch(e){}window.location.href=url;},900);};
 draw();
})();
</script>"""
    return (f'\n<!-- ИСТОРИИ -->\n<section id="s-stories" data-title="Темы">\n{css}\n'
            f'  <h2>Темы: 3 формата + воронка</h2>\n'
            f'  <p class="lead"><b>Выбери тему → «Отправить ✈» → нажми Start в боте.</b> Полный сценарий под выбранный формат появится во вкладке «Сценарий» в течение часа. 50 тем в трёх форматах: сторителлинг, тренд-туториал и экспертный кейс. Для историй и кейсов выбирай то, что реально было.</p>\n'
            f'  <div class="selbar"><span id="selN">Выбрано: 0</span><span style="display:flex;gap:6px"><button class="ghost" id="selOnly">Фильтр</button><button class="ghost" id="selCopy">Копия</button><button id="selSend">Отправить ✈</button></span></div><div id="sentNote" class="card" style="display:none;background:var(--good-bg);border-color:#bfe3cc;font-size:14px"><b>✅ Выбор отправлен в бот.</b> В чате это выглядит как «/start» — так и должно быть. Сценарий появится во вкладках «Выбранные» и «Сценарий» в течение часа.</div>\n'
            f'  {chips}\n  {fmts}\n'
            f'  {cards}\n'
            f'  <div class="card"><h3>Воронка в ChatPlace — одна на все ролики</h3>{flow}</div>\n'
            f'  <div class="card"><h3>Чек-лист публикации</h3><ul class="clean">{chk}</ul></div>\n'
            f'  <div class="card"><h3>Схема истории</h3><ul class="clean">{steps}</ul></div>\n'
            f'  <div class="card"><h3>Правила</h3><ul class="clean">{rules}</ul></div>\n'
            f'{js}\n</section>\n')


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "html":
        p = sys.argv[2]
        s = open(p, encoding="utf-8").read()
        m = re.search(r"\n<!-- ИСТОРИИ -->.*?</section>\n", s, flags=re.S)
        s = s[:m.start()] + html_tab() + s[m.end():]
        open(p, "w", encoding="utf-8").write(s)
        print("html ok")
    elif mode == "tg":
        token, chat = sys.argv[2], sys.argv[3]
        for m in tg_messages():
            out = subprocess.run(["curl", "-s", "-m", "30", f"https://api.telegram.org/bot{token}/sendMessage",
                                  "--form-string", f"chat_id={chat}", "--form-string", f"text={m}",
                                  "--form-string", "parse_mode=HTML"], capture_output=True, text=True).stdout
            r = json.loads(out); print("sendMessage", r.get("ok"), r.get("description", ""), len(m))
            time.sleep(0.6)
