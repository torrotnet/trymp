# Sanic & Nginx & mongo & docker-compose example

Using docker and docker-compose to orchestrate everything.

The app is based on the (great) blog-post for flask:
https://realpython.com/blog/python/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/

# How to run?
  - git clone the project
  - Create and start containers:
    `docker-compose up -d --build`
  
## Features:
  - /static/* files are served using the nginx.
  - Use the .env file to override or add config values (i override the logo):
    - Just add SANIC_ prefix before var name.
