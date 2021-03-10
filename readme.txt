Hi,
I have made this project with a few sample data for latitude and longitude of the destination.
And the output should come in a txt file.

First of all download the django project from git, I have made the project on docker so kindly hit the command after
entering directory of the desired folder:

-docker-compose up -d --build

-docker-compose exec orderapp python manage.py makemigrations

-docker-compose exec orderapp python manage.py migrate

now coming to browser just hit the url

-http://localhost:8000/place_order/


This url will create a dummy delivery_user with a product, central latitude, longitude position of the delivery Guy
as well creates 5 orders randomly.
Next Deliver boy will go to deliver orders next day.
All the result of delivery boy travelling to deliver orders will be saved on 'output_file.txt'.
Everytime a user goes out for delivery we will assign him unique delivery id that will help us to track a record of the
delivery sessions.

for getting the different urls of each delivery session hit the below url:

-http://localhost:8000/get_unique_delivery_key/

here you will get links for different delivery sessions you can just copy paste that links to get the details of that
delivery session in a file named as unique_delivery_file.txt.


Hope you like my work and update me for the same.
Thank you...

