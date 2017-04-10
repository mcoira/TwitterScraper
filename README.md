# Introduction #
`TwitterScraper` can get tweets from [Twitter Search](https://twitter.com/search-home).
It is built on [Scrapy](http://scrapy.org/) without using [Twitter's APIs](https://dev.twitter.com/rest/public).
The crawled data is not as *clean* as the one obtained by the APIs, but the benefits are you can get rid of the API's rate limits and restrictions. Ideally, you can get all the data from Twitter Search.

**WARNING:** please be polite and follow the [crawler's politeness policy](https://en.wikipedia.org/wiki/Web_crawler#Politeness_policy).
 

# Installation #
It requires [Scrapy](http://scrapy.org/). Setting up:

    $ git clone https://github.com/mcoira/TwitterScraper.git
    $ cd TwitterScraper/
    $ pip install -r requirements.txt  #add '--user' if you are not root
	$ scrapy list
	$ #If the output is 'TwitterScraper', then you are ready to go.

# Usage #
1. Change the `USER_AGENT` in `TwitterScraper/settings.py` to identify who you are
	
		USER_AGENT = 'your website/e-mail'

2. In the root folder of this project, run command like: 

		scrapy crawl TwitterScraper -a queries=foo,#bar

	where `queries` is a list of keywords seperated by comma (`,`). The queries can be any thing (keyword, hashtag, etc.) you want to search in [Twitter Search](https://twitter.com/search-home). `TwitterScraper` will crawl the search results of each query and save the tweet content and user information. You can also use the following operators in each query (from [Twitter Search](https://twitter.com/search-home)):
	
	| Operator | Finds tweets... |
	| --- | --- |
	| twitter search | containing both "twitter" and "search". This is the default operator. |
	| **"**happy hour**"** | containing the exact phrase "happy hour". |
	| love **OR** hate | containing either "love" or "hate" (or both). |
	| beer **-**root | containing "beer" but not "root". |
	| **#**haiku | containing the hashtag "haiku". |
	| **from:**alexiskold | sent from person "alexiskold". |
	| **to:**techcrunch | sent to person "techcrunch". |
	| **@**mashable | referencing person "mashable". |
	| "happy hour" **near:**"san francisco" | containing the exact phrase "happy hour" and sent near "san francisco". |
	| **near:**NYC **within:**15mi | sent within 15 miles of "NYC". |
	| superhero **since:**2010-12-27 | containing "superhero" and sent since date "2010-12-27" (year-month-day). |
	| ftw **until:**2010-12-27 | containing "ftw" and sent up to date "2010-12-27". |
	| movie -scary **:)** | containing "movie", but not "scary", and with a positive attitude. |
	| flight **:(** | containing "flight" and with a negative attitude. |
	| traffic **?** | containing "traffic" and asking a question. |
	| hilarious **filter:links** | containing "hilarious" and linking to URLs. |
	| news **source:twitterfeed** | containing "news" and entered via TwitterFeed |

3. The tweets will be saved to disk in `./Data/tweet/` in default settings and `./Data/user/` is for user data. The file format is JSON. Change the `SAVE_TWEET_PATH` and `SAVE_USER_PATH` in `TwitterScraper/settings.py` if you want another location.

# License #
TwitterScraper is released under the [GNU GENERAL PUBLIC LICENSE, Version 2](https://github.com/mcoira/TwitterScraper/blob/master/LICENSE)
