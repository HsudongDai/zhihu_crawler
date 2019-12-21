CREATE DATABASE zhihu DEFAULT CHARSET=utf8mb4;
CREATE TABLE zhihu.search_result (
    search_rank INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    search_terms VARCHAR(20),
    question_url VARCHAR(100),
    question_title VARCHAR(100),
    question_follow_num INT,
    question_view_num BIGINT,
    question_top_answer_username VARCHAR(50),
    question_top_answer_id VARCHAR(60),
    create_time DATE
)  AUTO_INCREMENT=1;