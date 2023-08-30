from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('App0').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)

def concatenate_and_lower(strings):
    result = ''
    sc = get_or_create_spark_context()
    strings_rdd = sc.parallelize(strings)
    
    strings_rdd = strings_rdd.map(lambda lower: lower.lower())
    result = strings_rdd.reduce(lambda result, lower: result + lower)
    sc.stop()
    return result