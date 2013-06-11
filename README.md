# Elucidata - A visual way of browsing through data repositories

This project was developed as part of [GovHack](http://govhack.org) 2013 by a team from [MakeHackVoid](http://www.makehackvoid.com) including Brenda Moon, Cameron Moon, Megan Byrne, Alistair D'Silva, Jessica Smith, Ra Inta, Max Bainrot and John Aslanides.

Our GovHack project page is [http://hackerspace.govhack.org/?q=groups/elucidata](http://hackerspace.govhack.org/?q=groups/elucidata)

The system consists of two major components, the backend which gathers the data and the frontend that allows users to explore it.

The frontend is a website which the end user accesses, it uses [Twitter Bootstrap](http://twitter.github.io/bootstrap/), [Google Maps API](https://developers.google.com/maps/), [Flask](http://flask.pocoo.org/), [Font Awesome](http://fortawesome.github.io/Font-Awesome/), [Google Web Fonts](http://www.google.com/fonts/), [jQuery](http://jquery.com/) and [D3.js](http://d3js.org).

The backend populates the data in the database by accessing the [CKAN api](http://docs.ckan.org/en/latest/api.html) interface on [data.gov.au](http://data.gov.au). The information is then stored in a [PostgreSQL](http://www.postgresql.org/) database.

It is intended that the backend will automatically check the repositories as needed to insure that the versioning information that is stored on our cache is of the most current date and time.

## Status

 - The current version only implements csv parsing. We intend to expand it to include all of the text and location based datafiles on data.gov.au.
 - checking for updates to datasets and updating their information has not been implemented

## Dependencies

In order to use our product you will need to install the following on your computer

 - Python
 - postgresql
 - postgresql-devel
 - postgresql-server
 - python modules (see pip_requirements.txt)
    - flask
    - sqlalchemy
    - pandas
    
## License

    Copyright 2013 Make, Hack, Void Inc

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.