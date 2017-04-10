import json
import logging
import re
import urllib
import urllib.parse

import scrapy
from scrapy.selector import Selector

from TwitterScraper.items import TweetItem, UserItem

logger = logging.getLogger(__name__)


class TweetScraper(scrapy.Spider):
    name = 'TwitterScraper'
    allowed_domains = ['twitter.com']

    def __init__(self, queries='', *args, **kwargs):
        super(TweetScraper, self).__init__(*args, **kwargs)
        self.queries = queries.split(',')
        self.reScrollCursor = re.compile(r'data-min-position="([^"]+?)"')
        self.reRefreshCursor = re.compile(r'data-refresh-cursor="([^"]+?)"')

    def start_requests(self):
        # generate request: https://twitter.com/search?q=[xxx] for each query
        for query in self.queries:
            url = 'https://twitter.com/search?q=%s' % urllib.parse.quote_plus(query)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # handle current page
        for item in self.parse_tweets_block(response.body):
            yield item

        # get next page
        tmp = self.reScrollCursor.search(response.body.decode())
        if tmp:
            query = urllib.parse.parse_qs(urllib.parse.urlparse(response.request.url).query)['q'][0]
            scroll_cursor = tmp.group(1)
            url = 'https://twitter.com/i/search/timeline?q=%s&' \
                  'include_available_features=1&include_entities=1&max_position=%s' % \
                  (urllib.parse.quote_plus(query), scroll_cursor)
            yield scrapy.Request(url, callback=self.parse_more_page)

            # TODO: # get refresh page
            # tmp = self.reRefreshCursor.search(response.body)
            # if tmp:
            #     query = urlparse.parse_qs(urlparse.urlparse(response.request.url).query)['q'][0]
            #     refresh_cursor=tmp.group(1)

    def parse_more_page(self, response):
        # inspect_response(response)
        # handle current page
        data = json.loads(response.body)
        for item in self.parse_tweets_block(data['items_html']):
            yield item

        # get next page
        query = urllib.parse.parse_qs(urllib.parse.urlparse(response.request.url).query)['q'][0]
        min_position = data['min_position']
        url = 'https://twitter.com/i/search/timeline?q=%s&' \
              'include_available_features=1&include_entities=1&max_position=%s' % \
              (urllib.parse.quote_plus(query), min_position)
        yield scrapy.Request(url, callback=self.parse_more_page)

    def parse_tweets_block(self, html_page):
        page = Selector(text=html_page)

        # for tweets with media
        items = page.xpath('//li[@data-item-type="tweet"]/ol[@role="presentation"]/li[@role="presentation"]/div')
        for item in self.parse_tweet_item(items):
            yield item

        # for text only tweets
        items = page.xpath('//li[@data-item-type="tweet"]/div')
        for item in self.parse_tweet_item(items):
            yield item

    def parse_tweet_item(self, items):
        for item in items:
            logger.debug("Show tweet:\n%s" % item.xpath('.').extract()[0])
            try:
                tweet_item = TweetItem()
                user_item = UserItem()

                tweet_id = item.xpath('.//@data-tweet-id').extract()
                if not tweet_id:
                    continue
                tweet_item['ID'] = tweet_id[0]
                # get text content
                tweet_item['text'] = '\n'.join(item.xpath('.//div[@class="content"]//p').xpath('.//.').extract())
                if tweet_item['text'] == '':
                    continue  # skip no <p> tweet

                # get meta data
                tweet_item['url'] = item.xpath('.//@data-permalink-path').extract()[0]
                tweet_item['datetime'] = \
                    item.xpath(
                        './/div[@class="content"]/div[@class="stream-item-header"]/small[@class="time"]/a/span/@data-time').extract()[
                        0]

                # get photo
                has_cards = item.xpath('.//@data-card-type').extract()
                if has_cards and has_cards[0] == 'photo':
                    tweet_item['has_image'] = True
                    tweet_item['images'] = item.xpath('.//*/div/@data-image-url').extract()
                elif has_cards:
                    logger.debug('Not handle "data-card-type":\n%s' % item.xpath('.').extract()[0])

                # get animated_gif
                has_cards = item.xpath('.//@data-card2-type').extract()
                if has_cards:
                    if has_cards[0] == 'animated_gif':
                        tweet_item['has_video'] = True
                        tweet_item['videos'] = item.xpath('.//*/source/@video-src').extract()
                    elif has_cards[0] == 'player':
                        tweet_item['has_media'] = True
                        tweet_item['medias'] = item.xpath('.//*/div/@data-card-url').extract()
                    elif has_cards[0] == 'summary_large_image':
                        tweet_item['has_media'] = True
                        tweet_item['medias'] = item.xpath('.//*/div/@data-card-url').extract()
                    elif has_cards[0] == 'amplify':
                        tweet_item['has_media'] = True
                        tweet_item['medias'] = item.xpath('.//*/div/@data-card-url').extract()
                    elif has_cards[0] == 'summary':
                        tweet_item['has_media'] = True
                        tweet_item['medias'] = item.xpath('.//*/div/@data-card-url').extract()
                    elif has_cards[0] == '__entity_video':
                        pass  # TODO
                        # tweetItem['has_media'] = True
                        # tweetItem['medias'] = item.xpath('.//*/div/@data-src').extract()
                    else:  # there are many other types of card2 !!!!
                        logger.debug('Not handle "data-card2-type":\n%s' % item.xpath('.').extract()[0])

                # get user info
                tweet_item['user_id'] = item.xpath('.//@data-user-id').extract()[0]
                user_item['ID'] = tweet_item['user_id']
                user_item['name'] = item.xpath('.//@data-name').extract()[0]
                user_item['screen_name'] = item.xpath('.//@data-screen-name').extract()[0]
                user_item['avatar'] = \
                    item.xpath('.//div[@class="content"]/div[@class="stream-item-header"]/a/img/@src').extract()[0]
                yield tweet_item
                yield user_item
            except:
                logger.error("Error tweet:\n%s" % item.xpath('.').extract()[0])
                #raise

    def extract_one(self, selector, xpath, default=None):
        extracted = selector.xpath(xpath).extract()
        if extracted:
            return extracted[0]
        return default
