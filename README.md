


  <h3 align="center">MYOB Vote_App</h3>




<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

This is a simple picture upload and voting application.<br>
Application accepts PNG or JPG files.<br>
Each picture can be tagged with description.<br>
Application offers voting functionality.<br>
Pictures are displayed on the main page in a sequence determined by the ranking algorythm, starting with rank:0 (the more more votes the lower rank number):<br>
rank:0<br>
rank:1<br>
rank:2 ...<br>

### Built With
Appliation is written in python3 using Flask framework and SQLite and delivered in docker container.
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [SQLite](https://www.sqlite.org/index.html)
* [Docker](https://docker.com)



<!-- GETTING STARTED -->
## Getting Started

Here you will find installation instructions. <br>Please note that while it is possible to run this application natively it has been intended for container environment.

### Prerequisites

Application has been created and tested using <b>Docker version 19.03.12</b> , but should work on earlier and later versions as well.
* For native installation prerequistis please refer to the Dockerfile and requirements.txt files in the root directory.

### Installation
#### Build your own Docker image

1. Clone the repo
```sh
git clone https://github.com/zbigniewseifert/myob2_project.git
```
2. Build Docker image
```sh
cd myob2_project/myob2; docker build -t <username>/<repository>:<tag> .
```
#### Download image from Docker Hub

1. Download docker image
```sh
docker pull zseifert/vote_app:travis
```

#### Travis pipeline
1. Application root directory contains travis yml file and a docker push script which enables Travis-CI pipline with an automated docker build.
To work you need to configure following varibales in your Travis repository:<br>
```JS
$DOCKER_USERNAME=
$DOCKER_PASSWORD=
```
<!-- USAGE EXAMPLES -->
## Usage
### Docker image configuration

1. Application is exposing port 8888 within docker container
2. Application stores persistent data in /app/db and /app/upload_files directories
3. Application is delivered with build in /health and /metadata endpoints

### Docker run command
```sh
docker run -d -p 8888:8888 -v /local/db:/app/db -v /local/upload_files:/app/upload_files zseifert/vote_app:travis
```

### Accesssing healthcheck
/health enpoint return json object with sqlite db status and access to upload_files directory. <br>

```sh
curl www.example.com:8888/health
{"hostname": "5c3f5ff91c94", "status": "success", "timestamp": 1597736769.7821982, "results": [{"checker": "healthcheck_db", "output": "sqlitedb OK", "passed": true, "timestamp": 1597736769.7669322, "expires": 1597736796.7669322}, {"checker": "healthcheck_uploads_dir", "output": "UploadDir OK", "passed": true, "timestamp": 1597736769.7821534, "expires": 1597736796.7821534}]}
```

<!-- ROADMAP -->
## Roadmap

1. User management
2. Administrative panel



<!-- CONTACT -->
## Contact


Project Link: [https://github.com/zbigniewseifert/myob2_project](https://github.com/zbigniewseifert/myob2_project)

[product-screenshot]: vote_app.png
