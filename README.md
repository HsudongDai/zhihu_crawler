# Abstract
It is a simple web crawler of several search pages of ZHIHU.com.

# How to start the crawler
```shell
python3 main.py 
```
There are several command line parameters you may have to configure mannually to ensure the service can run normally. <br>
* --db_user: the name of your account which you log in to the database
* --db_passwd: the password of your database account
* --db_name: the name of the database that you want to connect
* --db_addr: the IP address of the database that you want to connect

# Outer reliance
## Developing Environment
Personally, I build and test the structure on Windows 10 Professional, with MySQL 8.0.18 and Anaconda, whose Python's version is 3.7.4.
## Target Environment
The project is designed to run on Linux server, relying on Python, whose version is bigger than 3.6, and PostgreSQL or MongoDB.
## Docker configuration
 In order to build it as a micro service, we provide **Dockerfile** in buildDocker folder. It is designed to work on CentOS 8, the latest version. Simply you merely need to add all python files into the folder and run dockerfile.
## How to configure Chrome in Docker image
Though in **Dockerfile** we have configured how to install Chrome without GUI, there are still several steps which have to be done manually to ensure the project to work. Please *strictly* follow the below.
1. ddd
2. fff


# Project Structure
|--main.py <br>
|--spiders<br>
&emsp;  |--indexZhihu.py<br>
&emsp;  |--models.py<br>
&emsp;  |--multithread.py<br>
&emsp;  |--mysql_connect.py<br>
&emsp;  |--to_xlsx.py<br>
<br>
Here are the illustrations of these files.
* main.py : the entrance of whole project, accept command line paremeters, pass them to the function which connects to MySQL.
* indexZhihu.py : invoke all the modules defined in Spiders to finish the job of generating target info.
* models.py : The conglomrate of several practical functions which are used in other modules. For example, it provides the functions to capture a website, extract target urls, modify urls to 