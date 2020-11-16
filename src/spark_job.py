#built-in
import json
import os

#third-parties
import pyspark
import pyspark.sql.functions as F
from pyspark.sql.session import SparkSession, Row
from pyspark.sql import SQLContext
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, LongType, BooleanType 
from loguru import logger

#custom
from lake_google_drive_access.google_drive_connect import get_unstructured_file, send_files
from database_access.postgres_connect import get_database_credentials

spark = SparkSession.builder \
    .appName("Students Behavior") \
    .getOrCreate()

database = 'jdbc:postgresql://ec2-54-91-178-234.compute-1.amazonaws.com'
username = 'hkmwrxkewkhzrh'
password = 'a8f37ea49b38f2d3d07d853b15ed59e0a7b5edaea657c3450c970dd8b9038a57'
driver_postgress = 'postgresql-42.2.18.jar'

def execute_query(server, query, driver):
    df = spark.read.format('jdbc') \
        .option("driver", "org.postgresql.Driver") \
        .option('url', server) \
        .option('dbtable', query) \
        .option('user', username) \
        .option('password', password) \
        .load()

    return df

def get_students():
    query = """
        SELECT *
        FROM DM_PASSEI_DIRETO.fat_students
    """
    resultset = execute_query(database, query, driver_postgress)
    return resultset

def dw_get_data(query):
    connection = get_database_credentials()
    cursor = connection.cursor()

    cursor.execute(query)
    courses = cursor.fetchall()

    return courses

@F.udf
def clean_studentId(str_id):
    split_id = str_id.split('@')
    return split_id[0]


@logger.catch
def main():
    get_unstructured_file()
    logger.success('Downloaded Files')

    schema = StructType([
        StructField('Last Accessed Url',StringType(),True)
        ,StructField('Page Category',StringType(),True)
        ,StructField('Page Category 1',StringType(),True)
        ,StructField('Page Category 2',StringType(),True)
        ,StructField('Page Category 3',StringType(),True)
        ,StructField('Page Name',StringType(),True)
        ,StructField('at',StringType(),True)
        ,StructField('browser',StringType(),True)
        ,StructField('carrier',StringType(),True)
        ,StructField('city_name',StringType(),True)
        ,StructField('clv_total',LongType(),True)
        ,StructField('country',StringType(),True)
        ,StructField('custom_1',StringType(),True)
        ,StructField('custom_2',StringType(),True)
        ,StructField('custom_3',StringType(),True)
        ,StructField('custom_4',StringType(),True)
        ,StructField('device_new',BooleanType(),True)
        ,StructField('first-accessed-page',StringType(),True)
        ,StructField('install_uuid',StringType(),True)
        ,StructField('language',StringType(),True)
        ,StructField('library_ver',StringType(),True)
        ,StructField('marketing_campaign',StringType(),True)
        ,StructField('marketing_medium',StringType(),True)
        ,StructField('marketing_source',StringType(),True)
        ,StructField('model',StringType(),True)
        ,StructField('name',StringType(),True)
        ,StructField('nth',LongType(),True)
        ,StructField('os_ver',StringType(),True)
        ,StructField('platform',StringType(),True)
        ,StructField('region',StringType(),True)
        ,StructField('session_uuid',StringType(),True)
        ,StructField('studentId_clientType',StringType(),True)
        ,StructField('type',StringType(),True)
        ,StructField('user_type',StringType(),True)
        ,StructField('uuid',StringType(),True)
    ])

    logger.debug('Creating DataFrame...')
    df = spark.read.schema(schema).json('*.json')
    logger.success('DataFrame created with {} rows'.format(df.count()))

    df = df.select('at', 
                'browser', 
                'country', 
                'custom_4', 
                'studentId_clientType', 
                'Page Name',
                'Last Accessed Url') \
            .filter(df['studentId_clientType'].isNotNull())

    df_country = df.select(df.country) \
        .filter(df.country != 'br') \
        .groupBy('country').count() 
    #df_country.repartition(1).write.format('csv').mode('overwrite').option('header', 'true').save('country')
    


    df_users = df.filter(df.custom_4.isNotNull()) \
                .select(df.custom_4) \
                .groupBy(df.custom_4).count()
    #df_users.repartition(1).write.format('csv').mode('overwrite').option('header', 'true').save('user.csv')
    

    df_result = df.withColumn('id', clean_studentId(df['studentId_clientType']))
    df_result = df_result.drop('studentId_clientType')
   
    query = """SELECT fat.id, state, city, cou.name course
                                FROM "DM_PASSEI_DIRETO".fat_students fat
                                INNER JOIN "DM_PASSEI_DIRETO".dim_courses cou
                                ON fat.course_id = cou.id
                                INNER JOIN "DM_PASSEI_DIRETO".dim_sessions ds 
                                ON fat.id = ds.student_id 
                                WHERE CAST(ds.start_time as VARCHAR) LIKE '2017-11-16%'"""
    students = dw_get_data(query)

    students_schema = StructType([
        StructField('id', StringType(), True),
        StructField('state', StringType(), True),
        StructField('city', StringType(), True),
        StructField('course', StringType(), True)
    ])

    df_dim = spark.createDataFrame(students, students_schema)

    df_result = df_result.join(df_dim, 'id', how='inner').distinct()
    #df_result.repartition(1).write.format('csv').mode('overwrite').option('header', 'true').save('full.csv')
    
    df_country.toPandas().to_csv('country.csv')
    df_users.toPandas().to_csv('users.csv')
    df_result.toPandas().to_csv('full.csv')
    send_files('*.csv')

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(e)
    finally:
        os.system('rm -r *.json')
        logger.success('Deleted json files')

        os.system('rm -r *.csv')
        logger.success('Deleted csv files')

        os.system('cp ./lake_google_drive_access/client_secrets.json .')

  