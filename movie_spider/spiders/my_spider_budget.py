import scrapy

class MySpiderBudgetSpider(scrapy.Spider):
    name = "my_spider_budget"
    allowed_domains = ["www.the-numbers.com"]
    # Avoid getting blocked by the browser
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'FEEDS': {
            'movie_budgets.csv': {
                'format': 'csv',
                'encoding': 'utf-8',
                'store_empty': False,
                'fields': None,
            },
        },
        'DOWNLOAD_DELAY': 1,
    }
    start_urls = ["https://www.the-numbers.com/movie/budgets/all"]

    def parse(self, response):
        # full XPath to get table rows
        rows = response.xpath('//div[@id="page_filling_chart"]//table//tr[position() > 1]')
    
        for row in rows:
            # find and get the variables
            release_date = row.xpath('./td[2]/a/text()').get()
            movie_name = row.xpath('./td[3]/b/a/text()').get()
            detail_link = row.xpath('./td[3]/b/a/@href').get()  # Link to go into the movie main page and get the rest of the variables
            production_budget = row.xpath('./td[4]/text()').get()
            domestic_gross = row.xpath('./td[5]/text()').get()
            worldwide_gross = row.xpath('./td[6]/text()').get()

            # Follow the detail link to scrape additional data if available
            if detail_link:
                yield response.follow(
                    detail_link,
                    callback=self.parse_movie_details,
                    meta={
                        "release_date": release_date,
                        "movie_name": movie_name,
                        "production_budget": production_budget,
                        "domestic_gross": domestic_gross,
                        "worldwide_gross": worldwide_gross,
                    },
                )

        # Follow pagination links because not all of the movies are shown in the same page (only 100)
        next_page = response.css("div.pagination a.active + a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_movie_details(self, response):
        # Retrieve metadata passed from the previous page
        release_date = response.meta["release_date"]
        movie_name = response.css("h1::text").get()  # Movie Name from detail page because if the name didn't fit in the main table we found ...
        production_budget = response.meta["production_budget"]
        domestic_gross = response.meta["domestic_gross"]
        worldwide_gross = response.meta["worldwide_gross"]

        # Used css instead of xpath because we had it from the first dataset
        # In case the release date was not in the table we look for it in the main page
        if not release_date:
            release_date = response.css("tr:contains('Domestic Releases:') td::text").get()
        if not release_date:
            release_date = response.css("tr:contains('International Releases:') td::text").get()
        
        # Distributor next to the relesea data as a link
        distributor = response.css("tr:contains('Domestic Releases:') td a::text").get()
        # If there is not domestic releases, fall back to international releases
        if not distributor:
            distributor = response.css("tr:contains('International Releases:') td a::text").get()

        # Extract other details
        running_time = response.css("tr:contains('Running Time:') td::text").get()
        mpaa = response.css("tr:contains('MPAA\u00A0Rating:') td a::text").get() # If &nbsp in the HTML we have to write \u00A0 (Non-breaking space)
        genre = response.css("tr:contains('Genre:') td a::text").getall()
        franchise = response.css("tr:contains('Franchise:') td a::text").get()
        if not franchise:
            franchise = None
        creative_type = response.css("tr:contains('Creative\u00A0Type:') td a::text").getall()
        language = response.css("tr:contains('Languages:') td a::text").getall()
        production_countries = response.css("tr:contains('Production Countries:') td a::text").getall()  # Get all not only the first one
        international_box_office = response.css("td:contains('International Box Office') + td.data.sum::text").get()

        # Yield the combined data
        yield {
            "movie_name": movie_name,
            "release_date": release_date,
            "franchise": franchise,
            "running_time": running_time,
            "genre": genre,
            "creative_type": creative_type,
            "language": language,
            "production_countries": production_countries,
            "distributor": distributor,
            "mpaa": mpaa,
            "worldwide_gross": worldwide_gross,
            "production_budget": production_budget,
            "domestic_gross": domestic_gross,
            "international_box_office": international_box_office,
        }
