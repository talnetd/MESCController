import os
import random
import click
import uuid
from datetime import timedelta
from faker import Faker
from app import db
from app.models import Titles, Regions, Townships, Meterboxes, Customers, Bills
from flask_appbuilder.security.sqla.models import User


due_one_day = timedelta(days=1)
faker_obj = Faker()


wards = [
    "မှန်တန်းရပ်ကွက်",
    "ကျန်တန်းရပ်ကွက်",
    "လေးစုရပ်ကွက်",
    "အိုးတော်ရပ်ကွက်",
    "ရွှေဂွမ်းထုတ်ရပ်ကွက်",
    "ဆင်စွယ်ပွတ်ရပ်ကွက်",
    "တောင်ကြီးရပ်ကွက်",
    "ဈေးချိုရပ်ကွက်",
    "မြစ်ငယ်ရပ်ကွက်",
    "အနှိပ်တော်ရပ်ကွက်",
    "အမရဌာနီ (အရှေ့) ရပ်ကွက်",
    "အမရဌာနီ (အနောက်) ရပ်ကွက်",
    "အောင်မြေသာစံမြို့ရပ်ကွက်",
    "ဘုန်းတော်တိုးရပ်ကွက်",
    "ဒေါနဘွားရပ်ကွက်",
    "မဟာဇေယျာဘုံရပ်ကွက်",
    "မေဃဂီရိရပ်ကွက်",
    "မင်းတဲအီကင်းရပ်ကွက်",
    "ညောင်ကွဲရပ်ကွက်",
    "အိုးဘိုရပ်ကွက်",
    "ပုလဲငွေရောင်ရပ်ကွက်",
    "ပြည်ကြီးကျက်သရေ (အရှေ့) ရပ်ကွက်",
    "ပြည်ကြီးကျက်သရေ (အနောက်) ရပ်ကွက်",
    "ပြည်ကြီးရန်လုံရပ်ကွက်",
    "ပြည်လုံးချမ်းသာရပ်ကွက်",
    "သီရိမာလာ (အရှေ့) ရပ်ကွက်",
    "သီရိမာလာ (အနောက်) ရပ်ကွက်",
    "ဥပုသ်တော်ရပ်ကွက်",
    "အောင်နန်းရိပ်သာ (အရှေ့) ရပ်ကွက်",
    "အောင်နန်းရိပ်သာ (အနောက်) ရပ်ကွက်",
    "ချမ်းအေးသာစံ (အရှေ့) ရပ်ကွက်",
    "ချမ်းအေးသာစံ (အလယ်) ရပ်ကွက်",
    "ချမ်းအေးသာစံ (အနောက်) ရပ်ကွက်",
    "ဒေးဝန်း (အနောက်) ရပ်ကွက်",
    "ဟေမာဇလရပ်ကွက်",
    "ကံကောက်ရပ်ကွက်",
    "ကဉ္စနမဟီရပ်ကွက်",
    "မောရဂီဝါရပ်ကွက်",
    "ပါတ်ကုန်းပျော်ဘွယ်ရပ်ကွက်",
    "ပါတ်ကုန်းဝန်းကျင်ရပ်ကွက်",
    "ပြည်ကြီးမျက်မှန်ရပ်ကွက်",
    "ပြည်ကြီးမျက်ရှင်ရပ်ကွက်",
    "ပြည်ကြီးပျော်ဘွယ် (အရှေ့) ရပ်ကွက်",
    "ပြည်ကြီးပျော်ဘွယ် (အနောက်) ရပ်ကွက်",
    "စိတ္တရမဟီရပ်ကွက်",
    "သီရိဟေမာ (အရှေ့) ရပ်ကွက်",
    "သီရိဟေမာ (အနောက်) ရပ်ကွက်",
    "ရန်မျိုးလုံရပ်ကွက်",
    "အောင်ပင်လယ်ရပ်ကွက်",
    "အောင်သာယာရပ်ကွက်",
    "ချမ်းမြသာစည် (တောင်)ရပ်ကွက်",
    "ထွန်တုံးရပ်ကွက်",
    "ကန်သာယာရပ်ကွက်",
    "ကျွန်းလုံးဥသျှောင်ရပ်ကွက်",
    "မြရည်နန္ဒာရပ်ကွက်",
    "မြို့သစ်အမှတ် (၁) ရပ်ကွက်",
    "မြို့သစ်အမှတ် (၂) ရပ်ကွက်",
    "မြို့သစ်အမှတ် (၃) ရပ်ကွက်",
    "မြို့သစ်အမှတ် (၄) ရပ်ကွက်",
    "မြို့သစ်အမှတ် (၅) ရပ်ကွက်",
    "တမ္ပဝတီရပ်ကွက်",
    "သံလျှက်မော် (တောင်) ရပ်ကွက်",
    "အောင်မင်္ဂလာရပ်ကွက်",
    "ဘူတာရပ်ကွက်",
    "လွတ်လပ်ရေးရပ်ကွက်",
    "မြောက်ပြည်တော်သာရပ်ကွက်",
    "မြို့မတောင်ရပ်ကွက်",
    "မြို့မကွက်သစ်ရပ်ကွက်",
    "မြို့မရပ်ကွက်",
    "စံပြရပ်ကွက်",
    "တမ္ပဝတီရပ်ကွက်",
    "သာယာရေးရပ်ကွက်",
    "သီရိမင်္ဂလာရပ်ကွက်",
    "ဈေးကွက်သစ်ရပ်ကွက်",
    "ဧမြကြည်လင်ရပ်ကွက်",
    "ဘောဂဝတီရပ်ကွက်",
    "ဖောင်ရွာရပ်ကွက်",
    "ကြက်မင်းတွန်ရပ်ကွက်",
    "မင်းရပ်-ရပ်ကွက်",
    "ပြည်လုံးနိုင်ရပ်ကွက်",
    "စုကြီးရပ်ကွက်",
    "ဆူးကုန်းရပ်ကွက်",
    "ရဲစုရပ်ကွက်",
    "ဈေးတန်းရပ်ကွက်",
    "အမှတ် (၁) ရပ်ကွက်",
    "အမှတ် (၂) ရပ်ကွက်",
    "အမှတ် (၃) ရပ်ကွက်",
    "အမှတ် (၄) ရပ်ကွက်",
    "အမှတ် (၅) ရပ်ကွက်",
    "ချမ်းမြသာစည် (မြောက်) ရပ်ကွက်",
    "ဒေးဝန်း (အရှေ့) ရပ်ကွက်",
    "ဟေမမာလာ (မြောက်) ရပ်ကွက်",
    "ဟေမမာလာ (တောင်) ရပ်ကွက်",
    "မဟာအောင်မြေ (အရှေ့) ရပ်ကွက်",
    "မဟာအောင်မြေ (အနောက်) ရပ်ကွက်",
    "မဟာမြိုင်ရပ်ကွက် (၁) ရပ်ကွက်",
    "မဟာမြိုင်ရပ်ကွက် (၂) ရပ်ကွက်",
    "မဟာနွယ်စဉ်ရပ်ကွက်",
    "စိန်ပန်းရပ်ကွက်",
    "စကြာနွယ်စဉ်ရပ်ကွက်",
    "ရွှေဘုန်းရှိန်ရပ်ကွက်",
    "တက္ကသိုလ်ရပ်ကွက်",
    "သံလျက်မော် (အရှေ့) ရပ်ကွက်",
    "သံလျက်မော် (အနောက်) ရပ်ကွက်",
    "ရတနာဘုမ္မိ (အရှေ့) ရပ်ကွက်",
    "ရတနာဘုမ္မိ (အနောက်) ရပ်ကွက်",
    "ရဲမွန်တောင်ရပ်ကွက်",
    "အမှတ် (၁) ရပ်ကွက်",
    "အမှတ် (၂) ရပ်ကွက်",
    "အမှတ် (၃) ရပ်ကွက်",
    "အမှတ် (၄) ရပ်ကွက်",
    "အရှေ့ပြင်ရပ်ကွက်",
    "အောင်ဆန်းရပ်ကွက်",
    "အောင်ဇေယျာရပ်ကွက်",
    "ချည်စက်ရပ်ကွက်",
    "ကြည်တော်ကုန်းရပ်ကွက်",
    "မြို့မရပ်ကွက်",
    "နန်းတော်ကုန်းရပ်ကွက်",
    "ပေါက်ချောင်းရပ်ကွက်",
    "ပြည်သာယာရပ်ကွက် (မြောက်)",
    "ပြည်သာယာရပ်ကွက် (တောင်)",
    "သီရိမင်္ဂလာရပ်ကွက်",
    "ဝန်းဇင်းရပ်ကွက်",
    "ရတနာမာန်အောင်ရပ်ကွက်",
    "ရန်မျိုးအောင်ရပ်ကွက်",
    "လယ်ဦးရပ်ကွက်",
    "မင်းတံတားရပ်ကွက်",
    "မြို့မရပ်ကွက်",
    "ရှောလီဝိုင်းရပ်ကွက်",
    "ရေပူရပ်ကွက်",
    "အမှတ် (၁) ရပ်ကွက်",
    "အမှတ် (၁၀) ရပ်ကွက်",
    "အမှတ် (၁၁) ရပ်ကွက်",
    "အမှတ် (၁၂) ရပ်ကွက်",
    "အမှတ် (၁၃) ရပ်ကွက်",
    "အမှတ် (၁၄) ရပ်ကွက်",
    "အမှတ် (၁၅) ရပ်ကွက်",
    "အမှတ် (၁၆) ရပ်ကွက်",
    "အမှတ် (၁၇) ရပ်ကွက်",
    "အမှတ် (၁၈) ရပ်ကွက်",
    "အမှတ် (၁၉) ရပ်ကွက်",
    "အမှတ် (၂) ရပ်ကွက်",
    "အမှတ် (၂၀) ရပ်ကွက်",
    "အမှတ် (၃) ရပ်ကွက်",
    "အမှတ် (၄) ရပ်ကွက်",
    "အမှတ် (၅) ရပ်ကွက်",
    "အမှတ် (၆) ရပ်ကွက်",
    "အမှတ် (၇) ရပ်ကွက်",
    "အမှတ် (၈) ရပ်ကွက်",
    "အမှတ် (၉) ရပ်ကွက်",
    "အမှတ် (၁) ရပ်ကွက်",
    "အမှတ် (၂) ရပ်ကွက်",
    "အမှတ် (၃) ရပ်ကွက်",
    "အမှတ် (၄) ရပ်ကွက်",
    "အမှတ် (၁) ရပ်ကွက်",
    "အမှတ် (၂) ရပ်ကွက်",
    "အမှတ် (၃) ရပ်ကွက်",
    "အမှတ် (၄) ရပ်ကွက်",
    "အမှတ် (၅) ရပ်ကွက်",
    "ဘူတာရပ်ကွက်",
    "မင်းကုန်းရပ်ကွက်",
    "မြို့မအရှေ့ရပ်ကွက်",
    "မြို့မအနောက်ရပ်ကွက်",
    "ရှမ်းပွဲရပ်ကွက်",
    "ရွှေသူဌေးရပ်ကွက်",
    "အမှတ် (၁) ရပ်ကွက်",
    "အမှတ် (၂) ရပ်ကွက်",
    "အမှတ် (၃) ရပ်ကွက်",
    "အမှတ် (၄) ရပ်ကွက်",
    "အမှတ် (၅) ရပ်ကွက်",
    "အမှတ် (၆) ရပ်ကွက်",
    "အမှတ် (၇) ရပ်ကွက်",
    "အမှတ် (၈) ရပ်ကွက်",
    "အမှတ် (၁)ရပ်ကွက်",
    "အမှတ် (၂)ရပ်ကွက်",
    "အမှတ် (၃)ရပ်ကွက်",
    "အမှတ် (၄)ရပ်ကွက်",
    "အနော်ရထာရပ်ကွက်",
    "အရှေ့ရွာနောင်ရပ်ကွက်",
    "ဂန့်ဂါရပ်ကွက် (ဟော်တယ်ဇုံ ၄)",
    "ကျန်စစ်သားရပ်ကွက်",
    "ရွှေတွင်းရပ်ကွက်",
    "သီရိပစ္စယာရပ်ကွက်",
    "အမှတ် (၁)ရပ်ကွက်",
    "အမှတ် (၂)ရပ်ကွက်",
    "အမှတ် (၃)ရပ်ကွက်",
    "အမှတ် (၄)ရပ်ကွက်",
    "အမှတ် (၁) ရပ်ကွက်",
    "အမှတ် (၂) ရပ်ကွက်",
    "အမှတ် (၃) ရပ်ကွက်",
    "အမှတ် (၄) ရပ်ကွက်",
    "အမှတ် (၅) ရပ်ကွက်",
    "အမှတ် (၆) ရပ်ကွက်",
    "အမှတ် (၇) ရပ်ကွက်",
    "မြို့မရပ်ကွက်",
    "မန္တလေးတန်းရပ်ကွက်",
    "မြင်းဘက်ရပ်ကွက်",
    "မြို့မရပ်ကွက်",
    "မြို့သစ်ရပ်ကွက်",
    "ပြည်သာယာရပ်ကွက်",
    "ရှမ်းပွဲရပ်ကွက်",
    "ရွှေပြည်ရန်အောင်ရပ်ကွက်",
    "ရွှေပြည်ရန်လုံရပ်ကွက်",
    "ရွှေပြည်ရန်နိုင်ရပ်ကွက်",
    "(ဃ) ရပ်ကွက်",
    "(ဂ) ရပ်ကွက်",
    "(က) ရပ်ကွက်",
    "(ခ) ရပ်ကွက်",
    "(င) ရပ်ကွက်",
    "(ဆ) ရပ်ကွက်",
    "(စ) ရပ်ကွက်",
    "(ဇ) ရပ်ကွက်",
    "(ဈ) ရပ်ကွက်",
    "ချမ်းမြသာယာရပ်ကွက်",
    "ထိန်ကုန်းရပ်ကွက်",
    "ငွေတော်ကြည်ကုန်းရပ်ကွက်",
    "တံခွန်တိုင်ရပ်ကွက်",
    "တောင်မြင့်ရပ်ကွက်",
    "သင်ပန်းကုန်းရပ်ကွက်",
    "ယာတော်ရပ်ကွက်",
    "နန္ဒဝန်ရပ်ကွက် (ရပ်ကွက်ကြီး-၉)",
    "ပဒေသာရပ်ကွက် (ရပ်ကွက်ကြီး-၈)",
    "ရပ်ကွက်ကြီး (၁)",
    "ရပ်ကွက်ကြီး (၁၀)",
    "ရပ်ကွက်ကြီး (၁၁)",
    "ရပ်ကွက်ကြီး (၁၂)",
    "ရပ်ကွက်ကြီး (၁၃)",
    "ရပ်ကွက်ကြီး (၁၄)",
    "ရပ်ကွက်ကြီး (၁၅)",
    "ရပ်ကွက်ကြီး (၁၆)",
    "ရပ်ကွက်ကြီး (၁၇)",
    "ရပ်ကွက်ကြီး (၁၈)",
    "ရပ်ကွက်ကြီး (၁၉)",
    "ရပ်ကွက်ကြီး (၂)",
    "ရပ်ကွက်ကြီး (၂၀)",
    "ရပ်ကွက်ကြီး (၂၁)",
    "ရပ်ကွက်ကြီး (၃)",
    "ရပ်ကွက်ကြီး (၄)",
    "ရပ်ကွက်ကြီး (၅)",
    "ရပ်ကွက်ကြီး (၆)",
    "ရပ်ကွက်ကြီး (၇)",
    "အမှတ် (၁) ရပ်ကွက်",
    "အမှတ် (၂) ရပ်ကွက်",
    "မြို့မရပ်ကွက်",
    "မြို့သစ်ရပ်ကွက်",
    "တရုပ်စုရပ်ကွက်",
    "ရန်အောင်မြင်ရပ်ကွက်",
    "ရွာနိုင်ရပ်ကွက်",
    "အမှတ် (၁) ရပ်ကွက်",
    "အမှတ် (၂) ရပ်ကွက်",
    "အမှတ် (၃) ရပ်ကွက်",
    "ဘူတာကုန်းရပ်ကွက်",
    "ဘုရားကြီးအနောက်ရပ်ကွက်",
    "မင်းစုရပ်ကွက်",
    "မြို့မရပ်ကွက်",
    "တန်းမြင့်ကျောင်းရပ်ကွက်",
    "ဈေးရပ်ကွက်",
    "အမှတ် (၁) ရပ်ကွက်",
    "အမှတ် (၂) ရပ်ကွက်",
    "အမှတ် (၃) ရပ်ကွက်",
    "ကဘဲ့ရပ်ကွက်",
    "ဆိပ်ကမ်းရပ်ကွက်",
    "အမှတ် (၁) ရပ်ကွက်",
    "အမှတ် (၂) ရပ်ကွက်",
    "အမှတ် (၃) ရပ်ကွက်",
    "အမှတ် (၄) ရပ်ကွက်",
    "အမှတ် (၅) ရပ်ကွက်",
    "အမှတ် (၆) ရပ်ကွက်",
    "အမှတ် (၇) ရပ်ကွက်",
    "သဲတောမြို့မအမှတ်(၁)ရပ်ကွက်",
    "သဲတောမြို့မအမှတ်(၂)ရပ်ကွက်",
    "သဲတောမြို့မအမှတ်(၃)ရပ်ကွက်",
    "ဝမ်းတွင်းမြို့မအမှတ်(၁)ရပ်ကွက်",
    "ဝမ်းတွင်းမြို့မအမှတ်(၂)ရပ်ကွက်",
    "ဝမ်းတွင်းမြို့မအမှတ်(၃)ရပ်ကွက်",
    "အောင်မင်္ဂလာရပ်ကွက်",
    "ကျောင်းတိုက်စုရပ်ကွက်",
    "မြို့မရပ်ကွက်",
    "ရွှေစည်းခုံရပ်ကွက်",
    "ဝါတိုးရပ်ကွက်",
    "(ည) ရပ်ကွက်",
    "(ဋ) ရပ်ကွက်",
]


