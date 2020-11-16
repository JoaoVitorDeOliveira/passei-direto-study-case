from datetime import datetime

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from get_conection import bd_conection_util

dag_params = {
    'dag_id': 'Passei Direto',
    'start_date': datetime(2019, 10, 7)
}

path_variable = Variable.get('load_dimensao_cliente')
now = datetime.now()


with DAG('Passei_Direto',
	 default_args=dag_params,
	 schedule_interval='@daily',
     template_searchpath=path_variable,
	 catchup=False) as dag:

    Start = BashOperator(
        task_id='Start',
        bash_command="echo 'Begin Extraction {}'".format(now.strftime("%H:%M:%S")))

    Extract_Courses_To_Stage = BashOperator(
        task_id='Extract_Courses_To_Stage',
        bash_command='cd /app/src && python extract_courses_to_stage.py')

    Extract_Session_To_Stage = BashOperator(
        task_id='Extract_Session_To_Stage',
        bash_command='cd /app/src && python extract_session_to_stage.py')

    Extract_SFS_To_Stage = BashOperator(
        task_id='Extract_SFS_To_Stage',
        bash_command='cd /app/src && python extract_sfs_to_stage.py')

    Extract_Student_To_Stage = BashOperator(
        task_id='Extract_Student_To_Stage',
        bash_command='cd /app/src && python extract_students_to_stage.py')

    Extract_Subject_To_Stage = BashOperator(
        task_id='Extract_Subject_To_Stage',
        bash_command='cd /app/src && python extract_subject_to_stage.py')

    Extract_Subscription_To_Stage = BashOperator(
        task_id='Extract_Subscription_To_Stage',
        bash_command='cd /app/src && python extract_subscription_to_stage.py')

    Extract_Universities_To_Stage = BashOperator(
        task_id='Extract_Universities_To_Stage',
        bash_command='cd /app/src && python extract_universities_to_stage.py')
    
    #FYI: I decided to make more generic possible
    #Load_Dim_Courses = PostgresOperator(
    #    task_id='Load_Stage_To_Dim_Course',
    #    sql='dim_courses_load.sql',
    #    postgres_conn_id=bd_conection_util.get_db_conection(),
    #    database=bd_conection_util.get_db_name(),
    #    autocommit=True
	#)

    Load_Dim_Courses = BashOperator(
        task_id='Load_Stage_To_Dim_Course',
        bash_command='cd /app/src && python load_dim.py dim_courses_load.sql')

    Load_Dim_Sessions = BashOperator(
        task_id='Load_Stage_To_Dim_Sessions',
        bash_command='cd /app/src && python load_dim.py dim_sessions_load.sql')

    Load_Dim_Subjects = BashOperator(
        task_id='Load_Stage_To_Dim_Subjects',
        bash_command='cd /app/src && python load_dim.py dim_subjects_load.sql')

    Load_Dim_Subscriptions = BashOperator(
        task_id='Load_Stage_To_Dim_Subscriptions',
        bash_command='cd /app/src && python load_dim.py dim_subscriptions_load.sql')


    Load_Dim_Universities = BashOperator(
        task_id='Load_Stage_To_Dim_Universities',
        bash_command='cd /app/src && python load_dim.py dim_universities_load.sql')

    Load_Dim_SFS = BashOperator(
        task_id='Load_Stage_To_Dim_SFS',
        bash_command='cd /app/src && python load_dim.py dim_sfs_load.sql')

    Load_Fat_Students = BashOperator(
        task_id='Load_Stage_To_Fat_Students',
        bash_command='cd /app/src && python load_dim.py fat_students_load.sql')

    End = BashOperator(
        task_id='End',
        bash_command="echo 'Now is {}, Time spent {}'".format(datetime.now().strftime("%H:%M:%S"), datetime.now() - now))



Start >> [ Extract_SFS_To_Stage, 
            Extract_Session_To_Stage, 
            Extract_Courses_To_Stage, 
            Extract_Subject_To_Stage,
            Extract_Student_To_Stage,
            Extract_Universities_To_Stage,
            Extract_Subscription_To_Stage] >> Load_Dim_Courses \
>> Load_Dim_Sessions \
>> Load_Dim_Subjects \
>> Load_Dim_Subscriptions \
>> Load_Dim_Universities \
>> Load_Dim_SFS \
>> Load_Fat_Students \
>> End