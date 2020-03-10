## Intro

This project gives me an introduction to technologies such as Docker, Flask and a postgres database with the extension of postgis to be able to access and visualize geographic data. 
In it, a series of enpoints are created for serving data stored in a postgres database with postgis using flask and python.
To start working on it, you can clone the repository locally and follow the steps below.

```
git clone https://github.com/PedroDDiez/flask-postgis-test.git <project-name>
```

## Requirements

I've created a Dockerfile and a docker-compose.yml to make the app run easily, so it is neccesary to have docker and docker-compose installed in your machine, if you don't have it installed, you can have more information here on how to do it:
 - Docker: https://docs.docker.com/install/
 - Docker-compose: https://docs.docker.com/compose/install/

The application runs in the port 80, so it has to be free to be able to run it

## Quick Start

Build the images if the images do not exist and start the containers:
```sh
cd /location/of/the/app
docker-compose up
```

The first time you run the app the database is empty, to populate it run this command in a new terminal while the containers are running:

```sh
cd /location/of/the/app
docker-compose exec web bash -c "python feed.py"
```

After this, the application should be up and running, so go to your web-browser and open the http://127.0.0.1/ url there you will see the endpoints I've created

## Considerations

There are some aspects I to take into account when running this app:
I'm not familiar with geographical data, and postgis, so I couldn't make work some of the postgis funcions. Also I think the srid should be used as parameter and do conversions when needed, but I haven't implemented it. I've used 4326 for the results.
The results aimed to be used in charts are formated to be easily used with Highcharts library.
The results aimed to be used in maps are formated to be easily used with Leaflet library.
For this example, I'm returning all the data without filtering it by date, but also parameters for date range should be added.
 

## Links

1. Flask boilerplate: https://github.com/tiangolo/uwsgi-nginx-flask-docker
2. Docker Postgis: https://github.com/kartoza/docker-postgis
3. Flask: https://palletsprojects.com/p/flask/
4. Postgis: https://postgis.net/docs/manual-3.0/
5. Leaflet: https://leafletjs.com/
6. Highcharts: https://api.highcharts.com/highcharts/