# Project - Item Catalog
***

### Project Overview


This project builds dynamic modern web application with persistent data storage to provide a compelling service to the users. 

The web application provides a list of sport items within a variety of sport categories and integrate third party user registration and authentication. Authenticated users should have the ability to post, edit, and delete their own items. 

The project was created a RESTful web application from scratch using Python framework Flask along with implementation third-party OAuth authentication using Google's Sign in authentication services, HTML5, CSS3, SQLite, VirtualBox, Vagrant. Additionally it uses the various HTTP methods to relate to CRUD operations.

### Skills used for the project

* Virtual Box
* Vagrant
* Python
* HTTP methods
* CRUD operations
* HTML
* CSS
* JavaScript
* Flask
* SQLAchemy
* SQLite
* OAuth 2.0
* Google SignIn

### Features
* Authentication and Authorization
* Full CRUD support using SQLAlchemy and Flask
* JSON endpoints
* Implement OAuth2.0 using Google Sign-in API
### Project Structure

* ??????
* 

### Run the project
* Download and install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).
* Download and install [Vagrant](https://www.vagrantup.com/downloads.html).
* Download or clone the VM configuration file
   option 1: download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) 
   
   option 2: use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.
   Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory.
   
* Start the virtual machine
   From your terminal, inside the vagrant subdirectory, run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it. 
   `$ vagrant up`
* Log in to newly installed Linux VM
   When vagrant up is finished running, you will get your shell prompt back. At this point, you can run vagrant ssh to log in to your newly installed Linux VM!
  `$ vagrant ssh`
* Inside the VM, change directory to `/vagrant` to navigate the shared directory.
* Setup the database:
    `python database_setup.py`
* Populate values in the database
    `python generate_cat_items_temp.py`
* Run the application
    `python project.py`
* Access the application by visiting `http://localhost:5000`