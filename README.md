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

- [https://www.openstreetmap.fr/donnees/](Open Street Map)
- [https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_API_by_Example](Open Street Map Wiki, how ot use API)
- [https://geodatamine.fr/](OSM data but aggregated)
- [https://publicapis.io/open-street-map-api](OSM data examples)
- [https://docs.stream.estate/api-reference/concepts](Property API, stream-estate) -> not free
- [https://navitia.io/fr/](Navitia to compute distance from a point to another by public transport)
- [https://apify.com/lexis-solutions/seloger-scraper/api](Apify solution for seloger.com) -> not free
- [https://nominatim.org/](Geo spatial data from OSM)
- [https://www.data.gouv.fr/datasets/demandes-de-valeurs-foncieres/](DVF to get every informations about a city)
- [https://www.octoparse.fr/blog/comment-le-scraping-dimmobilier-peut-ameliorer-votre-business](Octoparse solution, free-tier possible)

## Architecture (draft)

Using AWS:

- Images on S3
- Infos in DynamoDB -> Fast and scalable
- FastAPI back-end<-> DynamoDB on EC2 free tier
- Front-end EC2 (Python Dash) (maybe load balancer if open to everyone)
- Route 53 to get a fix IP
