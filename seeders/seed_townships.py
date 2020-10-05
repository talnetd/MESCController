from app import db
from app.models import Townships, Regions


data = [
    {"name_en": "Amarapura", "name_my": "အမရပူရ", "region": "Mandalay Region"},
    {
        "name_en": "Aungmyaythazan",
        "name_my": "အောင်မြေသာစံ",
        "region": "Mandalay Region",
    },
    {
        "name_en": "Chanayethazan",
        "name_my": "ချမ်းအေးသာစံ",
        "region": "Mandalay Region",
    },
    {
        "name_en": "Chanmyathazi",
        "name_my": "ချမ်းမြသာစည်",
        "region": "Mandalay Region",
    },
    {
        "name_en": "Kyaukpadaung",
        "name_my": "ကျောက်ပန်းတောင်း",
        "region": "Mandalay Region",
    },
    {"name_en": "Kyaukse", "name_my": "ကျောက်ဆည်", "region": "Mandalay Region"},
    {"name_en": "Madaya", "name_my": "မတ္တရာ", "region": "Mandalay Region"},
    {"name_en": "Mahaaungmyay", "name_my": "မဟာအောင်မြေ", "region": "Mandalay Region",},
    {"name_en": "Mahlaing", "name_my": "မလှိုင်", "region": "Mandalay Region"},
    {"name_en": "Meiktila", "name_my": "မိတ္ထီလာ", "region": "Mandalay Region"},
    {"name_en": "Mogoke", "name_my": "မိုးကုတ်", "region": "Mandalay Region"},
    {"name_en": "Myingyan", "name_my": "မြင်းခြံ", "region": "Mandalay Region"},
    {"name_en": "Myittha", "name_my": "မြစ်သား", "region": "Mandalay Region"},
    {"name_en": "Natogyi", "name_my": "နွားထိုးကြီး", "region": "Mandalay Region"},
    {"name_en": "Ngazun", "name_my": "ငါန်းဇွန်", "region": "Mandalay Region"},
    {"name_en": "Nyaung-U", "name_my": "ညောင်ဦး", "region": "Mandalay Region"},
    {"name_en": "Patheingyi", "name_my": "ပုသိမ်ကြီး", "region": "Mandalay Region"},
    {"name_en": "Pyawbwe", "name_my": "ပျော်ဘွယ်", "region": "Mandalay Region"},
    {
        "name_en": "Pyigyitagon",
        "name_my": "ပြည်ကြီးတံခွန်",
        "region": "Mandalay Region",
    },
    {"name_en": "Pyinoolwin", "name_my": "ပြင်ဦးလွင်", "region": "Mandalay Region"},
    {"name_en": "Singu", "name_my": "စဉ့်ကူး", "region": "Mandalay Region"},
    {"name_en": "Sintgaing", "name_my": "စဉ့်ကိုင်", "region": "Mandalay Region"},
    {"name_en": "Tada-U", "name_my": "တံတားဦး", "region": "Mandalay Region"},
    {"name_en": "Taungtha", "name_my": "တောင်သာ", "region": "Mandalay Region"},
    {"name_en": "Thabeikkyin", "name_my": "သပိတ်ကျင်း", "region": "Mandalay Region"},
    {"name_en": "Thazi", "name_my": "သာစည်", "region": "Mandalay Region"},
    {"name_en": "Wundwin", "name_my": "ဝမ်းတွင်း", "region": "Mandalay Region"},
    {"name_en": "Yamethin", "name_my": "ရမည်းသင်း", "region": "Mandalay Region"},
]


def seed(user=None):
    for each in data:
        each["created_by"] = user
        each["changed_by"] = user
        region = db.session.query(Regions).filter_by(name_en=each.get("region")).first()
        if not region:
            continue

        found = (
            db.session.query(Townships).filter_by(name_en=each.get("name_en")).first()
        )
        if not found:
            each["region_id"] = region.id
            each["region"] = region
            record = Townships(**each)
            db.session.add(record)
            db.session.commit()
