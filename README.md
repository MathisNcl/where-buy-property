# where-buy-property

Web application that helps you choose and find the home that best meets your expectations.

## Target features

- All current online listings in France with images and information -> need to be scrapped
- Satellite images of the property
- Distance to amenities: schools, supermarkets, bakeries
- Distance to a reference city by public transport (Paris)
- Comparison of the price per square meter of the listing vs. the city or surrounding area
- Distance to a reference city (for vacation homes)
- Internet connection

## Resources

- [Open Street Map](https://www.openstreetmap.fr/donnees/)
- [Open Street Map Wiki, how ot use API](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_API_by_Example)
- [OSM data but aggregated](https://geodatamine.fr/)
- [OSM data examples](https://publicapis.io/open-street-map-api)
- [Property API, stream-estate](https://docs.stream.estate/api-reference/concepts) -> not free
- [Navitia to compute distance from a point to another by public transport](https://navitia.io/fr/)
- [Apify solution for seloger.com](https://apify.com/lexis-solutions/seloger-scraper/api) -> not free
- [Geo spatial data from OSM](https://nominatim.org/)
- [DVF to get every informations about a city](https://www.data.gouv.fr/datasets/demandes-de-valeurs-foncieres/)
- [Octoparse solution, free-tier possible](https://www.octoparse.fr/blog/comment-le-scraping-dimmobilier-peut-ameliorer-votre-business)

## Architecture (draft)

Using AWS:

- Images on S3
- Infos in DynamoDB -> Fast and scalable
- FastAPI back-end<-> DynamoDB on EC2 free tier
- Front-end EC2 (Python Dash) (maybe load balancer if open to everyone)
- Route 53 to get a fix IP

## Note

Seloger.com uses hash for location in url so can't use with requests. Maybe we can try using RPA solution:

- [Selenium](https://selenium-python.readthedocs.io/)
- [Playwright](https://playwright.dev/python/docs/intro)

Or a AI boostbsolution like [Browse AI](https://www.browse.ai/)

## TODO

- [] Add pre-commit
