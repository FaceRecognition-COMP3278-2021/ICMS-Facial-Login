INSERT INTO Student (student_id,log_id, name,  email_address,log_in,log_out) VALUES
(3035603526,'ksho719','Sunghyun Kim','ksho719@connect.hku.hk',NULL,NULL),
(3035554658,'tngus254','Suhyun Choi','tngus254@conncet.hku.hk',NULL,NULL),
(3035603930,'yjlee','Yoonjeong Lee','u3560393@connect.hku.hk',NULL,NULL),
(3035596307,'nurnur','Nurdaulet Kemel','u3559630@conncet.hku.hk',NULL,NULL),
(3035553355,'michael','Michael','u3555335@connect.hku.hk',NULL,NULL),
(3035664466,'iammichael','Inyeoreum Chong','hot@connect.hku.hk',NULL,NULL);

INSERT INTO Course (course_id, academic_year) VALUES
('2021STAT3621S2',2021),
('2021CHIN9503S2',2021),
('2021STAT3600S2',2021),
('2021COMP2119S2',2021),
('2021COMP3278S2',2021),
('2021STAT4609S2',2021),
('2021CCST9042S2',2021);

INSERT INTO Lecture (course_id,lecture_id,lecture_name,lecturer,l_email_address) VALUES
('2021STAT3621S2','STAT3621A','Statistical data analysis','Dr. Ingaeul Chong','cool@connect.hku.hk'),
('2021CHIN9503S2','CHIN9503A','Chinese as a foreign language III','Ms.Nihao Jin','hello@connect.hku.hk'),
('2021CHIN9503S2','CHIN9503B','Chinese as a foreign language III','Ms.Nihao Jin','hello@connect.hku.hk'),
('2021STAT3600S2','STAT3600A','Linear statistical anaysis','Ms.Yoonjung Li','dessert@connect.hku.hk'),
('2021COMP2119S2','COMP2119A','Introduction to data structures and algorithms','Dr.Soohyeon Choi','engigoddess@conncet.hku.hk'),
('2021COMP3278S2','COMP3278A','Introduction to database management systems','Mr. Nulldaulet Kemel','smartboi@conncet.hku.hk'),
('2021STAT4609S2','STAT4609A','Big data analytics','Mrs.Chengxian Jin','loopy@connect.hku.hk'),
('2021CCST9042S2','CCST9042A','The World of Waves','Ms.Soohyeon Kim','johnjal@conncet.hku.hk');


INSERT INTO Lecture_time (course_id,lecture_id,lecture_day,start_time,end_time,lecture_room,online) VALUES
('2021STAT3621S2','STAT3621A','MON','09:30:00','12:20:00','LE3','https://hku.zoom.us/j/95660717361'),
('2021CHIN9503S2','CHIN9503A','MON','15:30:00','17:30:00','CPD 1.04','https://hku.zoom.us/j/95660717361'),
('2021CHIN9503S2','CHIN9503A','FRI','15:30:00','17:30:00','CPD 1.04','https://hku.zoom.us/j/95660717361'),
('2021CHIN9503S2','CHIN9503B','TUE','16:30:00','18:20:00','CPD 1.01','https://hku.zoom.us/j/95660717361'),
('2021CHIN9503S2','CHIN9503B','THU','16:30:00','18:20:00','CPD 1.01','https://hku.zoom.us/j/95660717361'),
('2021STAT3600S2','STAT3600A','THU','13:30:00','16:20:00','LE3','https://hku.zoom.us/j/95660717361'),
('2021COMP2119S2','COMP2119A','TUE','12:30:00','13:20:00','CPD 101','https://hku.zoom.us/j/95660717361'),
('2021COMP2119S2','COMP2119A','FRI','12:30:00','14:20:00','CPD 101','https://hku.zoom.us/j/95660717361'),
('2021COMP3278S2','COMP3278A','FRI','09:30:00','11:20:00','online','https://hku.zoom.us/j/95660717361'),
('2021STAT4609S2','STAT4609A','THU','13:30:00','16:20:00','online','https://hku.zoom.us/j/95660717361'),
('2021CCST9042S2','CCST9042A','WED','16:30:00','18:20:00','online','https://hku.zoom.us/j/95660717361');

