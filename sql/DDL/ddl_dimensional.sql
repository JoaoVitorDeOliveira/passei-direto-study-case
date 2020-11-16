CREATE SCHEMA IF NOT EXISTS "DM_PASSEI_DIRETO";

--SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS "DM_PASSEI_DIRETO".FAT_STUDENTS;
DROP TABLE IF EXISTS "DM_PASSEI_DIRETO".DIM_COURSES;
DROP TABLE IF EXISTS "DM_PASSEI_DIRETO".DIM_SESSIONS;
DROP TABLE IF EXISTS "DM_PASSEI_DIRETO".DIM_STUDENT_FOLLOW_SUBJECT;
DROP TABLE IF EXISTS "DM_PASSEI_DIRETO".DIM_SUBJECTS;
DROP TABLE IF EXISTS "DM_PASSEI_DIRETO".DIM_SUBSCRIPTIONS;
DROP TABLE IF EXISTS "DM_PASSEI_DIRETO".DIM_UNIVERSITIES;
--SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE "DM_PASSEI_DIRETO".FAT_STUDENTS (
    SK_STUDENT SERIAL PRIMARY KEY,
    ID VARCHAR(100) NOT NULL,
    REGISTERED_DATA TIMESTAMP NOT NULL,
    STATE VARCHAR(100) NOT NULL,
    CITY VARCHAR(100) NOT NULL,
    UNIVERSITY_ID INTEGER NOT NULL,
    COURSE_ID INTEGER NOT NULL,
    SIGNUP_SOURCE VARCHAR(100) NOT NULL,
    CHANGE_DATE DATE NULL
);

CREATE TABLE "DM_PASSEI_DIRETO".DIM_COURSES (
    SK_COURSES SERIAL PRIMARY KEY,
    ID INTEGER NOT NULL,
    NAME VARCHAR(100) NOT NULL,
    CHANGE_DATE DATE NULL,
    UNIQUE(ID)
);

CREATE TABLE "DM_PASSEI_DIRETO".DIM_SESSIONS (
    STUDENT_ID VARCHAR(100) NOT NULL,
    START_TIME TIMESTAMP NOT NULL,
    STUDENT_CLIENT VARCHAR(100) NOT NULL
);

CREATE TABLE "DM_PASSEI_DIRETO".DIM_STUDENT_FOLLOW_SUBJECT (
    STUDENT_ID VARCHAR(100) NOT NULL,
    SUBJECT_ID INTEGER NOT NULL,
    FOLLOW_DATE TIMESTAMP NOT NULL
);

CREATE TABLE "DM_PASSEI_DIRETO".DIM_SUBJECTS (
    SK_SUBJECTS SERIAL PRIMARY KEY,
    ID INTEGER NOT NULL,
    NAME VARCHAR(100) NOT NULL,
    CHANGE_DATE DATE NULL,
    UNIQUE(ID)
);

CREATE TABLE "DM_PASSEI_DIRETO".DIM_SUBSCRIPTIONS (
    STUDENT_ID VARCHAR(100) NOT NULL,
    PAYMENT_DATE TIMESTAMP NOT NULL,
    PLAN_TYPE VARCHAR(10) NOT NULL
);

CREATE TABLE "DM_PASSEI_DIRETO".DIM_UNIVERSITIES (
    SK_UNIVERSITIES SERIAL PRIMARY KEY,
    ID INTEGER NOT NULL,
    NAME VARCHAR(100) NOT NULL,
    CHANGE_DATE DATE null,
    UNIQUE(ID)
);

ALTER TABLE "DM_PASSEI_DIRETO".FAT_STUDENTS ADD FOREIGN KEY (UNIVERSITY_ID) REFERENCES "DM_PASSEI_DIRETO".DIM_UNIVERSITIES(ID);
ALTER TABLE "DM_PASSEI_DIRETO".FAT_STUDENTS ADD FOREIGN KEY (COURSE_ID) REFERENCES "DM_PASSEI_DIRETO".DIM_COURSES(ID);
ALTER TABLE "DM_PASSEI_DIRETO".DIM_STUDENT_FOLLOW_SUBJECT ADD FOREIGN KEY (SUBJECT_ID) REFERENCES "DM_PASSEI_DIRETO".DIM_SUBJECTS(ID);