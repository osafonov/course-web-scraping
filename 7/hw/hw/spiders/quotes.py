import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    max_count_follow = 1

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse(self, response):
        rows = response.css('.quote')
        for row in rows:
            text_selector = '.text::text'
            text = row.css(text_selector).get()
            author_selector = '.author::text'
            author = row.css(author_selector).get()

            yield {
                'text': text,
                'author': author
            }

        next_btn = response.css('.next a').attrib['href']
        if next_btn and self.max_count_follow:
            self.max_count_follow -= 1
            yield response.follow(next_btn, callback=self.parse)
