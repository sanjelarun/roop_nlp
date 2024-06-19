from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('App0').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)


def union_and_count(num1, num2):
    result = []
    sc = get_or_create_spark_context()
    num1_rdd = sc.parallelize(num1)
    num2_rdd = sc.parallelize(num2)
    
    result = num1_rdd.union(num2_rdd).count()
    sc.stop()
    return result