# -*- coding: utf-8 -*-
import json
import logging
import os

from scrapy.conf import settings

from TwitterScraper.items import TweetItem, UserItem
from TwitterScraper.utils import mkdirs

logger = logging.getLogger(__name__)


class SaveToFilePipeline(object):
    """ pipeline that save data to disk """
    def __init__(self):
        self.saveTweetPath = settings['SAVE_TWEET_PATH']
        self.saveUserPath = settings['SAVE_USER_PATH']
        mkdirs(self.saveTweetPath)  # ensure the path exists
        mkdirs(self.saveUserPath)

    def process_item(self, item, spider):
        if isinstance(item, TweetItem):
            save_path = os.path.join(self.saveTweetPath, item['ID'])
            if os.path.isfile(save_path):
                pass  # simply skip existing items
                # or you can rewrite the file, if you don't want to skip:
                # self.save_to_file(item,savePath)
                # logger.info("Update tweet:%s"%dbItem['url'])
            else:
                self.save_to_file(item, save_path)
                logger.info("Add tweet:%s" % item['url'])

        elif isinstance(item, UserItem):
            save_path = os.path.join(self.saveUserPath, item['ID'])
            if os.path.isfile(save_path):
                pass  # simply skip existing items
                # or you can rewrite the file, if you don't want to skip:
                # self.save_to_file(item,savePath)
                # logger.info("Update user:%s"%dbItem['screen_name'])
            else:
                self.save_to_file(item, save_path)
                logger.info("Add user:%s" % item['screen_name'])

        else:
            logger.info("Item type is not recognised! type = %s" % type(item))

    def save_to_file(self, item, fname):
        """
        Write items into the file.
        Args:
            item: a dict like object
            fname: where to save

        Returns: nothing
        """
        with open(fname, 'w') as f:
            json.dump(dict(item), f)