INSERT INTO Lecture_date(course_id,lecture_id,lecture_date) VALUES
('2021STAT3621S2','STAT3621A','2021-01-18'),
('2021CHIN9503S2','CHIN9503A','2021-01-18'),
('2021CHIN9503S2','CHIN9503A','2021-01-22'),
('2021CHIN9503S2','CHIN9503B','2021-01-19'),
('2021CHIN9503S2','CHIN9503B','2021-01-21'),
('2021STAT3600S2','STAT3600A','2021-01-21'),
('2021COMP2119S2','COMP2119A','2021-01-19'),
('2021COMP2119S2','COMP2119A','2021-01-22'),
('2021COMP3278S2','COMP3278A','2021-01-22'),
('2021STAT4609S2','STAT4609A','2021-01-21'),
('2021CCST9042S2','CCST9042A','2021-01-20');


INSERT INTO Lecture_message(course_id,lecture_id,lecture_message) VALUES
('2021STAT3621S2','STAT3621A','Install R studio before the lecture'),
('2021CHIN9503S2','CHIN9503A','Please submit the level test paper'),
('2021CHIN9503S2','CHIN9503B','Please submit the level test paper'),
('2021STAT3600S2','STAT3600A','No lecture today'),
('2021COMP2119S2','COMP2119A','Please do the survey'),
('2021COMP3278S2','COMP3278A','Have a nice holiday!'),
('2021STAT4609S2','STAT4609A','Please come to the lecture today'),
('2021CCST9042S2','CCST9042A','nothing');

INSERT INTO Lecture_materials(course_id,lecture_id,lecture_materials) VALUES
('2021STAT3621S2','STAT3621A','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html'),
('2021CHIN9503S2','CHIN9503A','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html'),
('2021CHIN9503S2','CHIN9503B','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html'),
('2021STAT3600S2','STAT3600A','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html'),
('2021COMP2119S2','COMP2119A','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html'),
('2021COMP3278S2','COMP3278A','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html'),
('2021STAT4609S2','STAT4609A','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html'),
('2021CCST9042S2','CCST9042A','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html');


INSERT INTO Tutorial (course_id,tutorial_id,tutor,t_email_address) VALUES
('2021STAT3621S2','STAT3621AA','Mr.Eunwoo Cha','chong@connect.hku.hk'),
('2021STAT3621S2','STAT3621AB','Mr.Bogum Park','bgpark@connect.hku.hk'),
('2021STAT3600S2','STAT3600AA','Ms.Suzi Bae','szbae@connect.hku.hk'),
('2021COMP3278S2','COMP3278AA','Ms.Taehee Kim','thkim@connect.hku.hk'),
('2021STAT4609S2','STAT4609AA','Mr.Joonggi Song','jgsong@connect.hku.hk'),
('2021CCST9042S2','CCST9042AA','Ms.Jieun Lee','iu@connect.hku.hk');

INSERT INTO Tutorial_time(course_id,tutorial_id,tutorial_day,start_time,end_time,tutorial_room,online) VALUES
('2021STAT3621S2','STAT3621AA','WED','08:30:00','09:20:00','MB103','https://hku.zoom.us/j/95660717361'),
('2021STAT3621S2','STAT3621AB','WED','09:30:00','10:20:00','MB103','https://hku.zoom.us/j/95660717361'),
('2021STAT3600S2','STAT3600AA','FRI','16:30:00','17:20:00','LE7','https://hku.zoom.us/j/95660717361'),
('2021COMP3278S2','COMP3278AA','TUE','09:30:00','10:20:00','online','https://hku.zoom.us/j/95660717361'),
('2021STAT4609S2','STAT4609AA','TUE','17:30:00','18:20:00','online','https://hku.zoom.us/j/95660717361'),
('2021CCST9042S2','CCST9042AA','WED','15:30:00','16:20:00','online','https://hku.zoom.us/j/95660717361');

INSERT INTO Tutorial_date(course_id,tutorial_id,tutorial_date) VALUES
('2021STAT3621S2','STAT3621AA','2021-01-20'),
('2021STAT3621S2','STAT3621AB','2021-01-20'),
('2021STAT3600S2','STAT3600AA','2021-01-22'),
('2021COMP3278S2','COMP3278AA','2021-01-19'),
('2021STAT4609S2','STAT4609AA','2021-01-19'),
('2021CCST9042S2','CCST9042AA','2021-01-20');


