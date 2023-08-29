from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('MyApp').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)

def even_counter(numbers):
    evens = []
    sc = get_or_create_spark_context()
    numbers_rdd = sc.parallelize(numbers)
    evens = numbers_rdd.filter(lambda num: num % 2 == 0).collect()
    sc.stop()
    return evens

def length_counter(strings):
    lengths = []
    sc = get_or_create_spark_context()
    strings_rdd = sc.parallelize(strings)
    lengths = strings_rdd.map(lambda s: len(s)).collect()
    sc.stop()
    return lengths