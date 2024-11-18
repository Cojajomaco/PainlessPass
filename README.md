### DISCLAIMER: This is a student in cybersecurity creating an app with crypto reliance. Please do not trust anything put out there yet. Thanks.

# PainlessPass
PainlessPass is a simple way to store your account credentials. Developed with security in mind, PainlessPass ensures that you, and only **_you_** can access your stored credentials. PainlessPass allows you to store and search through your credentials with ease. PainlessPass is open-source and dockerized, making it easy to run your own instance on your own hardware. 

## Installation
I'll figure this out soon, I guess. The goal is to pretty much have the app running with a few local commands to get Docker to do its thing. Currently, it is this:
1. Copy the code to your local machine or server
2. Install Docker
3. Browse to your directory and launch the command in getting started to install

More steps will be added later on to define a secure initial config as right now the app uses insecure default hard-coded creds. 

## Getting Started
These are the commands for now. More to come later!
```bash
docker-compose build
docker-compose up
docker-compose run app python manage.py makemigrations
docker-compose run app python manage.py migrate
```

## Uh-oh
I am already experiencing scope creep. It turns out, implementing crypto that is consistent and secure is really hard to do, even with libraries dedicated to crypto to assist me. 
The minimum viable product that I am aiming for is a password manager that encrypts and decrypts data with a semi-usable UI and API calls that allow you to generate a password. 
