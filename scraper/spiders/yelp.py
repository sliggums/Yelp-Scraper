from scrapy import Request
from scrapy.spiders import Spider
from ..items import RestaurantItem

# BASE_LINK = "https://www.yelp.com/biz"
# SEARCH_LINK = "https://www.yelp.com/search?find_desc=&find_loc=San+Ramon%2C+CA&ns=1"
# SEARCH_RESTAURANT_XPATH = '//div/h4/span/a/@href'

SEARCH_LINK = "https://www.yelp.com/user_details_reviews_self?userid=BUeueHeX3mzlyEBEEK9quQ&review_filter=category&category_filter=restaurants"

NEXT_BUTTON_XPATH = "//a[@class='u-decoration-none next pagination-links_anchor']/@href"
REVIEW_XPATH = "//div[@class='review']/@data-review-id"
TEXT_XPATH = "//div[@data-review-id='%s']/div/div/p/text()"
PHOTO_XPATH = "//div[@data-review-id='%s']/div/div/ul/li/div/img/@srcset"
RESTAURANT_XPATH = "//div[@data-review-id='%s']/div/div/div/div/a/span/text()"

class QuotesSpider(Spider):
  name = "yelp"
  allowed_domains = ['yelp.com']

  def start_requests(self):
    return [Request(url=SEARCH_LINK, callback=self.parse)]

  def parse(self, response):
    for review_id in response.xpath(REVIEW_XPATH).extract():
      restaurant_name = response.xpath(RESTAURANT_XPATH % review_id).extract_first()
      text = response.xpath(TEXT_XPATH % review_id).extract_first()
      photo_list = [ "/".join(photo.split(" ")[0].split("/")[:-1]) + "/1000s.jpg" for photo in response.xpath(PHOTO_XPATH % review_id).extract() ]
      item = RestaurantItem()
      item['text'] = text
      item['name'] = restaurant_name
      item['image_urls'] = photo_list
      yield item
    next_page = response.xpath(NEXT_BUTTON_XPATH).extract_first()
    # if next_page:
    #   yield Request(url=next_page, callback=self.parse)






