## Setup & dependencies

- Python 3.9
- Django 3.1.2

The following steps will walk you thru installation on a Mac. Linux should be similar.
It's also possible to develop on a Windows machine, but I have not documented the steps.
If you've developed django apps on Windows, you should have little problem getting
up and running.


### Create Database
For mysql
```
CREATE DATABASE capital_finishes_erp;
CREATE USER 'capital_finishes'@'localhost' IDENTIFIED BY 'capital_finishes';
GRANT ALL PRIVILEGES ON *.* TO 'capital_finishes'@'localhost';
```

### Setup
Run
```
make virtualenv
make install
```

## Run server locally
Run
```
make collectstatic
make migrate
make server
```

## Before committing
Run
```
make local-ci
```