INSERT INTO Tutorial_message(course_id,tutorial_id,tutorial_message) VALUES
('2021STAT3621S2','STAT3621AA','No tutorial today'),
('2021STAT3621S2','STAT3621AB','Please bring your laptop'),
('2021STAT3600S2','STAT3600AA','nothing'),
('2021COMP3278S2','COMP3278AA','No tutorial this week'),
('2021STAT4609S2','STAT4609AA','Please hand in your assignment'),
('2021CCST9042S2','CCST9042AA','nothing');

INSERT INTO Tutorial_materials(course_id,tutorial_id,tutorial_materials) VALUES
('2021STAT3621S2','STAT3621AA','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html'),
('2021STAT3621S2','STAT3621AB','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html'),
('2021STAT3600S2','STAT3600AA','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html'),
('2021COMP3278S2','COMP3278AA','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html'),
('2021STAT4609S2','STAT4609AA','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html'),
('2021CCST9042S2','CCST9042AA','https://www.computer-pdf.com/database/888-tutorial-learning-mysql.html');

INSERT INTO Student_in_Lecture(student_id,course_id,lecture_id) VALUES
(3035603526,'2021STAT3621S2','STAT3621A'),
(3035603526,'2021CHIN9503S2','CHIN9503A'),
(3035603526,'2021COMP3278S2','COMP3278A'),
(3035603526,'2021STAT4609S2','STAT4609A'),
(3035664466,'2021STAT3621S2','STAT3621A'),
(3035664466,'2021CHIN9503S2','CHIN9503B'),
(3035664466,'2021STAT3600S2','STAT3600A'),
(3035664466,'2021COMP2119S2','COMP2119A'),
(3035553355,'2021STAT3621S2','STAT3621A'),
(3035553355,'2021COMP3278S2','COMP3278A'),
(3035553355,'2021STAT4609S2','STAT4609A'),
(3035554658,'2021CHIN9503S2','CHIN9503A'),
(3035554658,'2021COMP3278S2','COMP3278A'),
(3035554658,'2021STAT4609S2','STAT4609A'),
(3035596307,'2021COMP3278S2','COMP3278A'),
(3035596307,'2021STAT4609S2','STAT4609A'),
(3035596307,'2021CCST9042S2','CCST9042A'),
(3035603930,'2021STAT4609S2','STAT4609A'),
(3035603930,'2021COMP3278S2','COMP3278A'),
(3035603930,'2021CCST9042S2','CCST9042A');

INSERT INTO Student_in_Tutorial(student_id,course_id,tutorial_id) VALUES
(3035603526,'2021STAT3621S2','STAT3621AA'),
(3035603526,'2021COMP3278S2','COMP3278AA'),
(3035603526,'2021STAT4609S2','STAT4609AA'),
(3035664466,'2021STAT3621S2','STAT3621AB'),
(3035664466,'2021STAT3600S2','STAT3600AA'),
(3035553355,'2021STAT3621S2','STAT3621AA'),
(3035553355,'2021COMP3278S2','COMP3278AA'),
(3035553355,'2021STAT4609S2','STAT4609AA'),
(3035554658,'2021COMP3278S2','COMP3278AA'),
(3035554658,'2021STAT4609S2','STAT4609AA'),
(3035596307,'2021COMP3278S2','COMP3278AA'),
(3035596307,'2021STAT4609S2','STAT4609AA'),
(3035596307,'2021CCST9042S2','CCST9042AA'),
(3035603930,'2021STAT4609S2','STAT4609AA'),
(3035603930,'2021COMP3278S2','COMP3278AA'),
(3035603930,'2021CCST9042S2','CCST9042AA');

INSERT INTO Student_enroll_Course(student_id,course_id) VALUES
(3035603526,'2021STAT3621S2'),
(3035603526,'2021CHIN9503S2'),
(3035603526,'2021COMP3278S2'),
(3035603526,'2021STAT4609S2'),
(3035664466,'2021STAT3621S2'),
(3035664466,'2021CHIN9503S2'),
(3035664466,'2021STAT3600S2'),
(3035664466,'2021COMP2119S2'),
(3035553355,'2021STAT3621S2'),
(3035553355,'2021COMP3278S2'),
(3035553355,'2021STAT4609S2'),
(3035554658,'2021CHIN9503S2'),
(3035554658,'2021COMP3278S2'),
(3035554658,'2021STAT4609S2'),
(3035596307,'2021COMP3278S2'),
(3035596307,'2021STAT4609S2'),
(3035596307,'2021CCST9042S2'),
(3035603930,'2021STAT4609S2'),
(3035603930,'2021COMP3278S2'),
(3035603930,'2021CCST9042S2');
