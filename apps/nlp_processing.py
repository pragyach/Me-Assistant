from transformers import pipeline
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer

# Sentiment analysis using Hugging Face
def sentiment_analysis(transcription):
    sentiment_pipeline = pipeline("sentiment-analysis")
    return sentiment_pipeline(transcription)

# Topic extraction using Spark NLP
def topic_extraction(data):
    spark = SparkSession.builder.appName("TopicExtraction").getOrCreate()
    df = spark.createDataFrame(data)

    tokenizer = Tokenizer(inputCol="transcription", outputCol="words")
    tokenized = tokenizer.transform(df)

    # Example: Return tokenized output for topics
    return tokenized.select("meeting_id", "words").collect()
