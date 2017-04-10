# -*- coding: utf-8 -*-

# !!! # Crawl responsibly by identifying yourself (and your website/e-mail) on the user-agent
USER_AGENT = 'TwitterScraper'

# settings for spiders
BOT_NAME = 'TwitterScraper'
LOG_LEVEL = 'INFO'
DOWNLOAD_HANDLERS = {'s3': None,} # from http://stackoverflow.com/a/31233576/2297751, TODO

SPIDER_MODULES = ['TwitterScraper.spiders']
NEWSPIDER_MODULE = 'TwitterScraper.spiders'
ITEM_PIPELINES = {
    'TwitterScraper.pipelines.SaveToFilePipeline':100,
    # 'TwitterScraper.pipelines.SaveToMongoPipeline':100, # replace `SaveToFilePipeline` with this to use MongoDB
}

# settings for where to save data on disk
SAVE_TWEET_PATH = './Data/tweet/'
SAVE_USER_PATH = './Data/user/'
