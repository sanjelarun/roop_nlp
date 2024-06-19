from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('App0').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)


def map_sort(numbers):
    result = []
    sc = get_or_create_spark_context()
    numbers_rdd = sc.parallelize(numbers)
    
    result = numbers_rdd.map(lambda num: num * 2).distinct().sortBy(lambda x: x).collect()
    sc.stop()
    return result