class NamePicker:
    def __init__(self):
        self.names_male = get_names("sorted males.txt")
        self.names_female = get_names("sorted females.txt")
        self.used_names = list()

    def get_random_name(self, gender):
        names = self.names_male if gender == "male" else self.names_female
        picked = random.choice(names)
        while picked in self.used_names:
            reduced = list(set(names) - set(self.used_names))
            picked = random.choice(reduced)
        self.used_names.append(picked)
        return picked


def create_user():
    user = None
    user = db.session.query(User).filter_by(username="seeder").first()
    if not user:
        user = User(
            username="seeder",
            email="seeder@localhost",
            first_name="Data",
            last_name="Seeder",
            active=True,
        )
        db.session.add(user)
        db.session.commit()
    return user


def get_names(file_name):
    names = None
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(root_dir, "data", file_name)
    with open(data_file) as tmp_file:
        names = list(map(lambda x: x.strip(), tmp_file.readlines()))
    return names


@click.command()
@click.argument("total", type=int, default=100)
def main(total):

    titles = db.session.query(Titles).all()
    region = db.session.query(Regions).filter_by(name_en="Mandalay Region").first()
    townships = db.session.query(Townships).filter_by(region=region).all()
    name_picker = NamePicker()
    user = create_user()

    for i in range(total):
        meterbox_number = f"AG-{str(i+1).zfill(5)}"
        selected_title = random.choice(titles)
        selected_township = random.choice(townships)
        selected_ward = random.choice(wards)
        selected_name = None
        if selected_title.name_en.lower() in ["u", "ko"]:
            selected_name = name_picker.get_random_name("male")
        else:
            selected_name = name_picker.get_random_name("female")
        customer = Customers(
            title=selected_title,
            name_en=selected_name,
            name_my=None,
            nrc_number=None,
            township=selected_township,
            region=region,
            address="{}, {}".format(faker_obj.address(), selected_ward),
        )
        customer.created_by = user
        customer.changed_by = user
        db.session.add(customer)
        db.session.commit()
        meterbox = Meterboxes(box_number=meterbox_number, customer=customer)
        meterbox.created_by = user
        meterbox.changed_by = user
        db.session.add(meterbox)
        db.session.commit()
        reading_date = faker_obj.date_between(start_date="-1y", end_date="-6m")
        due_date = reading_date + due_one_day
        previous_reading = faker_obj.pyint(min_value=12345, max_value=34567)
        diff_reading = random.randrange(100, 500)
        current_reading = previous_reading + diff_reading
        sub_total = diff_reading * 30
        maintenance_fee = 500
        horsepower_fee = 0
        grand_total = sub_total + maintenance_fee + horsepower_fee
        bill = Bills(
            reading_date=reading_date,
            due_date=due_date,
            meterbox=meterbox,
            previous_reading=previous_reading,
            current_reading=current_reading,
            diff_reading=diff_reading,
            sub_total=sub_total,
            maintenance_fee=maintenance_fee,
            horsepower_fee=horsepower_fee,
            grand_total=grand_total,
            ref_code=uuid.uuid1(),
        )
        bill.created_by = user
        bill.changed_by = user
        db.session.add(bill)
        db.session.commit()


if __name__ == "__main__":
    main()
