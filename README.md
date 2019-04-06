# Project - Item Catalog
***

The project builds a dynamic web application with persistent data storage to provide a compelling service to the users. The web application provides a list of sports items within a variety of sports categories and integrates third party user registration and authentication. Authenticated users have the ability to post, edit, and delete their own items. 

The project created a RESTful web application from scratch using Python framework Flask and implemented third-party OAuth authentication using Google's Sign in authentication services, HTML5, CSS3, SQLite, VirtualBox, and Vagrant. Additionally it uses the various HTTP methods to relate to CRUD operations.

### Skills used for the project

* VirtualBox
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
* Google Sign-in API

### Features
* HTML - the structure of the pages
* CSS - the style of the pages
* Python/Flask backend
   * Full CRUD support using SQLAlchemy and Flask
   * JSON endpoints
   * Implement OAuth2.0 using Google Sign-in API for Authentication and Authorization
* Database - SQLite to store and organize the information

### Run the project
* Download and install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).
* Download and install [Vagrant](https://www.vagrantup.com/downloads.html).
* Download or clone the VM configuration file
   
   option 1: download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) 
   
   option 2: use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.
   
   Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory.
   
* Start the virtual machine
   
   From your terminal, inside the vagrant subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. 
   
   `$ vagrant up`
* Log into newly installed Linux VM

   When vagrant up is finished running, you will get your shell prompt back. At this point, you can run vagrant ssh to log into your newly installed Linux VM!
   
  `$ vagrant ssh`
* Inside the VM, change directory to `/vagrant/catalog` to navigate to the shared directory.
* Setup the database:

    `python database_setup.py`
* Populate values in the database

    `python generate_cat_items_temp.py`
* Run the application

    `python project.py`
* Access the application by visiting `http://localhost:5000`

### JSON Endpoints
* Localhost:5000/api/catalog.json - displays all items in JSON format

   ![Alt](/images/all_json.png "All items in JSON format")

* Localhost:5000/api/category/JSON - displays all categories in JSON format

   ![Alt](/images/cat_json.png "All categories in JSON format")

* localhost:5000/api/category/1/list/JSON - displays selected items in JSON format

   ![Alt](/images/item_json.png "Selected items in JSON format")


### REST Endpoints

* localhost:5000 - displays all current categories with the latest added items to public before login

   ![Alt](/images/home_login.png "Homepage before Login")
   
* localhost:5000/catalog/Basketball - selecting a specific category shows all the items available for that category to public before login

   ![Alt](/images/cat_items_login.png "Items in a specific category before Login")
   
* localhost:5000/catalog/Soccer/Two%20Shinguards/ - selecting a specific item shows the specific information about that item to public before login

   ![Alt](/images/item_info_login.png "Info for a specific Item before Login")
   
* localhost:5000 - after logging in, a user has the ability to add, update, or delete item information. Users are able to modify only those items that they themselves have created.

   ![Alt](/images/home_logout.png "Homepage Logged in")
   
* localhost:5000/catalog/new - adding a new item after logged in

   ![Alt](/images/add_new_logout.png "Add New")
   
* localhost:5000/catalog/Hockey/Hockey%20Stick - selecting a specific item shows you specific information about that item after logged in

   ![Alt](/images/item_info_logout.png "Info for a specific item")
   
* localhost:5000/catalog/Hockey/Hockey%20Stick/edit - users are able to edit only those items that they themselves have created.

   ![Alt](/images/item_edit_logout.png "Edit Item")
   
* localhost:5000/catalog/Hockey/Hockey%20Stick/delete- users are able to delete only those items that they themselves have created.

   ![Alt](/images/item_delete_logout.png "Delete Item")
