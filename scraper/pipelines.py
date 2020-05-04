# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import random
import os

class UpdatedImagesPipeLine(ImagesPipeline):
  def get_media_requests(self, item, info):
    return [Request(x, meta={'restaurant_name': item['name']})
    	for x in item.get('image_urls', [])]

  def get_images(self, response, request, info):
    for path, image, buf, in super(UpdatedImagesPipeLine, self).get_images(response, request, info):
      path = self.change_filename(path, response)
      print(path)
      yield path, image, buf

  def change_filename(self, key, response):
    return '%s/%d.jpg' % (response.meta['restaurant_name'], random.getrandbits(128))


class WriteTextPipeline:
	def process_item(self, item, spider):
		path = os.environ['FILE_PATH']
		file_name = item['name']
		with open('{}{}{}'.format(path, file_name, '/review.txt'), 'w') as f:
			f.write(item['text'])


