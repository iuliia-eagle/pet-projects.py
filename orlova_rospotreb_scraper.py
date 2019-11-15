from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
df = pd.DataFrame(columns=['appeal_id', 'appeal_date', 'response_date', 'region', 'category', 'appeal_text', 'response_text'])

#Путь к Chrome webdriver
chromedriver_path = r"C:\Python37\chromedriver.exe"
#Адрес сайта жалоб
URL = 'http://zpp.rospotrebnadzor.ru/Forum/Appeals'

#Инициализация webdriver
driver = webdriver.Chrome(chromedriver_path)
driver.get(URL)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

#Поиск количества страниц
results = soup.find_all('div', attrs={'class': 'appeal-element'})
pages_num_info = soup.find('input', attrs={'id': 'appeals-list-number-of-pages'})
num_pages = int(pages_num_info['value'])
print(num_pages)
#Цикл по страницам
for j in range(num_pages):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', attrs={'class': 'appeal-element'})
    #Цикл по жалобам на странице
    for i in range(len(results)):
        print("Найдено", len(results), "записей")
        category_tag = results[i].find('p', attrs={'class': 'appeal-cat-title'})
        category = category_tag.text
        appeal_link = results[i].find('a', attrs={'class': 'appeal-title-link'})
        link = appeal_link['href']
        print(link)

        # Extract id from link (/Forum/Appeals/Details/<id>)
        appeal_id = int(link[23:])

        # print("Категория: ", category.text)
        print(appeal_id)

        appeal_info = results[i].find_all('p', attrs={'class': 'appeal-element-bottom'})
        appeal_date = appeal_info[0].contents[1][1:]
        region = appeal_info[2].contents[1][1:]
        print(category)
        print(appeal_date)
        # print(appeal_info[1])
        print(region)

        r_details = requests.get('http://zpp.rospotrebnadzor.ru' + link)
        soup_details = BeautifulSoup(r_details.text, 'html.parser')
        results_details = soup_details.find_all('div', attrs={'id': 'mainbody'})

        appeal_text_info = results_details[0].find('p', attrs={'class': 'appeal-details-message'})
        if appeal_text_info is not None:
            appeal_text = appeal_text_info.text
        appeal_response_info = results_details[0].find('p', attrs={'class': 'appeal-comments-message'})
        if appeal_response_info is not None:
            response_text = appeal_response_info.text

        appeal_c_d = results_details[0].find('p', attrs={'class': 'appeal-comments-date'})
        if appeal_c_d is not None:
            response_date = appeal_c_d.text[:10] + ';' + appeal_c_d.text[12:]
        df = df.append({'appeal_id': appeal_id, 'appeal_date': appeal_date, 'region': region, 'category': category,
                        'appeal_text': appeal_text, 'response_text': response_text, 'response_date': response_date},
                       ignore_index=True)

    if j == num_pages:
        break
    else:
        driver.find_element_by_link_text('Следующая').click()

df['appeal_date'] = pd.to_datetime(df['appeal_date'])
df['response_date'] = pd.to_datetime(df['response_date'])

df.to_pickle('appeals.pk1')
df.to_csv('appeals.csv', header=True, index=False, encoding='utf-8')

#with pd.option_context('display.max_rows', None, 'display.max_columns', df.shape[1]):
#    print(df)