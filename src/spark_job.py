#built-in
import json

#third-parties
import pyspark
import pyspark.sql.functions as F
from pyspark.sql.session import SparkSession, Row
from pyspark.sql import SQLContext
from pyspark.sql.types import StructField, StructType, StringType, IntegerType
from loguru import logger

#custom
from lake_google_drive_access.google_drive_connect import get_unstructured_file
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

def main():
    records_list = get_unstructured_file()
    schema = StructType([
        StructField('at', StringType(), False),
        StructField('browser', StringType(), False),
        StructField('country', StringType(), False),
        StructField('custom_4', StringType(), False),
        StructField('studentId_clientType', StringType(), False),
        StructField('Page Name', StringType(), False),
        StructField('Last Accessed Url', StringType(), True)
    ])

    df = spark.createDataFrame([], schema)
    for record in records_list:
        df_result = spark.read.json(spark.sparkContext.parallelize([record]))
        if not 'Last Accessed Url' in df.columns:
            df_result.withColumn('Last Accessed Url', F.lit(''))
        df_result = df_result.select('at', 
                    'browser', 
                    'country', 
                    'custom_4', 
                    'studentId_clientType', 
                    'Page Name',
                    'Last Accessed Url').fillna(0)
        df = df.union(df_result)
    df.show()

    #postgres_insert_query = """SELECT * FROM "DM_PASSEI_DIRETO".dim_courses"""
    #dim_courses = dw_get_data(postgres_insert_query)

    schema = StructType([
        StructField('Id', IntegerType(), True),
        StructField('Name', StringType(), True)
    ])

    schema = StructType([
        StructField('at', StringType(), False),
        StructField('browser', StringType(), False),
        StructField('country', StringType(), False),
        StructField('custom_4', StringType(), False),
        StructField('studentId_clientType', StringType(), False),
        StructField('Page Name', StringType(), False)
    ])

    dim_schema = StructType([
        StructField('SK_Courses', IntegerType(), True),
        StructField('Id', IntegerType(), True),
        StructField('Name', StringType(), True),
        StructField('Change_Date', StringType(), True)
    ])

    #df = spark.createDataFrame(json.loads(json.dumps(records_list[0])))
    #df.show()

    #df_dim = spark.createDataFrame(dim_courses, dim_schema)
    #df_dim.show()

    #df = df.join(df_dim, 'Id', how='left')
    #df.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)


  