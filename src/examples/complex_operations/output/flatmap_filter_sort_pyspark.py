from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('App0').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)

def flatted_filter(list_of_lists):
    result = []
    sc = get_or_create_spark_context()
    list_of_lists_rdd = sc.parallelize(list_of_lists)
    
    result = list_of_lists_rdd.flatMap(lambda x: x).filter(lambda num: num > 10).sortBy(lambda x: x).collect()
    sc.stop()
    return result