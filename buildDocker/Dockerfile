FROM centos:latest
LABEL author="Hsudongdai"
LABEL email="hsudongdai@foxmail.com"
WORKDIR /root

RUN yum -y install mysql
#安装服务器
RUN yum -y install mysql-server
#启动镜像时自启动
RUN chkconfig mysqld on
#启动MySQL服务
RUN service mysqld start
RUN mysql_install_db --user=root
ENV MYSQL_USER root
ENV MYSQL_PASS 990916
ENV LC_ALL en_US.UTF-8
# 加入初始化数据库的脚本文件
ADD build_table.sh /root/build_table.sh
RUN chmod 755 /root/build_table.sh
RUN /root/build_table.sh
# 安装完之后还需要进一步配置
# 参见README.md
ADD google-chrome.repo /etc/yum.repos.d/google-chrome.repo
RUN chmod 755 /etc/yum.repos.d/google-chrome.repo
RUN yum -y install google-chrome-stable --nogpgcheck

RUN yum -y install python3
RUN yum -y install crontabs
RUN yum -y install Xvfb

RUN pip3 install bs4
RUN pip3 install pymysql
RUN pip3 install selenium

RUN mkdir /crawl
RUN mkdir /crawl/spiders
ADD main.py /crawl/main.py
ADD indexZhihu.py /crawl/spiders/indexZhihu.py
ADD models.py /crawl/spiders/models.py
ADD multithread.py /crawl/spiders/multithread.py
ADD mysql_connect.py /crawl/spiders/mysql_connect.py
# 将定时任务添加到目录下
RUN echo "0 10 * * 1 root python3 main.py >> /tmp/tmp.txt" >> /etc/crontab