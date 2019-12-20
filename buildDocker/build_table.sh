mysqld_safe &
sleep 3
mysql -e "GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASS' WITH GRANT OPTION;"
mysql -e "CREATE DATABASE zhihu DEFAULT CHARSET=utf8mb4;"
mysql -e "create table zhihu.search_result (
        search_rank INT NOT NULL primary key auto_increment,
        search_terms varchar(20),
        question_url varchar(100),
        question_title varchar(100),
        question_follow_num INT,
        question_view_num bigint,
        question_top_answer_username varchar(50),
        question_top_answer_id varchar(60),
        create_time date
        )auto_increment = 1;"
