from pyspark import SparkContext, SparkConf
def even_counter(numbers):
    evens = []
    conf = SparkConf().setAppName('MyApp').setMaster('local')
    sc = SparkContext(conf=conf)
    numbers_rdd = sc.parallelize(numbers)
    evens = numbers_rdd.filter(lambda num: num % 2 == 0).collect()
    sc.stop()
    return evens

def length_counter(strings):
    lengths = []
    conf = SparkConf().setAppName('MyApp').setMaster('local')
    sc = SparkContext(conf=conf)
    strings_rdd = sc.parallelize(strings)
    lengths = strings_rdd.map(lambda s: len(s)).collect()
    sc.stop()
    return lengths