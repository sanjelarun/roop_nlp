from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('App0').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)

def join_list(orders, order_details):
    # The result will hold tuples combining matched orders and order details
    joined_result = []

    sc = get_or_create_spark_context()
    orders_rdd = sc.parallelize(orders)
    order_details_rdd = sc.parallelize(order_details)
    joined_result = orders_rdd.join(order_details_rdd).collect()
    sc.stop()
    return joined_result