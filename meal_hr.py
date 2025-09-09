# meal_hr.py
from datetime import datetime
import requests
from PIL import Image, ImageDraw, ImageFont
from instagrapi import Client
import schedule
import time
import os
from dotenv import load_dotenv

# variable
ATPT_OFCDC_SC_CODE = "K10"
API_KEY = "8406d826006347e8800608cc7098a415"
SD_SCHUL_CODE = "7863058"

IMG_WIDTH = 1080
IMG_HEIGHT = 1920
FONT_PATH = "HAKGYOANSIM NADUERI TTF L"
FONT_SIZE = 28

IG_USERNAME = "meal.hr" 
IG_PASSWORD = "haerangmslunch"

# information
def get_today_meal():
    today = datetime.now().strftime("%Y%m%d")
    
    base_url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    url = f"{base_url}?KEY={API_KEY}&Type=json&pIndex=1&pSize=10&ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}&SD_SCHUL_CODE={SD_SCHUL_CODE}&MLSV_YMD={today}"
    
    res = requests.get(url)
    data = res.json()
    try:
        meal_text = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'].replace("<br/>","\n")
        nutrition_text = data['mealServiceDietInfo'][1]['row'][0].get('NTR_INFO','영양 정보 없음')
        return meal_text, nutrition_text
    except:
        return "오늘은 급식 정보가 없어요", ""
    
# image
def create_meal_image(meal_text, nutrition_text, filename="meal.png"):
    img = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    draw.text((50, 30), f"오늘의 급식 ({today_str}) 🍴", fill=(0,0,0), font=font)
    draw.text((50, 100), meal_text, fill=(0,0,0), font=font)
    draw.text((50, 600), f"영양 정보:\n{nutrition_text}", fill=(0,0,0), font=font)
    
    img.save(filename)
    return filename

# story upload
cl = Client()
cl.login(IG_USERNAME, IG_PASSWORD)

def upload_story(image_path, caption="오늘 급식 🍴"):
    cl.photo_upload_to_story(image_path, caption)
def post_story():
    meal_text, nutrition_text = get_today_meal()
    image_file = create_meal_image(meal_text, nutrition_text)
    upload_story(image_file)
    print("스토리 업로드 완료!")

# .evi
load_dotenv()

API_KEY = os.getenv("NEIS_API_KEY")
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

# scheduling
schedule.every().day.at("07:00").do(post_story)

while True:
    schedule.run_pending()
    time.sleep(1)
