import datetime as dt
import pandas as pd
import requests as r
import urllib3
import time
import random

from bs4 import BeautifulSoup as bs4
import multiprocessing
r.packages.urllib3.disable_warnings(
    category=urllib3.exceptions.InsecureRequestWarning)
# <start editable> edit this dates to match what you did expect for
# format is d.m.yyyy
start_date = "20.03.2014"
end_date = "12.06.2020"
id = 11  # id obtained from request itself
# <end editable>
id = str(id)
start_date, end_date = [dt.datetime.strptime(i, "%d.%m.%Y").date() for i in [
    start_date, end_date]]
invalid_data = """<table id="data-table" class="display data-table" cellspacing="0" width="100%">
    <thead>
        <tr>
            <th>Дата заявления</th>
            <th>Ф.И.О заявителя</th>
            <th>Дата и номер решения о постановке в очередь</th>
            <th>Дата и номер решения о предоставлении земельного участка</th>
            <th>Статус заявления</th>
            <th>Номер в очереди</th>
        </tr>
    </thead>
    <tbody>
            </tbody>
</table>"""
headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="85", "\\\\Not;A\\"Brand";v="99"',
    'Accept': '*/*',
    'DNT': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4148.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://aiszem.krtech.ru',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://aiszem.krtech.ru/',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}

params = (
    ('r', '0.3236588850453519'),
)


def req(now):
    #print(f'Obtaining list of date {now.strftime("%d.%m.%Y")}')
    data = {
        'id': id,
        'date': now.strftime("%d.%m.%Y")
    }
    response = r.post('https://aiszem.krtech.ru/list',
                      headers=headers, params=params, data=data, verify=False)
    if response.text == invalid_data:
        return
    print(f"\nREPSONSE_CODE {response.status_code}")
    return response.text


def dots():
    print()
    c = 0
    while True:
        print("\r."*c, end="")
        c += 1 if c != 3 else -3


now = start_date
indexes = []
dataframes = []
try:
    print(f"Dates set: {start_date}>>{end_date}")
    for i in range((end_date-start_date).days):
        try:
            response = req(now)
        except:
            print("\nError! Waiting for 30secs")
            time.sleep(30)
            response = req(now)
        if response != None:
            print(f"Got valid response for {now.strftime('%d.%m.%Y')} date.")
#            print(response)
            indexes += [i.text for i in bs4(response,
                                            features="html.parser").findAll("td") if i.text[0].isdigit()]
            dataframes.append(pd.read_html(response)[
                              0].drop(columns="Дата заявления"))
    #        print(a)
#            print(indexes)
#            print(a)
#            print(pd.DataFrame(a.values, columns=a.columns, index=indexes))
    #        print([i.text for i in bs4(response, features="html.parser").findAll("td")])
    #        sec = random.randint(1, 5)
    #        print(f"Waiting for {sec} seconds.")
    #        time.sleep(sec)
        now += dt.timedelta(days=1)
        print(f"\r[{dt.datetime.now()}] {now.strftime('%d.%m.%Y')}", end="")
except:
    a = pd.concat(dataframes)
    s = pd.DataFrame(a.values, columns=a.columns, index=indexes)
    s.to_excel("out.xlsx")
    raise SystemExit()
s = pd.DataFrame(a.values, columns=a.columns, index=indexes)
s.to_excel("_".join(f"{dt.datetime.now()}_out.xlsx".split()))


# print(a.text)
