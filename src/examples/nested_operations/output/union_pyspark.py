from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('App0').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)

def combine_two_lists(words1, words2):
    result = []
    sc = get_or_create_spark_context()
    words1_rdd = sc.parallelize(words1)
    words2_rdd = sc.parallelize(words2)
    
    result = words1_rdd.union(words2_rdd).collect()
    sc.stop()
    return result