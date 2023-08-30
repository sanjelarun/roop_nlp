from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('App0').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)

def count_positive_values(values):
    result = []
    sc = get_or_create_spark_context()
    values_rdd = sc.parallelize(values)
    
    cnt = values_rdd.filter(lambda val: val > 0).count()
    sc.stop()
    return cnt