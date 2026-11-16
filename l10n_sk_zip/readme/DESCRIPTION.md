Loads the Slovak localities (obce) with their postal code and region, and fills in the
city and the region of Slovak addresses from the postal code.

- Ships the list of Slovak localities with their postal code, linked to the regions of Slovakia. The data
  comes from [GeoNames](https://www.geonames.org) (Creative Commons Attribution 4.0).
- Slovakia is set to *enforce cities*: the city of a Slovak address is chosen from the list.
- On the contact form, typing the postal code (PSČ) of a Slovak address sets the city and the
  region. A postal code shared by several localities sets only the region; the city name, when it matches
  one of them (without accents and case), picks the locality.
- The action *Slovakia: set city from ZIP* on contacts links the Slovak contacts to the city of their postal
  code and fills in the region.
- At install, the Slovak contacts are linked: directly on a small database, by the scheduled action
  *Slovakia: link contacts to the city of their ZIP* in batches on a large one (it deactivates itself when done).
- Every form that runs the postal code rules of the contact (for example the delivery details of an AWB)
  gets the region filled in, so the shipment can be sent to Slovakia without looking it up by hand.
