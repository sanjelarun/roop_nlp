from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName('MyApp').setMaster('local')
sc = SparkContext(conf=conf)

def even_counter(numbers):
    evens = []
    numbers_rdd = sc.parallelize(numbers)
    evens = numbers_rdd.filter(lambda num: num % 2 == 0)
    return evens

def length_counter(strings):
    lengths = []
    strings_rdd = sc.parallelize(strings)
    lengths = strings_rdd.map(lambda s: len(s))
    return lengths