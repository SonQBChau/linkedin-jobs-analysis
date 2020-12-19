import unicodedata
import typing
import time
import scrapy

# https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python#11566398


def normalize_and_strip(s):
    return unicodedata.normalize("NFKD", s).strip()


class LinkedInJobItem(scrapy.Item):
    jobid = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    entities = scrapy.Field()


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    allowed_domains = ['linkedin.com']

    job_titles = ['data scientist', 'data engineer',
                  'mobile application developer', 'web developer', 'machine learning engineer']
    # [city], state, country
    locations = ['california, united states',
                 'new york, united states', 'texas, united states']

    # scrapy worries about url formatting so we don't have to
    job_search_base = 'https://linkedin.com/jobs/search?keywords={0!s}&location={1!s}'
    job_view_base = 'https://linkedin.com/jobs/view/{0!s}'

    jobs_scraped = 0

    def start_requests(self):
        for t in self.job_titles:
            for l in self.locations:
                yield scrapy.Request(url=self.job_search_base.format(t, l), callback=self.parse)
                time.sleep(1800)  # 1 search per half hour, trying to be polite

    def parse(self, response):
        for jobid in response.css("[data-id]::attr(data-id)").getall():
            # command line argument numjobs, which by default is
            # set as a member variable on the spider
            # https://docs.scrapy.org/en/latest/topics/spiders.html#spider-arguments
            if hasattr(self, 'numjobs'):
                if self.jobs_scraped >= int(self.numjobs):
                    break
            yield scrapy.Request(url=self.job_view_base.format(jobid), callback=self.parse_job_post)
            self.jobs_scraped += 1

    def parse_job_post(self, response):

        jobid = response.request.url.split('/')[-1]
        company, location = response.css(
            '.topcard__flavor').xpath('./descendant-or-self::*/text()').getall()
        title = response.css('.topcard__title').xpath('./text()').get()

        desc_strings = [
            normalize_and_strip(s) for s in
            # https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-relative-xpaths
            # https://stackoverflow.com/questions/10413649/xpath-to-get-all-the-childrens-text#10416604
            # .show-more-less-html__markup is the css class of the immediate parent element of the full job description
            response.css(
                ".show-more-less-html__markup").xpath("./descendant-or-self::*/text()").getall()
            if normalize_and_strip(s)
        ]

        description = '\n\n'.join(desc_strings)

        return LinkedInJobItem({
            'jobid': jobid,
            'title': title,
            'company': company,
            'location': location,
            'description': description,
            'entities': []  # entities will be filled in by the next stage in the item pipeline
        })
