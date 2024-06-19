from pyspark import SparkContext, SparkConf
import os
os.environ['PYSPARK_PYTHON'] = 'F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\myenv\\Scripts\\python.exe'
def get_or_create_spark_context():
    conf = SparkConf().setAppName('App0').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)

def join_list(orders, orders1):
    # The result will hold tuples combining matched orders and order details
    joined_result = []

    sc = get_or_create_spark_context()
    orders_rdd = sc.parallelize(orders)
    orders1_rdd = sc.parallelize(orders1)
    joined_result = orders_rdd.join(orders1_rdd).reduce(lambda a,b: a + (b[0] *))
    sc.stop()
    return joined_result
print(join_list([(1,1),(2,2),(3,3)],[(1,5),(2,6),(3,4)]))