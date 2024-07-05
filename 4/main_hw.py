import requests
import re


def get_vacancies():
    response = requests.get('https://www.lejobadequat.com/emplois')
    h3_elements = re.findall('(<h3 class="jobCard_title">)(.+)(</h3>)', response.text)

    job_titles = []
    for h3_element in h3_elements:
        job_titles.append(h3_element[1])

    print("Job Titles: ", job_titles)


if __name__ == '__main__':
    get_vacancies()
