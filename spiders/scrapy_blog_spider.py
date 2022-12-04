import scrapy
from ten_min_scrapy.items import Post
import re


class ScrapyBlogSpiderSpider(scrapy.Spider):
    name = 'scrapy_blog_spider'
    allowed_domains = ['zyte.com']
    start_urls = ['https://www.zyte.com/blog/']

    def parse(self, response):
        for post in response.css('#_posts_grid-98-2233 > div.oxy-posts > div.oxy-post'):
            print(
                response.css('#_posts_grid-98-2233 > div.oxy-easy-posts-pages > a.next.page-numbers::attr(href)').get())
            yield Post(
                url=post.css(
                    'a::attr(href)').getall()[1],
                title=post.css(
                    'div.oxy-post-wrap > div > a::text').get(),
                date=re.sub(r"[^a-zA-Z0-9]", "", post.css(
                    'a > div.oxy-post-image-date-overlay::text').get()
                ))
        older_post_link = response.css(
            '#_posts_grid-98-2233 > div.oxy-easy-posts-pages > a.next.page-numbers::attr(href)').get()
        if older_post_link is None:
            # リンクが取得できなかった場合は最後のページなので処理を終了
            print("------------------------------------------------nopagesleft")
            return

        # URLが相対パスだった場合に絶対パスに変換する
        older_post_link = response.urljoin(older_post_link)
        print(older_post_link)
        # 次のページをのリクエストを実行する
        yield scrapy.http.Request(url=older_post_link, callback=self.parse)
