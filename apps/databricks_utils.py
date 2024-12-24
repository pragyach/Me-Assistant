from pyspark.sql import SparkSession
from delta.tables import DeltaTable

# Initialize Spark session for Databricks
def get_spark_session():
    return SparkSession.builder \
        .appName("MeetingAssistantDatabricks") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:1.2.1") \
        .getOrCreate()

# Save transcription data to Delta Lake
def save_to_delta(data, delta_table_path):
    spark = get_spark_session()
    df = spark.createDataFrame(data)
    df.write.format("delta").mode("append").save(delta_table_path)

# Query transcription data from Delta Lake
def query_delta_table(delta_table_path):
    spark = get_spark_session()
    delta_table = DeltaTable.forPath(spark, delta_table_path)
    return delta_table.toDF()
