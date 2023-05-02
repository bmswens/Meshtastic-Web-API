# Meshtastic Web API

[![Docs](https://img.shields.io/badge/Docs-Deployed-brightgreen)](https://bmswens.github.io/Meshtastic-Web-API/)
[![Test](https://github.com/bmswens/Meshtastic-REST-API/actions/workflows/Test.yml/badge.svg)](https://github.com/bmswens/Meshtastic-REST-API/actions/workflows/Test.yml)
[![Coverage Status](https://coveralls.io/repos/github/bmswens/Meshtastic-Web-API/badge.svg?branch=main)](https://coveralls.io/github/bmswens/Meshtastic-Web-API?branch=main)
[![Docker Build](https://img.shields.io/badge/Docker%20Build-Automated-brightgreen)](https://github.com/bmswens/Meshtastic-Web-API/actions/workflows/docker.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/bmswens/meshtastic-web-api)](https://hub.docker.com/repository/docker/bmswens/meshtastic-web-api)
[![License](https://img.shields.io/github/license/bmswens/Meshtastic-REST-API)](https://github.com/bmswens/Meshtastic-REST-API/blob/master/LICENSE.txt)


---
## Overview
A web-based API to be hosted on devices connected to a [Meshtastic](https://github.com/meshtastic) node via serial connection.

## Installation
`Coming soon`

## Usage
`Coming soon`

## Documentation

### Docker Environment Variables

| Name | Description | Example | Default |
| ---- | ----------- | ------- | ------- |
| MATTERMOST_ENABLED | Boolean; if set to anything, Mattermost integration will be enabled | `TRUE` | Empty |
| MATTERMOST_TOKEN | String; the token of the Mattermost server to communicate with | `zmigewsanbbsdf59xnmduzypjc` | Empty |
| MATTERMOST_WEBHOOK | String; URL to POST messages to | `http://chat.apocrypha.swenson.software/hooks/p9crnwz8uiyk5mjk1tm745q4ky` | Empty |

### Github Pages
Searchable documentation is deployed on Github pages and can be found [here](https://bmswens.github.io/Meshtastic-Web-API/).

### Local Deployments
Endpoints are documented using [Swagger](https://swagger.io/) via [RestX](https://flask-restx.readthedocs.io/en/latest/index.html) at the root URL and can be executed from there.

## Plans
- [ ] Implement all Python CLI functionality via HTTP
- [ ] Add websocket support for real time chat functionality

## Authors

* **Brandon Swenson**- *Initial work* - [bmswens](https://github.com/bmswens)

## License

This project, like Meshtastic, is licensed under the GNU General Public License - see the [LICENSE.txt](LICENSE.txt) file for details