# distributed-ethnography

[![Continuous Integration](https://github.com/epwr/distributed-ethnography/actions/workflows/Continuous%20Integration.yml/badge.svg)](https://github.com/epwr/distributed-ethnography/actions/workflows/Continuous%20Integration.yml)

Distributed ethnography is a method of understanding a "community’s belief systems through their own narratives" (K Mausch, 2018). It tackles the idea 
that it's very difficult to use technology to understand what someone means by having the storyteller quickly explain the meaning of their story across
a set of dimensions. These dimensions can then be used as metadata. Technology can then use this metadata to aggregate and slice stories from hundreds 
or thousands of storytellers, and provide the end consumer of this information a way of understanding trends and then diving into the individual stories.

I first came across distributed ethnography through a speech given by Dave Snowden (D Snowden, 2016). In that speech, Dave makes a very strong case
for the weaknesses in traditional survey-based, and presented his approach of having survey respondents tell a story and then rank the meaning over 
their stories across sets of three positive qualities. This his argues -- and my further reading seems to support this argument -- can significantly 
reduce bias in the results.

However, the only tool that I've seen that supports running distributed ethnography is closed-source and maintained by Dave Snowden and his company 
The Cynefin Co. This opens up distributed ethnography to some criticism that it is just the same old survey-based research consulting under some excellent 
marketing-speak, but I'm not convinced. In the hopes that I'll get an opportunity to put some of this theory to the test, this repo serves as an open-source
tool to experiment with distributed ethnography.

## Setup

The goal is everything in this repo can be accomplished via `make`.

Note: This repo was written on MacOS, but any Unix-based OS should work. 

### Toolchain

To run this service, you will need the following programs on a Unix-based operating system:

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

## References:

- Mausch, K., Harris, D., Heather, E., Jones, E., Yim, J., & Hauser, M. (2018). Households’ aspirations for rural development through agriculture. Outlook on Agriculture, 47(2), 108-115. https://doi.org/10.1177/0030727018766940
- Snowden, D., (2016) _How leaders change culture through small actions_ [Conference presentation]. Bangor University. https://www.youtube.com/watch?v=MsLmjoAp_Dg
