# Airport service
Django REST project that simulates work of an airport. As a user, you can register, login, select a flight and create order with tickets for that flight. As an admin, you're able to create new entities, such as airport, airplane, crew, route, flight.

## Technologies
* Python
* Django
* DjangoORM
* Django REST
* Postgres
* JWT Authentication
* Swagger


## Installation
* Python3 and Docker must be already installed
* Create .env file using .env.sample with your environmental variables
* With Docker open, run command `docker-compose build`
* Then run `docker-compose up`

## Features
* Registrations for new users
* JWT authentication
* CRUD operations with all the models for admin users
* Ability to work with db through admin panel
* Admins are able to create new routes from one airport to another
* Users are allowed to view available fight and filter them by date or rote
* After finding needed flight, user can create an order
* Users are allowed to view only theirs orders/tickets
* API also validates, that only free seats can be taken
