import os
os.environ['PYSPARK_PYTHON'] = 'F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\myenv\\Scripts\\python.exe'
from pyspark import SparkContext, SparkConf
def even_counter(numbers):
    evens = []
    for num in numbers:
        if num % 2 == 0:
            evens.append(num)
    return evens

def length_counter(strings):
    lengths = []
    conf = SparkConf().setAppName('MyApp').setMaster('local')
    sc = SparkContext(conf=conf)
    strings_rdd = sc.parallelize(strings)
    lengths = strings_rdd.map(lambda s: len(s)).collect()
    sc.stop()
    return lengths

print(length_counter(["asd","fsd"]))