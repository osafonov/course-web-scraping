import re

text = "March 12, 2024"
text_emails = "Ось кілька електронних адрес для пошуку:john.doe@example.com, jane_doe123@domain.org, support@service.net, info@company.co.uk та contact.us@my-website.com Трішки складніший формат електронних адресів: weird.address+spam@gmail.com, \"quotes.included@funny.domain\" та this.one.with.periods@weird.co.in"
text_dates = "Почнімо з дат: 01/02/2021, 12-25-2020, 2021.03.15, 2022/04/30, 2023.06.20 та 2021.07.04 Також ви можете спробувати знайти дати зі словами: March 14, 2022, and December 25, 2020 "






def parse_emails():
    pattern = r'[\w\-\.\+"]{1,64}@[a-zA-Z0-9\-\."]+\.[a-zA-Z"]{2,}'
    emails = re.findall(pattern, text_emails)
    print(emails)

def parse_dates():
    pattern1 = r'(\d{2})(\/|-)(\d{1,2})(\/|-)(\d{4})' #01/02/2021, 12-25-2020
    pattern2 = r'(\d{4})(\/|\s|\.)(\d{1,2})(\/|\s|\.)(\d{2})' #2021.03.15, 2022/04/30, 2023.06.20 та 2021.07.04
    pattern3 = r'\w{3,9}\s\d{1,2},\s\d{4}' #March 14, 2022, and December 25, 2020
    dates1 = re.findall(pattern1, text_dates)
    dates2 = re.findall(pattern2, text_dates)
    dates3 = re.findall(pattern3, text_dates)
    print(dates1)
    print(dates2)
    print(dates3)

# //input[@id='text-input-what']
# //input[@id='text-input-where']
# //*[@id='jobsearch']//button

if __name__ == '__main__':
    parse_emails()
    parse_dates()