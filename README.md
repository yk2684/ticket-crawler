# Ticket Site Crawler

Crawls [Stubhub](https://www.stubhub.com/) and [Seatgeek](https://seatgeek.com/) -- collects data on event and ticket information listed for the event. 

| Header | Description | Data Type |
|---|---|---|
| `currentPrice` | The current listed ticket price | number | 
| `listingId` | Listing Id | number/text | 
| `listingPrice` | TThe origina listed ticket price | number | 
| `quantity` | Number of tickets on sale | number | 
| `row` | Row number of the tickets | text | 
| `score` | Score value of the tickets | number | 
| `seatnumber` | Seat number  | number | 
| `sectionName` | Section Name | text | 
| `zoneName` | Zone Name | text |
| `eventId` | Event Id | text |
| `performance` | Performance date and time | datetime |
| `datePulled` | The date when the sites were scraped | datetime |
| `vendor` | Site name | text |

## Usage example

### Stubhub

Run `stubhub_scrape.py` as you normally would -- the output is a csv file. 

### Seatgeek

Run the scrapy spider `seatgeek_spider`

Example command: `scrapy crawl seatgeek_spider -o bandsvisit.csv -a showname=the-band-s-visit`

### Prerequisites

Scrapy
StubHub Developer Account (API)
