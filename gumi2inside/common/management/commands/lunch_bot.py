import requests
import datetime

from django.core.management.base import BaseCommand

from common.models import Lunch


class Command(BaseCommand):
    help = 'update lunch menu'

    #### welstory 식단표
    def update_lunch(self, menuCourseType):
        ## 식단 날짜
        # 년원일 형식
        date = datetime.date.today()
        # week = datetime.datetime.weekday(date)
        # while week:
        #     date = date - datetime.timedelta(days=1)
        #     week = datetime.datetime.weekday(date)

        date = str(date).split()[0].replace("-", "")
        ## restaurantCode 분류
        # 서울 : REST000133
        # 부울경 : REST000595
        # 구미 : REST000213
        restaurantCode = 'REST000213'

        ## hallNo 분류
        # 서울 : E110
        # 부울경 : E32
        # 구미 : E21F
        hallNo = "E21F"

        ## menuCourseType 분류
        # 서울 : ["BB", "CC"]
        # 부울경 : ["AA", "BB", "CC", "DD", "EE", "JK", "ZZ", "JJ", "KK", "MM", "NN", "OO", "PP", "RR", "SS", "T2", "T3", "WF"]
        # 구미 : ["AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II" , "JJ", "KK", "LL", "MM", "NN", "OO"]
        # menuCourseType = "AA"

        url = f"https://welplus.welstory.com/api/meal/detail?menuDt={date}&hallNo={hallNo}&menuCourseType={menuCourseType}&menuMealType=2&restaurantCode={restaurantCode}"

        ## 인증 쿠키
        # remember-me : 회원정보 세션 
        cookies = {
            'remember-me':'anVuaG9uZzYyNToyNjE5MzkyNTc2NTM2OjJmZGMyMzEyY2MyN2FmMDU2ZjU0YjRmOGNkZTMwMjRk',
        }

        ## 점심 관련 주요 정보
        # res['data'] : 점심 메뉴 리스트
        # res['data']['subMenuTxt'] : 메뉴
        # res['data']['sumKcal'] : 칼로리
        # res['data']['totCho'] : 탄수화물
        # res['data']['totNa'] : 나트륨
        # res['data']['totFat'] : 지방
        # res['data']['totProtein'] : 단백질
        res = requests.get(url, cookies=cookies).json()

        main_menu, sub_menu = "", ""
        kcal, carbs, protein, fat, sodium = 0, 0, 0, 0, 0
        image_url = ""
        for idx, menu in enumerate(res['data']):
            if idx == 0:
                image_url = menu['photoUrl']+menu['photoCd'] if menu['photoUrl'] and menu['photoCd'] else ""
                main_menu = menu['menuName']
            else: 
                sub_menu += f", {menu['menuName']}" if sub_menu else menu['menuName']
            if not kcal:
                kcal = menu['sumKcal']
                carbs = menu['totCho']
                protein = menu['totProtein']
                fat = menu['totFat']
                sodium = menu['totNa']

        print(f"메인 메뉴 : {main_menu}")
        print(f"서브 메뉴 : {sub_menu}")
        print(f"칼로리 : {kcal}kcal")
        print(f"성분표 : [탄수화물 : {carbs}g, 나트륨 : {sodium}mg , 지방 : {fat}g, 단백질 : {protein}g]")
        print(f"사진 : {image_url}")
        print()

        parsed_date = datetime.datetime.strptime(date, '%Y%m%d').date()

        lunch_instance = Lunch(
            date=parsed_date,
            menuCourseType=menuCourseType,
            main_menu=main_menu,
            sub_menu=sub_menu,
            kcal=kcal,
            carbs=carbs,
            sodium=sodium,
            fat=fat,
            protein=protein,
            image_url=image_url
        )
        lunch_instance.save()
    
    def handle(self, *args, **options):
        self.update_lunch("AA")
        self.update_lunch("BB")
