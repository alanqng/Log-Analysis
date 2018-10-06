# Log.py

Log.py is a simple python script for demonstrating the capabilities and knowledge learned through the first section of the Udacity's Full Stack nanodegree program. The scripts looks for data in an already built database and performs this query through the implementation of **psycopg2** library for integrating Postgresql into python.

## Installation
### Python
The user must be able to run python scripts on shell interface either Python 2 or Python 3.

If you don't have python installed please go to [Python]("https://www.python.org/downloads/"). Download the python installer and follow the instructions.
### Virtual Machine(VM), Vagrant
This project make use of a Ubuntu based Virtual Machine which you can download from [here]("https://github.com/udacity/fullstack-nanodegree-vm")

First you need to download [VM]("https://www.virtualbox.org/wiki/Downloads") and follow the on screen steps.

Then install [Vagrant]("https://www.vagrantup.com/downloads.html") which will enable the configuration of your virtual machine through the shell.

Once the VM and Vagrant are installed and you have your virtual machine files, go to your downloaded virtual machine file's directory on the shell and run the following commands:

```
vagrant up
vagrant ssh
```
After running the commands you will be prompted to the virtual machine's shell, you can confirmed by seeing _vagrant_ in your terminal.

### Database
The databe can be download from [here]("https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip")

You will need to unzip the file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.

To build the reporting tool, you'll need to load the site's data into your local database. 

To load the data, cd into the vagrant directory and use the command:
```
psql -d news -f newsdata.sql
```
Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

### Views
The user needs to create three views before running the script. Please run the following commands for creating the views needed by the script:

```sql
CREATE VIEW toparticles as 
        SELECT articles.title, l.count 
        FROM articles JOIN 
        (SELECT path, COUNT(*) as count 
        FROM log GROUP BY path) as l
        ON CONCAT('/article/', articles.slug) = l.path
        ORDER BY count desc

CREATE VIEW auth as
        SELECT articles.title, authors.name 
        FROM articles JOIN authors
        ON articles.author = authors.id

CREATE VIEW logerrors as
        SELECT logstatus.date, 
        TRUNC((status400.total *1.0) / (logstatus.total *1.0) * 100,2) 
        as percentage
        FROM
        (SELECT date(time), COUNT(*) as total
        FROM log 
        GROUP BY date(time)) as logstatus
        JOIN
        (SELECT date(time), COUNT(*) as total
        FROM log 
        WHERE status = '404 NOT FOUND' 
        GROUP BY date(time)) as status400
        ON logstatus.date = status400.date
        GROUP BY logstatus.date, logstatus.total, status400.total
```



## Usage
Log.py requires three new views to be created in the already supplied database. After the creating of this three views the user can run the script.
For the creation of the views refer to [Installation](##Installation)

After the views are created run the script, just open a terminal where the Log.py file is located and run the following command:

```shell
python log.py
```

The three queries that the script perform are:

### Queries:
* Queries the three most viewed articles in descending order
* Queries the three most popular authors according to views
* Queries the days that 404 errors were more than 1% of the total requests

The python script contains one function for each query:

### Functions:
* get_top_post()
* get_top_authors()
* get_errors()
