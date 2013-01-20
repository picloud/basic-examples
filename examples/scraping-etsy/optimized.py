import cloud
import urllib2
from BeautifulSoup import BeautifulSoup

# the portion of the url that is shared by all etsy's pages
# we're scraping. {page} should be replaced by a number.
base_url = 'http://www.etsy.com/browse/art/painting/{page}'

def scrape_etsy_page(page):
    
    # scrape page
    soup = BeautifulSoup(urllib2.urlopen(base_url.format(page=page)).read())
    
    # get html tags that contain prices
    text_prices = [row.getText() for row in soup('span', {'class': 'listing-price'})]
    
    # convert all prices from strings to numbers (remove $ and commas)
    prices = [float(text_price[1:].replace(',', '')) for text_price in text_prices]
    
    return prices

def batch_scrape(pages):
    return [scrape_etsy_page(page) for page in pages]

if __name__ == '__main__':    

    pages_to_scrape = 50

    # number of pages each job should scrape
    chunksize = 3 

    # list of ranges of page each should should scrape
    page_ranges = [range(i, i+chunksize) for i in range(1,50, chunksize)]

    # the cost of all goods summed together
    total_cost = 0.0
    
    # the number of products scraped
    num_products = 0
   
    # offload all at once
    jids = cloud.map(batch_scrape, page_ranges)
    for batch_prices in cloud.result(jids):
        for prices in batch_prices:
            # sum costs and increment product count
            total_cost += sum(prices, 0.0)
            num_products += len(prices)
        
    print 'Found %s products costing on average %s each' \
          % (num_products, total_cost/num_products)
