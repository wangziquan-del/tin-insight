import json
import re
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


URL = "https://hq.sinajs.cn/rn=tin-pages&list=nf_SN0,hf_SND"
HEADERS = {
    "Referer": "https://finance.sina.com.cn/",
    "User-Agent": "Mozilla/5.0 (GitHub Actions; Tin Dashboard)",
}


def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def pct(last, reference):
    if last is None or reference in (None, 0):
        return None
    return (last - reference) / reference * 100


def clock(value):
    text = str(value or "")
    if len(text) == 6 and text.isdigit():
        return f"{text[:2]}:{text[2:4]}:{text[4:]}"
    return text


request = Request(URL, headers=HEADERS)
with urlopen(request, timeout=30) as response:
    text = response.read().decode("gb18030", errors="replace")

rows = {
    key: value.split(",")
    for key, value in re.findall(r'var hq_str_(\w+)="([^"]*)";', text)
}
sn = rows.get("nf_SN0")
lme = rows.get("hf_SND")
if not sn or len(sn) < 18 or not lme or len(lme) < 13:
    raise RuntimeError("Sina quote response is incomplete")

sn_last = number(sn[8])
sn_reference = next(
    (value for value in (number(item) for item in sn[18:]) if value and value > 100000),
    number(sn[10]),
)
lme_last = number(lme[0])
lme_reference = number(lme[7])
payload = {
    "updated_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds"),
    "source": "新浪期货行情",
    "sn": {
        "symbol": "SN0",
        "name": sn[0],
        "last": sn_last,
        "change_pct": pct(sn_last, sn_reference),
        "time": clock(sn[1]),
        "date": sn[17],
        "open_interest": number(sn[13]),
        "volume": number(sn[14]),
    },
    "lme": {
        "symbol": "SND",
        "name": lme[13] if len(lme) > 13 else "LME锡3个月",
        "last": lme_last,
        "change_pct": pct(lme_last, lme_reference),
        "time": lme[6],
        "date": lme[12],
    },
}
Path("quotes.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(json.dumps(payload, ensure_ascii=False))
