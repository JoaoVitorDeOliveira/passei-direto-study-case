#!/bin/bash

echo "Extract course.json to stage"
python extract_courses_to_stage.py

echo "Extract session.json to stage"
python extract_session_to_stage.py

echo "Extract student_session.json to stage"
python extract_sfs_to_stage.py

echo "Extract students.json to stage"
python extract_students_to_stage.py

echo "Extract subject.json to stage"
python extract_subject_to_stage.py

echo "Extract subscription.json to stage"
python extract_subscription_to_stage.py

echo "Extract universities.json to stage"
python extract_universities_to_stage.py

echo "Tranform data and Load to Dimensional"

echo "Load dim_courses_load.sql"
python load_dim.py dim_courses_load.sql


echo "Load dim_sessions_load.sql"
python load_dim.py dim_sessions_load.sql


echo "Load dim_subjects_load.sql"
python load_dim.py dim_subjects_load.sql


echo "Load dim_subscriptions_load.sql"
python load_dim.py dim_subscriptions_load.sql

echo "Load dim_universities_load.sql"
python load_dim.py dim_universities_load.sql


echo "Load dim_sfs_load.sql"
python load_dim.py dim_sfs_load.sql


echo "Load fat_students_load.sql"
python load_dim.py fat_students_load.sql

echo "Start Spark Job"
 /mnt/c/Users/Joao/spark-3.0.0-preview2-bin-hadoop2.7/bin/spark-submit spark_job.py