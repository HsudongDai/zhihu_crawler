# Abstract
It is a simple web crawler of several search pages of ZHIHU.com. Through the project, we hope to get several kinds of data from searching-result pages of ZHIHU. Here are the keywords we have to search:
* 面试(interview)
* 实习(intern)
* 找工作(job hunting)
* 简历(CV)
  
You can visit [ZHIHU_Search](https://www.zhihu.com/search) and enter the keywords to view the generated answer page.<br>
From the answer page, we will collect several information, which forms a tuple of table.
* search_terms : the word you search
* search_rank: the rank of this tuple
* question_url: the link of the question
* question_title: the name of question
* question_follow_num: the number of followers of the question
* question_view_num: how many times the question has been viewed
* question_top_answer_username: the *name* of account whose answer ranks first among all the answers
* question_top_answer_id: the *id* of account whose whose answer ranks first among all the answers

In order to distinguish potential same tuples, we add a **"create_time"** column to record when the tuple is created.
# How to start the crawler
```bash
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
1. Run the image in docker, entering bash
2. Find the path of Chrome, create a soft link for the sake of use 
```bash
which google-chrome-stable
ln -s [path] /bin/chrome
```
3. Solve the problem that *root* user cannot run chrome, which needs to modify file '/opt/google/chrome/google-chrome', modify the last line as:
```bash
exec -a "$0" "$HERE/chrome" "$@" --no-sandbox $HOME
```
4. Install chrome drive
   1. Download chromedrive built for installed version of Chrome
   2. build soft link and add 'x' mod
```bash
chmod +x chromedriver
sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
```


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
* models.py : The conglomrate of several practical functions which are used in other modules. For example, it provides the functions to capture a website, extract target urls, modify urls to standard format etc.
* multithread.py : In this file we define a class to execute multi-thread crawler. It is able to modify the number of threads you plan to use.
* mysql_connect.py : It is used to connect to the MySQL database, providing functions which respectively execute creating connection, closing connection and inserting tuples.
* to_xlsx.py: It intends to collect all tuples from table in SQL database and format the dataframe into an xlsx file.

We also have prepared createDatabase.sql for you to have a clear understanding of the design of our database. You can run it on your computer.

# Demostration of running result of the project
Here is a screenshot of the table.<br>
<img src="https://github.com/HsudongDai/zhihu_crawler/blob/master/screenshot.png?raw=true" alt="demoGraph">