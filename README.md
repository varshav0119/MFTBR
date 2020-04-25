# MFTBR
Multi-Faceted Trust Based Recommendation System  
This repository contains and demonstrates a model built to carry out rating prediction for user-item pairs in an e-commerce environment.

###Dataset
Rich Epinions Dataset, can be found at:  https://projet.liris.cnrs.fr/red/ 

## Dependencies
1. Python3
2. Angular 8, with Node version 10+

## Installation
### front-end: flask-crm/frontend
`npm install`
### back-end: flask-crm/backend
`pip3 install -r requirements.txt`  
  
  
If the above command fails, or succeeds but on running the server some modules are missing, kindly install them manually and proceed.

## Running
### back-end server: flask-crm/backend
1. `flask run`
2. Server runs on localhost:5000; to check the APIs, import the given Postman collection referred to in the last section

### front-end server: flask-crm/frontend
1. `ng serve`
2. Server runs on localhost:4200

## API Calls
Import Postman Collection from https://www.getpostman.com/collections/bf27a89218c8a2d329dd
