#!/bin/bash
env $(cat env.test | xargs) python3 -m pytest --cov=src --cov-report term-missing