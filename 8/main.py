import json
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def parse_selenium():
    site = 'https://jobs.aon.com'
    driver = webdriver.Chrome()

    max_page = 3
    result = []

    for page in range(1, max_page):
        driver.get(urljoin(site, f'jobs?page={page}'))

        jobs = driver.find_elements(By.CLASS_NAME, 'job-title-link')
        for job in jobs:
            link = job.get_attribute('href')
            title = job.find_element(By.TAG_NAME, 'span').text
            result.append({
                'link': link,
                'title': title
            })

    driver.quit()

    with open('jobs_selenium.json', 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == '__main__':
    parse_selenium()
