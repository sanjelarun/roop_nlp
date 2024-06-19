from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('App0').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)


def total(data):
   total = 0
   sc = get_or_create_spark_context()
   data_rdd = sc.parallelize(data)
   
   total = data_rdd.sum()
   sc.stop()
   return total