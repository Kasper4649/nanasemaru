# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy.pipelines.images import ImagesPipeline
from nanasemaru import settings


class NanasemaruPipeline(object):
    def process_item(self, item, spider):
        return item


class NonnoImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        super(NonnoImagesPipeline, self).file_path(request, response, info)
        datetime = request.item.get('article_datetime')
        title = request.item.get('article_title')

        # 按日期创建文件夹
        image_store_path = settings.IMAGES_STORE
        datetime_path = os.path.join(image_store_path, datetime)
        if not os.path.exists(datetime_path):
            os.mkdir(datetime_path)

        # 按文章名称创建文件夹
        title_path = os.path.join(datetime_path, title)
        if not os.path.exists(title_path):
            os.mkdir(title_path)

        image_name = request.url.split('/')[-1]
        image_path = os.path.join(title_path, image_name)
        return image_path

    def get_media_requests(self, item, info):
        requests = super(NonnoImagesPipeline, self).get_media_requests(item, info)
        for request in requests:
            request.item = item
        return requests
