import sys 
import requests
from bs4 import BeautifulSoup
import csv
import importlib

importlib.reload(sys)

# طلب تاريخ من المستخدم
date = input("Please enter a Date in the following format MM/DD/YYYY : ")
page = requests.get(f"https://www.yallakora.com/match-center/?date={date}")

def main(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    matches_details = []
    
    # جمع معلومات البطولات والمباريات
    championships = soup.find_all("div", {"class": "matchCard"})

    def get_match_info(championship):
        # الحصول على اسم البطولة
        championship_title = championship.contents[1].find("h2").text.strip()
        
        # جمع جميع المباريات من البطولات
        all_matches = championship.contents[3].find_all("div", {"class": "item finish liItem"})
        
        for match in all_matches:
            team_A = match.find('div', {'class': 'teams teamA'}).text.strip()
            team_B = match.find('div', {'class': 'teams teamB'}).text.strip()

            # الحصول على نتيجة المباراة
            match_result = match.find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

            # الحصول على وقت المباراة
            match_time = match.find('div', {'class': 'MResult'}).find('span', {'class': 'time'}).text.strip()

            # إضافة تفاصيل المباراة إلى القائمة
            matches_details.append({
                "Championship title": championship_title, 
                "Team A": team_A, 
                "Team B": team_B, 
                "Match Time": match_time, 
                "Score": score
            })
    
    # تطبيق الدالة على جميع البطولات
    for championship in championships:
        get_match_info(championship)
    
    # حفظ البيانات في ملف CSV مع الترميز UTF-8
    keys = matches_details[0].keys()
    
    with open('E:/python/Projects/matches-details.csv', 'w', encoding='utf-8-sig', errors='ignore') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)

# تشغيل الدالة
main(page)

