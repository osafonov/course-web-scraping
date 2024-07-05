import requests
import re
import json
import sqlite3
from pprint import pprint


def get_vacancies():
    response = requests.get('https://www.lejobadequat.com/emplois')
    a_elements = re.findall('<a\shref="(.+)"\stitle(.|\n){1,1000}<h3\sclass="jobCard_title">(.+)</h3>', response.text)

    json_filename = '../6/vacancies.json'
    vacancies = [
        {'title': a_element[2], 'url': a_element[0]}
        for a_element in a_elements
    ]
    pprint(vacancies)
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, indent=4)

    sqlite_filename = '../6/vacancies.db'
    conn = sqlite3.connect(sqlite_filename)
    cursor = conn.cursor()

    sql = """
            create table if not exists vacancies (
                id integer primary key,
                title text,
                url text,
                unique (url) on conflict ignore
            )
        """
    cursor.execute(sql)

    for a_element in a_elements:
        cursor.execute("""
                insert into vacancies (title, url)
                values (?, ?)
            """, (a_element[2], a_element[0]))

    conn.commit()

    rows = cursor.execute('select * from vacancies').fetchall()
    print('\nData from DB:\n', rows)

    conn.close()


if __name__ == '__main__':
    get_vacancies()
