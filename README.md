# distributed-ethnography

A battery included approach to running small surveys using a approach based in distributed ethnography. 




## Setup

### Toolchain

This repo was written on MacOS, but any Unix-based OS should work. You will need the following tools:

| Tool    | Notes                                                                                                 |
|---------|-------------------------------------------------------------------------------------------------------|
| sqlite3 | Simple data storage solution for the application. Converting to a backend like Postgress is possible. |
| yq      | Used to parse TOML configuration files to set local and testing environments.                         |
| make    | Used to hide the headache of managing python environments.                                            |
| python3 | This application is written in python 3.12, but likely works for versions >= 3.9.                     |

Install these from your respective package manager.

### Database

To setup the local sqlite3 database, pick a location to house the database and update `/config/local.toml` to point `SQLITE_FILE` to this location.

Then, run `make setup-db`.
