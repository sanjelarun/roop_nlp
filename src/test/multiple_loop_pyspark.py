from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName('MyApp').setMaster('local')
sc = SparkContext(conf=conf)

# Sample data: two lists of tuples where the first item is the 'key'
orders = [(1, 'Apple'), (2, 'Banana'), (3, 'Cherry')]
order_details = [(1, 'Fruit'), (2, 'Fruit'), (3, 'Berry'), (4, 'Unknown')]

# The result will hold tuples combining matched orders and order details
joined_result = []

orders_rdd = sc.parallelize(orders)
order_details_rdd = sc.parallelize(order_details)
joined_result = orders_rdd.join(order_details_rdd)