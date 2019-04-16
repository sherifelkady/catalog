# Project : Items Catalog
### by Sherif Elkady

## Description
The Item Catalog project consists of developing an application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system.

## Requirements
* Python 3
* Flask
* Vagrant
* VirtualBox
* Git
* You can also use anaconda instead of (vagrant , VirtualBox)

## Getting Started
1 - Download and install VirtualBox and vagrant
2 - Download [Data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
3 - Download this [folder](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)
4 - Open folder Directory by using GitBash then type vagrant up
5 - Use vagrant ssh to log in 
3 - Back to the catlog folder and Run python app.py

## Third Party Integration
This application use google third party to login and create , update and delete items ,
to login with google you have to registration an account with the same email in your google account

## Demo account
* Username : shirefelkady
* Password : 123123

## Json Endpoint 
http://localhost:5000/catlog/json

### JSON Endpoint of selected specific item
http://localhost:5000/api/category/5/item/4/json
