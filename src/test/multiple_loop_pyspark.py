from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName('MyApp').setMaster('local')
sc = SparkContext(conf=conf)

import os
def total(data):
   squared_data = 0
   data_rdd = sc.parallelize(data)
   squared_data = data_rdd.reduce(lambda squared_data, num: squared_data + (num * 2))
   return squared_data