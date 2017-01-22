import requests
from bs4 import BeautifulSoup as bs


main_url = "https://list.jd.com/list.html?cat=1713,12775"

req = requests.get(main_url)

soup = bs(req.content,'html5lib')

url_str ="https://list.jd.com{t}"

ul = soup.find('ul', class_='menu-drop-list')

data = []

a_list = ul.find_all('a')

for a in a_list:
    one = {
        "url":url_str.format(t=a["href"]),
        "classify":a.text
    }
    print one["url"].encode('utf-8'),",",one["classify"].encode('utf-8')
    data.append(one)

l = [
['https://list.jd.com/list.html?cat=1713,3258' , '小说'],
['https://list.jd.com/list.html?cat=1713,3259' , '文学'],
['https://list.jd.com/list.html?cat=1713,3260' , '青春文学'],
['https://list.jd.com/list.html?cat=1713,3261' , '传记'],
['https://list.jd.com/list.html?cat=1713,12775' , '绘画'],
['https://list.jd.com/list.html?cat=1713,12776' , '摄影'],
['https://list.jd.com/list.html?cat=1713,13627' , '书法'],
['https://list.jd.com/list.html?cat=1713,13634' , '音乐'],
['https://list.jd.com/list.html?cat=1713,3262' , '艺术'],
['https://list.jd.com/list.html?cat=1713,3263' , '童书'],
['https://list.jd.com/list.html?cat=1713,3267' , '励志与成功'],
['https://list.jd.com/list.html?cat=1713,3266' , '管理'],
['https://list.jd.com/list.html?cat=1713,3264' , '经济'],
['https://list.jd.com/list.html?cat=1713,3265' , '金融与投资'],
['https://list.jd.com/list.html?cat=1713,13613' , '孕产/胎教'],
['https://list.jd.com/list.html?cat=1713,3270' , '育儿/家教'],
['https://list.jd.com/list.html?cat=1713,3271' , '旅游/地图'],
['https://list.jd.com/list.html?cat=1713,9278' , '烹饪/美食'],
['https://list.jd.com/list.html?cat=1713,9291' , '时尚/美妆'],
['https://list.jd.com/list.html?cat=1713,9301' , '家居'],
['https://list.jd.com/list.html?cat=1713,9309' , '婚恋与两性'],
['https://list.jd.com/list.html?cat=1713,9314' , '娱乐/休闲'],
['https://list.jd.com/list.html?cat=1713,3269' , '健身与保健'],
['https://list.jd.com/list.html?cat=1713,3272' , '动漫'],
['https://list.jd.com/list.html?cat=1713,3273' , '历史'],
['https://list.jd.com/list.html?cat=1713,3279' , '心理学'],
['https://list.jd.com/list.html?cat=1713,3276' , '政治/军事'],
['https://list.jd.com/list.html?cat=1713,3275' , '国学/古籍'],
['https://list.jd.com/list.html?cat=1713,3274' , '哲学/宗教'],
['https://list.jd.com/list.html?cat=1713,3277' , '法律'],
['https://list.jd.com/list.html?cat=1713,3280' , '文化'],
['https://list.jd.com/list.html?cat=1713,3281' , '社会科学'],
['https://list.jd.com/list.html?cat=1713,9340' , '科普读物'],
['https://list.jd.com/list.html?cat=1713,3287' , '计算机与互联网'],
['https://list.jd.com/list.html?cat=1713,3284' , '建筑'],
['https://list.jd.com/list.html?cat=1713,3285' , '医学'],
['https://list.jd.com/list.html?cat=1713,3282' , '工业技术'],
['https://list.jd.com/list.html?cat=1713,9351' , '电子与通信'],
['https://list.jd.com/list.html?cat=1713,9368' , '农业/林业'],
['https://list.jd.com/list.html?cat=1713,3286' , '科学与自然'],
['https://list.jd.com/list.html?cat=1713,3288' , '体育/运动'],
['https://list.jd.com/list.html?cat=1713,3289' , '中小学教辅'],
['https://list.jd.com/list.html?cat=1713,11047' , '大中专教材教辅'],
['https://list.jd.com/list.html?cat=1713,3290' , '考试'],
['https://list.jd.com/list.html?cat=1713,3291' , '外语学习'],
['https://list.jd.com/list.html?cat=1713,3294' , '字典词典/工具书'],
['https://list.jd.com/list.html?cat=1713,4758' , '杂志/期刊'],
['https://list.jd.com/list.html?cat=1713,4855' , '进口原版'],
['https://list.jd.com/list.html?cat=1713,6929' , '港台图书'],
['https://list.jd.com/list.html?cat=1713,3296' , '套装书'],
['https://list.jd.com/list.html?cat=1713,11745' , '文化用品'],
]
