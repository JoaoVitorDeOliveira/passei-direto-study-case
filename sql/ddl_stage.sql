SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `STG_FAT_STUDENTS`;
DROP TABLE IF EXISTS `STG_DIM_COURSES`;
DROP TABLE IF EXISTS `STG_DIM_SESSIONS`;
DROP TABLE IF EXISTS `STG_DIM_STUDENT_FOLLOW_SUBJECT`;
DROP TABLE IF EXISTS `STG_DIM_SUBJECTS`;
DROP TABLE IF EXISTS `STG_DIM_SUBSCRIPTIONS`;
DROP TABLE IF EXISTS `STG_DIM_UNIVERSITIES`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `STG_FAT_STUDENTS` (
    `SK_STUDENT` VARCHAR(100) NOT NULL,
    `ID` VARCHAR(100) NOT NULL,
    `REGISTERED_DATA` VARCHAR(100) NOT NULL,
    `STATE` VARCHAR(100) NOT NULL,
    `CITY` VARCHAR(100) NOT NULL,
    `UNIVERSITY_ID` VARCHAR(100) NOT NULL,
    `COURSE_ID` VARCHAR(100) NOT NULL,
    `SIGNUP_SOURCE` VARCHAR(100) NOT NULL,
    `CHANGE_DATE` VARCHAR(100) NOT NULL
);

CREATE TABLE `STG_DIM_COURSES` (
    `SK_COURSES` VARCHAR(100) NOT NULL,
    `ID` VARCHAR(100) NOT NULL,
    `NAME` VARCHAR(100) NOT NULL,
    `CHANGE_DATE` VARCHAR(100) NOT NULL
);

CREATE TABLE `STG_DIM_SESSIONS` (
    `STUDENT_ID` VARCHAR(100) NOT NULL,
    `START_TIME` VARCHAR(100) NOT NULL,
    `STUDENT_CLIENT` VARCHAR(100) NOT NULL
);

CREATE TABLE `STG_DIM_STUDENT_FOLLOW_SUBJECT` (
    `STUDENT_ID` VARCHAR(100) NOT NULL,
    `SUBJECT_ID` VARCHAR(100) NOT NULL,
    `FOLLOW_DATE` VARCHAR(100) NOT NULL
);

CREATE TABLE `STG_DIM_SUBJECTS` (
    `SK_SUBJECTS` VARCHAR(100) NOT NULL,
    `ID` VARCHAR(100) NOT NULL,
    `NAME` VARCHAR(100) NOT NULL,
    `CHANGE_DATE` VARCHAR(100) NOT NULL
);

CREATE TABLE `STG_DIM_SUBSCRIPTIONS` (
    `STUDENT_ID` VARCHAR(100) NOT NULL,
    `PAYMENT_DATE` VARCHAR(100) NOT NULL,
    `PLAN_TYPE` VARCHAR(100) NOT NULL
);

CREATE TABLE `STG_DIM_UNIVERSITIES` (
    `SK_UNIVERSITIES` VARCHAR(100) NOT NULL,
    `ID` VARCHAR(100) NOT NULL,
    `NAME` VARCHAR(100) NOT NULL,
    `CHANGE_DATE` VARCHAR(100) NOT NULL
);