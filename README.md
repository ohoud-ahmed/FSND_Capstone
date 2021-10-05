# FSND_Capstone

Udacity Full-Stack Web Developer Nanodegree Program Capstone Project:

overview: The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

In this Capstone project, I use all of the concepts and the skills taught in the courses to build an API from start to finish and host it. These include data modelling , API design, authentication and authorization and cloud deployment.

Key Dependencies:

    Flask :is a web framework use to create our api server.
    PostgreSQL is a powerful, open source object-relational database system
    SQLAlchemy :is the most popular open-source library for working with relational databases from Python.
    Auth0 : is an easy to implement, adaptable authentication and authorization platform.
    Heroku: is the cloud platform use for deployment

Running the server

$ export FLASK_APP=app $ export FLASK_DEBUG=True $ export FLASK_ENVIRONMENT=debug $ flask run

Endpoints
GET /actors * gets the list of all the actors * requires get:actors permission

POST /actors * creates a new actor * requires post:actor permission

    Request Body
        name: string
        age: string
        gender:string

PATCH /actors/{actor_id} * updates the info for an actor * requires patch:actor permission

    Request Body
        name: string
        age: string
        gender:string

DELETE /actors/{actor_id} * deletes the actor * requires delete:actor permission

GET /movies * gets the list of all the movies * requires get:movies permission

GET /movies/{movie_id} * gets the complete info for a movie * requires get:movies-info permission

POST /movies * creates a new movie * requires post:movie permission

    Request Body
        title: string
        release_date: string

PATCH /movie/{movie_id} * updates the info for a movie * requires patch:movie permission

    Request Body
        title: string
        release_date: string

DELETE /movies/{movie_id} * deletes the movie * requires delete:movie permission Roles:

The project has three different types of roles:

    Casting Assistant
        can only view the list of actors and movies .
    Casting Director
        can perform all the actions that casting assistant can
        can also create an actor and delete it
        Can also update actors and movies information
    Executive Producer
        can perform all the actions that casting assistant can
        can also create an movie and delete it

Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:movies`
   - `post:movies`
   - `patch:movies`
   - `delete:movies`
   - `get:actors`
   - `post:actors`
   - `patch:actors`
   - `delete:actors`
6. Create new roles for:
   - Casting Assistant
     - `get:movies`
     - `get:actors`
   - Casting Director
     - `get:movies`
     - `patch:movies`
     - `get:actors`
     - `post:actors`
     - `patch:actors`
     - `delete:actors`
   - Executive Producer
     - `get:movies`
     - `post:movies`
     - `patch:movies`
     - `delete:movies`
     - `get:actors`
     - `post:actors`
     - `patch:actors`
     - `delete:actors`
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 3 users - assign the Casting Assistant role to one ,Casting Director role to one and Executive Producer role to the other.

Test the application by URL:
https://capstonefp.herokuapp.com/

Testing: $ python test_app.py
 
