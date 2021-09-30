import requests
from bs4 import BeautifulSoup
import json


def parser():
    headers = {

        "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.186"
    }
    req = requests.get("https://kinobrest.by",headers=headers)
    soup = BeautifulSoup(req.text,'lxml')
    datas_array = [(i['href'].replace('#',""),i.text) for i in soup.find('div',class_='tabs movies').find_all('a')][0:7]
    main_div = soup.find('div',class_='row movie-tabs')
    days_array = [(i[1],main_div.find('div',id=i[0])) for i in datas_array]
    end_dict = {}
    for arr in days_array:
        day_arr = []
        day = arr[1]
        col_sm = day.find_all('div',class_='col-sm-6')
        for i in col_sm:
            col45 = i.find('div',class_='col-md-4 col-sm-5')
            a = col45.find('a')
            href = a['href']
            img_href = "https://kinobrest.by" + a.find('img')['src']
            title = a['title']
            col87 = i.find('div',class_='col-md-8 col-sm-7')
            info = col87.find_all('span',class_='time')
            array_info = [i.text.strip().replace('\t',"") for i in info]
            day_arr.append({href.replace("https://kinobrest.by/events/",""):{
                'title':title,
                "href": href,
                "img_href": img_href,
                'info': array_info,
            }})
        end_dict[arr[0]] = {'array': day_arr,'callback_data': 'f' + arr[0]}
    with open('files/endless.json', 'w', encoding='utf-8') as f:
        json.dump(end_dict,f,indent=3)


if __name__ == '__main__':
    parser()
