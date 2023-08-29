from pyspark import SparkContext, SparkConf

def total(data):
   squared_data = 0
   conf = SparkConf().setAppName('MyApp').setMaster('local')
   sc = SparkContext(conf=conf)
   data_rdd = sc.parallelize(data)
   None = data_rdd.map(lambda squared_data: squared_data + (num * 2)).collect()
   sc.stop()
   return squared_data