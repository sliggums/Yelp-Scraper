# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import os

class UpdatedImagesPipeLine(ImagesPipeline):
  def get_media_requests(self, item, info):
    return [Request(x, meta={'image_name': item['name']})
    	for x in item.get('image_urls', [])]

  def get_images(self, response, request, info):
    for path, image, buf, in super(UpdatedImagesPipeLine, self).get_images(response, request, info):
      path = self.change_filename(path, response)
      yield path, image, buf

  def change_filename(self, key, response):
    return '%s/image.jpg' % response.meta['image_name']


class WriteTextPipeline:
	def process_item(self, item, spider):
		path = os.environ['FILE_PATH']
		file_name = item['name']
		with open('{}{}{}'.format(path, file_name, '/review.txt'), 'w') as f:
			f.write(item['text'])


