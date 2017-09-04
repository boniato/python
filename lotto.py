# -*- coding: UTF-8 -*-

import requests
import pymysql
import sys
from bs4 import BeautifulSoup

'''
content="나눔로또 769회 당첨번호 5,7,11,16,41,45+4. 1등 총 9명, 1인당 당첨금
'''

paramList = []

basic_url = "http://nlotto.co.kr/gameResult.do?method=byWin&drwNo="


def scrapingData():
   
    for i in range(1, 6): #1~5회까지 실행
        resp = requests.get(basic_url + str(i))
        soup = BeautifulSoup(resp.text, "lxml")
        line = str(soup.find("meta", {"id" : "desc", "name" : "description"})['content']) 
        
        begin = line.find("당첨번호") 
        begin = line.find(" ", begin) + 1 
        end = line.find(".", begin) 
        numbers = line[begin:end] 
        
        param={}
        param["count"] = i #회차
        param["numbers"] = numbers #당첨번호(Winning Numbers)
        
        paramList.append(param)
        
            
def insertData():

        conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       db='mysql',
                       user='lee',
                       password='yourPassword', #None
                       charset='utf8'
                       )
        
        cursor = conn.cursor()
              
        for dic in paramList: 
            count = dic["count"] 
            numbers = dic["numbers"]  
            
            numberList = str(numbers).split(",") 
            #print("numberList: " + str(numberList))
          
            try:
                with conn.cursor() as cursor:
                    sql = 'INSERT INTO LOTTO (count, num1, num2, num3, num4, num5, num6, num7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                    print("sql: " + str(sql))
                    cursor.execute(sql, (count, numberList[0], numberList[1], numberList[2], numberList[3], numberList[4], numberList[5].split("+")[0], numberList[5].split("+")[1]) )
                conn.commit() 
            except: 
                print(sys.exc_info()[0]) 
                conn.rollback() 
                break 

        conn.close()
                
         
def main():
    
    scrapingData()
    
    insertData() 
    
    ''' 무한루프 돌아서 뺌
    if __name__ == "__main__": 
        main()
    '''

main()