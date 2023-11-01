# AAM-Small-App
##### Version 1.0
![Demo Animation](https://example.com/demo.gif)


---
## Overview

AAM-Small-App is a small webapp that allows you to customize the 3d model of a masterplan. You have the ability to 
- change the hight of the buildings 
- the width of different types of roads
- the density level of the trees 
- [Save File!](.). 

## Features

##### Backend

- read customized rhino files
- generate customized masterplan 3d model using aam_data_structure 
- send 3dm modeling information to frontend

##### Frontend

- User Interface contains the Navbar, Right Menu, and the 3js scene.
- Right panel allows you to change:
    1. building hight
    2. l1_road width
    3. l2_road width
    4. l4_road width
- Save Rhino File to local directory. 

## Installation 

To use the app, clone this repository to your local directory.

##### To run the server:
  1. create new conda environment with python 3.8
  2. install required packages
  3. change file loading directories
  4. change file saving directories
  5. cd into backend and run `<flask run app-app.py>`

##### To run Frontend:

1. cd into frontend/aam folder
2. run `<npm install>`
3. run `<npm run dev>`
    
