from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('App0').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)

def sum_even_numbers(numbers):
    result = 0
    sc = get_or_create_spark_context()
    numbers_rdd = sc.parallelize(numbers)
    
    result = numbers_rdd.sum()
    sc.stop()
    return result