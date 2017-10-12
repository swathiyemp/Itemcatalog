Item Catalog Application
This project is for creating an application that displays categories with list of items and their JSON endpoints. This App utilizes the oauth functionality from google to enable the users to sign in or sign up for performing CRUD operations.


Getting Started  
* Log in to your GitHub account and click ItemCatalog to go to the repository and fork it.
* Download Git from the link specified in prerequisites and install.
* Click on Git Bash and run the following command-- 
          Git clone http://github.com/<username>/https://github.com/swathiyemp/
            ItemCatalog
* Replace <username> with your Github User Name in the command above. 
   
     Prerequisites


1.  Vagrant--https://www.vagrantup.com/downloads.html
2.  Virtual Box--https://www.virtualbox.org/wiki/Downloads
3.  Git--https://git-scm.com/downloads
4.  Google Client Id and Client Secret--https://console.developers.google.com


     Installing
1. Install the Git with default options.
2. Install Virtual box with default specifications and make sure you don’t  launch it.
3. To install Vagrant, first find the appropriate package for your system and download it.  Run the installer for your system. The installer will automatically add vagrant to your system path so that it is available in Git. 
4. For creating client id and client secrets goto https://console.developers.google.com and then follow below steps.
* Click credentials from the left menu
* Then click create credentials.
* Choose OAuth client id
* Click configure consent screen
* In the product name option type Item Catalog Application
* In the home page url type http://localhost:5000
* Click save
* Then choose web application from the options
* Name it Item Catalog Application
* In the advanced javascript origins type http://localhost:5000
* Click create
* Then it gives you client id and client secret
* Click on download button and download the file.
* After downloading rename the file to client_secrets.json and save it in your ItemCatalog directory that you have already cloned.
* Open editor such as atom or sublime and  click file and open folder then choose ItemCatalog.
* Then select list of items.py file from the left menu.
* Enter your username and email id in the fields with name and email and save it.
* Click on login.html file and paste your client id that you just created from console.developer.google page in ‘data-clientid’ field.
* save all.


Running the Application  
* Go to ItemCatalog directory and right click and choose Git Bash Here.
* The Git terminal opens up.
* Type vagrant up and wait until it finishes loading.
* Then type vagrant ssh.
* Type cd/vagrant 
* Type ls to make sure ItemCatalog is present in the directory, then type cd ItemCatalog.
* Type python application.py and open the browser.
* In the browser type http://localhost:5000
* The application will open, click log in and enter your gmail credentials.


Built With
* Python
* Flask
* SQL Alchemy
* HTML
* BootStrap
* CSS