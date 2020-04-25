# MFTBR
Multi-Faceted Trust Based Recommendation System  
This repository contains and demonstrates a model built to carry out rating prediction for user-item pairs in an e-commerce environment.

### Dataset
Rich Epinions Dataset, can be found at:  https://projet.liris.cnrs.fr/red/ 

## Dependencies
1. Python 3.5-3.7
2. Pip 19.0+
3. Angular 8

## Installation
### front-end: flask-crm/frontend
`npm install`
### back-end: flask-crm/backend
`pip3 install -r requirements.txt`  
  
#### Note
If the above command fails due to:
  * inability to find tensorflow 2.1.0, update Pip to a version > 19.0 as mentioned in dependencies
  * other reasons; or succeeds, but on running the demo, some modules are missing/prediction does not work due to server error: kindly check the versions of installed Python modules against flask-crm/backend/requirements.txt

## Running
### back-end server: flask-crm/backend
1. `flask run`
2. Server runs on localhost:5000; to check the APIs, import the given Postman collection referred to in the last section

### front-end server: flask-crm/frontend
1. `ng serve`
2. Server runs on localhost:4200

## API Calls
Import Postman Collection from https://www.getpostman.com/collections/bf27a89218c8a2d329dd
