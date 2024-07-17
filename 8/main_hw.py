import json
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By


def parse_selenium():
    site = 'https://jobs.marksandspencer.com/job-search'
    driver = webdriver.Chrome()

    max_page = 2
    result = []

    for page in range(1, max_page + 1):
        driver.get(urljoin(site, f'?page={page}'))

        jobs = driver.find_elements(By.CLASS_NAME, 'ais-Hits-item')
        for job in jobs:
            title = job.find_element(By.TAG_NAME, 'h3').text
            url = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
            result.append({
                'title': title,
                'url': url
            })

    driver.quit()

    with open('jobs_selenium_hw.json', 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == '__main__':
    parse_selenium()
