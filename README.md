### DISCLAIMER: This is a student in cybersecurity creating an app with crypto reliance. Please do not trust anything put out there yet. Thanks.

# PainlessPass
PainlessPass is a simple way to store your account credentials. Developed with security in mind, PainlessPass ensures that you, and only **_you_** can access your stored credentials. PainlessPass allows you to store and search through your credentials with ease. PainlessPass is open-source and dockerized, making it easy to run your own instance on your own hardware. 

## Explanation of Use
PainlessPass is currently in beta. It is a test of storing and decrypting passwords using known cryptographic libraries. The entire program revolves around each user having an encryption key that is encrypted using their password. This is to ensure that the only way a user's password entry is decrypted is by entering in their own login password following the same encryption algorithm that PainlessPass uses. At the time of writing, this unencrypted key is stored in volatile memory on the server utilizing sessions. It is possible that this key gets overwritten. The program is coded to reauthenticate a user whenever their unencrypted encryption key cannot be accessed. Throughout the code, this overarching encryption key (used for password entries) is referred to as a "GEK", or "General Encryption Key". 

The current flow of the program is to create an account, sign in, create folder and passwords, and then access password by clicking individual entries. The application code unencrypts passwords only when their individual entries are clicked. You then must click the "eye" icon to show the password. Javascript is required. 

## Installation
1. Copy the code to your local machine or server
2. Install Docker
3. Edit the app.env, db.env, and settings.py files in order to add necessary secrets and tune the app to your liking
4. Browse to your directory and launch the commands in getting started to install


## Getting Started
These are the commands for now. More to come later!
```bash
docker-compose build
docker-compose up
docker-compose run app python manage.py makemigrations
docker-compose run app python manage.py migrate
```
