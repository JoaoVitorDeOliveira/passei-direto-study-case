DROP TABLE IF EXISTS STG_FAT_STUDENTS;
DROP TABLE IF EXISTS STG_DIM_COURSES;
DROP TABLE IF EXISTS STG_DIM_SESSIONS;
DROP TABLE IF EXISTS STG_DIM_STUDENT_FOLLOW_SUBJECT;
DROP TABLE IF EXISTS STG_DIM_SUBJECTS;
DROP TABLE IF EXISTS STG_DIM_SUBSCRIPTIONS;
DROP TABLE IF EXISTS STG_DIM_UNIVERSITIES;

CREATE TABLE STG_FAT_STUDENTS (
    SK_STUDENT VARCHAR(100),
    ID VARCHAR(100),
    REGISTERED_DATA VARCHAR(100),
    STATE VARCHAR(100),
    CITY VARCHAR(100),
    UNIVERSITY_ID VARCHAR(100),
    COURSE_ID VARCHAR(100),
    SIGNUP_SOURCE VARCHAR(100),
    CHANGE_DATE VARCHAR(100)
);

CREATE TABLE STG_DIM_COURSES (
    SK_COURSES VARCHAR(100),
    ID VARCHAR(100),
    NAME VARCHAR(100),
    CHANGE_DATE VARCHAR(100)
);

CREATE TABLE STG_DIM_SESSIONS (
    STUDENT_ID VARCHAR(100),
    START_TIME VARCHAR(100),
    STUDENT_CLIENT VARCHAR(100)
);

CREATE TABLE STG_DIM_STUDENT_FOLLOW_SUBJECT (
    STUDENT_ID VARCHAR(100),
    SUBJECT_ID VARCHAR(100),
    FOLLOW_DATE VARCHAR(100)
);

CREATE TABLE STG_DIM_SUBJECTS (
    SK_SUBJECTS VARCHAR(100),
    ID VARCHAR(100),
    NAME VARCHAR(100),
    CHANGE_DATE VARCHAR(100)
);

CREATE TABLE STG_DIM_SUBSCRIPTIONS (
    STUDENT_ID VARCHAR(100),
    PAYMENT_DATE VARCHAR(100),
    PLAN_TYPE VARCHAR(100)
);

CREATE TABLE STG_DIM_UNIVERSITIES (
    SK_UNIVERSITIES VARCHAR(100),
    ID VARCHAR(100),
    NAME VARCHAR(100),
    CHANGE_DATE VARCHAR(100)
);