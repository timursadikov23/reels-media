"""Rebuild the «Темы» tab of tv-dash-7k3p/index.html in place from tools/tv_topics.py.

Usage: python3 rebuild_topics.py ../index.html
Add a new format: put it into FORMATS (key, name, short, labels[4], about) and append 10 topics to TOPICS
with T(title_ru, fmt_key, hook_uz, [4 beats], CODE, CYR, bonus_uz, accusative_uz) in tv_topics.py.
"""
import importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tv_topics import TOPICS, FORMATS

p = sys.argv[1]
s = open(p, encoding="utf-8").read()
spec = importlib.util.spec_from_file_location("stories", os.path.join(HERE, "stories.py"))
st = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(st)
except ModuleNotFoundError:  # stories.py imports Mukhlisa topic files at top level; not needed here
    src = open(os.path.join(HERE, "stories.py"), encoding="utf-8").read()
    src = re.sub(r"import os as _os, sys as _sys.*?T \+= T3 \+ T4; FUN \+= FUN3 \+ FUN4; ACC \+= ACC3 \+ ACC4\n", "", src, flags=re.S)
    st.__dict__["__file__"] = os.path.join(HERE, "stories.py")
    exec(compile(src, "stories.py", "exec"), st.__dict__)
st.T = TOPICS
st.FORMATS = FORMATS
st.METHOD = [("Факты", "Каждая цифра, цена и правило — из свежего источника с датой; без подтверждения цифра не используется."),
             ("Медиа", "Только реальные: свои кадры, Pexels, Wikimedia Commons, скриншоты App Store. Никаких нарисованных интерфейсов и чужих видео."),
             ("Голос", "Узбекский (латиница), разговорный, твой голос; «Shuncha pulga?!» где уместно; ~2,6 слова/с."),
             ("Сборка", "F1–F3 — через tripvibe-engine: new → stills → render → дубль с твоей съёмкой → финал −14 LUFS + .srt.")]
st.RULES = ["Не больше 4 Reels в неделю.", "Субтитры UZ + RU/EN на ключевых моментах — для Москвы, Стамбула, Казахстана.",
            "Не вкладывать в твои уста опыт, которого не было.", "Каждый ролик заканчивается кодом для ChatPlace с проверкой подписки."]
n_fmt = len(FORMATS)
word = {3: "3 формата", 4: "4 формата", 5: "5 форматов", 6: "6 форматов", 7: "7 форматов"}.get(n_fmt, f"{n_fmt} форматов")
tab = st.html_tab()
tab = (tab.replace("mukhlisa_story_pick_v1", "tripvibe_pick_v1").replace("mukhlisa22092024_bot", "timurblog222024_bot")
          .replace("<h3>3 формата</h3>", f"<h3>{word}</h3>").replace("Темы: 3 формата + воронка", f"Темы: {word} + воронка")
          .replace("Полный сценарий под выбранный формат появится во вкладке «Сценарий» в течение часа. 50 тем в трёх форматах: сторителлинг, тренд-туториал и экспертный кейс. Для историй и кейсов выбирай то, что реально было.",
                   f"Полный сценарий под формат появится во вкладке «Сценарий» в течение часа. {len(TOPICS)} тем в {n_fmt} форматах: F1–F3 — твои фиксированные форматы, F4 — «локация + вопрос» из данных, F5–F7 — форматы из референсов, адаптированные под travel.")
          .replace("<h3>Схема истории</h3>", "<h3>Производство</h3>")
          .replace("Kanalda barcha topilmalar ssilkalari bor", "Kanalda barcha lokatsiyalar va ro'yxatlar bor")
          .replace("Va'da qilganimni tayyorlab qo'ydim", "Va'da qilgan ma'lumotni tayyorlab qo'ydim")
          .replace("@mukhlisasadikova_", "@tripvibeuz"))
m = re.search(r"\n<!-- ИСТОРИИ -->.*?</section>\n", s, flags=re.S)
s = s[:m.start()] + tab + s[m.end():]
open(p, "w", encoding="utf-8").write(s)
print("topics", len(TOPICS), "formats", n_fmt)
