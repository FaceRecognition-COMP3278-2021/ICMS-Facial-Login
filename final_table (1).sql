CREATE TABLE Student(
  student_id BIGINT NOT NULL,
  log_id VARCHAR(80) NOT NULL,
  name VARCHAR(80) NOT NULL,
  email_address VARCHAR(80),
  log_in DATETIME,
  log_out DATETIME,
  PRIMARY KEY(student_id,log_id)
);

CREATE TABLE Course(
  course_id VARCHAR(80) NOT NULL,
  academic_year INT,
  PRIMARY KEY(course_id)
);

CREATE TABLE Lecture(
  course_id VARCHAR(80) NOT NULL,
  lecture_id VARCHAR(80) NOT NULL,
  lecture_name VARCHAR(150) NOT NULL,
  lecturer VARCHAR(80),
  l_email_address VARCHAR(80),
  PRIMARY KEY(course_id,lecture_id),
  FOREIGN KEY(course_id) REFERENCES Course(course_id)
);

CREATE TABLE Lecture_time(
  course_id VARCHAR(30) NOT NULL,
  lecture_id VARCHAR(30) NOT NULL,
  lecture_day VARCHAR(30) NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  lecture_room VARCHAR(30),
  online VARCHAR(150),
  PRIMARY KEY (course_id, lecture_id,lecture_day),
  FOREIGN KEY (course_id, lecture_id) REFERENCES Lecture(course_id,lecture_id)
);

CREATE TABLE Lecture_date(
  course_id VARCHAR(30) NOT NULL,
  lecture_id VARCHAR(30) NOT NULL,
  lecture_date DATE NOT NULL,
  PRIMARY KEY (course_id, lecture_id, lecture_date),
  FOREIGN KEY (course_id,lecture_id) REFERENCES Lecture(course_id,lecture_id)
);

CREATE TABLE Lecture_message(
  course_id VARCHAR(30) NOT NULL,
  lecture_id VARCHAR(30) NOT NULL,
  lecture_message VARCHAR(100) NOT NULL,
  PRIMARY KEY (course_id, lecture_id, lecture_message),
  FOREIGN KEY (course_id,lecture_id) REFERENCES Lecture(course_id,lecture_id)
);

CREATE TABLE Lecture_materials(
  course_id VARCHAR(30) NOT NULL,
  lecture_id VARCHAR(30) NOT NULL,
  lecture_materials VARCHAR(100) NOT NULL,
  PRIMARY KEY (course_id, lecture_id, lecture_materials),
  FOREIGN KEY (course_id,lecture_id) REFERENCES Lecture(course_id,lecture_id)
);

CREATE TABLE Tutorial(
  course_id VARCHAR(80) NOT NULL,
  tutorial_id VARCHAR(80) NOT NULL,
  tutor VARCHAR(80),
  t_email_address VARCHAR(80),
  PRIMARY KEY(course_id,tutorial_id),
  FOREIGN KEY(course_id) REFERENCES Course(course_id)
);

CREATE TABLE Tutorial_time(
  course_id VARCHAR(30) NOT NULL,
  tutorial_id VARCHAR(30) NOT NULL,
  tutorial_day VARCHAR(30) NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  tutorial_room VARCHAR(30),
  online VARCHAR(150),
  PRIMARY KEY (course_id, tutorial_id,tutorial_day),
  FOREIGN KEY (course_id, tutorial_id) REFERENCES Tutorial(course_id,tutorial_id)
);

CREATE TABLE Tutorial_date(
  course_id VARCHAR(30) NOT NULL,
  tutorial_id VARCHAR(30) NOT NULL,
  tutorial_date DATE NOT NULL,
  PRIMARY KEY (course_id, tutorial_id, tutorial_date),
  FOREIGN KEY (course_id,tutorial_id) REFERENCES Tutorial(course_id,tutorial_id)
);

CREATE TABLE Tutorial_message(
  course_id VARCHAR(30) NOT NULL,
  tutorial_id VARCHAR(30) NOT NULL,
  tutorial_message VARCHAR(100) NOT NULL,
  PRIMARY KEY (course_id, tutorial_id, tutorial_message),
  FOREIGN KEY (course_id,tutorial_id) REFERENCES Tutorial(course_id,tutorial_id)
);

CREATE TABLE Tutorial_materials(
  course_id VARCHAR(30) NOT NULL,
  tutorial_id VARCHAR(30) NOT NULL,
  tutorial_materials VARCHAR(100) NOT NULL,
  PRIMARY KEY (course_id, tutorial_id, tutorial_materials),
  FOREIGN KEY (course_id,tutorial_id) REFERENCES Tutorial(course_id,tutorial_id)
);

CREATE TABLE Student_in_Lecture(
  student_id BIGINT NOT NULL,
  course_id VARCHAR(30) NOT NULL,
  lecture_id VARCHAR(30) NOT NULL,
  PRIMARY KEY (student_id, course_id, lecture_id),
  FOREIGN KEY (student_id) REFERENCES Student (student_id),
  FOREIGN KEY (course_id, lecture_id) REFERENCES Lecture(course_id, lecture_id)
);

CREATE TABLE Student_in_Tutorial(
  student_id BIGINT NOT NULL,
  course_id VARCHAR(30) NOT NULL,
  tutorial_id VARCHAR(30) NOT NULL,
  PRIMARY KEY (student_id, course_id, tutorial_id),
  FOREIGN KEY (student_id) REFERENCES Student (student_id),
  FOREIGN KEY (course_id, tutorial_id) REFERENCES Tutorial(course_id, tutorial_id)
);


CREATE TABLE Student_enroll_Course(
  student_id BIGINT NOT NULL,
  course_id VARCHAR(30) NOT NULL,
  PRIMARY KEY (student_id,course_id),
  FOREIGN KEY (student_id) REFERENCES Student(student_id),
  FOREIGN KEY (course_id) REFERENCES Course(course_id)
);
