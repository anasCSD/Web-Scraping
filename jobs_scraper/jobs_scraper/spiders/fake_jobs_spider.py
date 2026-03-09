import scrapy

class FakeJobsSpider(scrapy.Spider):
    name = "fake_jobs"
    start_urls = ["https://realpython.github.io/fake-jobs/"]

    def parse(self, response):
        # Scrape job cards on current page
        for job in response.css("div.card-content"):
            title = job.css("h2.title.is-5::text").get()
            company = job.css("h3.subtitle.is-6.company::text").get()
            location = job.css("p.location::text").get()
            deadline = job.css("time::attr(datetime)").get()
            apply_links = job.css("footer.card-footer a.card-footer-item::attr(href)").getall()

            if title:
                yield {
                    "title": title.strip(),
                    "company": company.strip() if company else "",
                    "location": location.strip() if location else "",
                    "deadline": deadline.strip() if deadline else "N/A",
                    "salary": "Not Specified",
                    "apply_link": apply_links[1] if len(apply_links) > 1 else ""
                }

        # Pagination: follow "Next" link
        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)