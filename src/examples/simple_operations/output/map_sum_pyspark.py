from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('App0').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)

def square_and_sum(numbers):
    result = []
    s = 0
    sc = get_or_create_spark_context()
    numbers_rdd = sc.parallelize(numbers)
    
    result = numbers_rdd.map(lambda num: num ** 2)
    s = result.sum()
    sc.stop()
    return s