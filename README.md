# SegRed-Practica3
Easy and secure API Restful for json storage made with Flask

Authors:
  - Francisco Jesús Díaz Pellejero
  - Miguel de las Heras Fuentes


# Project files
- `app_module` custom module containing methods and exceptions used by the main application
- `database` is the root directory for storing all json files
- `domain.crt` is the self signed certificate used by the user. When using curl, the parameter --cacert domain.crt is necessary to resolve the domain in https 
- `domain.key` is the encrypted private key used to sign the certificate
- `requirements.txt` has all the modules that are necessary for this app
- `reset` deletes all files and all users from the shadow.txt file
- `run_app` is the main entry point of the application
- `shadow.txt` stores users and passwords with the same format as shadow files in linux systems
- `test_cases` runs all the test cases made with curl


# Requirements
Flask-restful and pyopnessl are required to run the app. Both can be installed with pip and the requirements.txt file:
  1. pip install -r requirements

To resolve 127.0.0.1 to the specified domain name in this assignement it is necessary to add 'myserver.local' to localhost in the /etc/hosts file
The first line of that file should be looking like this:
  `127.0.0.1	localhost myserver.local`


# Run the application
To run the application:
  1. ./run_app
  2. Introduce `1234` as the passphrase for the private key 2 times
The introduction of the `1234` passphrase will be mandatory everytime the application is executed


# Run test cases
Some test cases done in curl, regarding common uses and errors have been added to this assignement. To run this file:
  1. ./test_cases

The output should be all the commands used with curl and the response of the server. The main application should be running first

When we execute the test cases the reset file is executed first to delete all media and all users


# User available space
Currently there is not a limit to the amount of files that a single client can store. The only limit being the space available in the server


# User available number of request
Currently there is not a limit to the number of request an user can make in a period of time
