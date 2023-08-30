from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('App2').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)


def total(data):
   total = 0
   sc = get_or_create_spark_context()
   data_rdd = sc.parallelize(data)
   
   total = data_rdd.sum()
   sc.stop()
   return total
import pytest


import os
os.environ['PYSPARK_PYTHON'] = 'F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\myenv\\Scripts\\python.exe'


def test_total_single_element():
    data = [5]
    expected_result = 5
    assert total(data) == expected_result, f"Expected {expected_result} for input {data}, but got {total(data)}"

def test_total_multiple_elements():
    data = [1, 2, 3, 4, 5]
    expected_result = sum(data)
    assert total(data) == expected_result, f"Expected {expected_result} for input {data}, but got {total(data)}"

def test_total_negative_numbers():
    data = [-1, -2, -3]
    expected_result = sum(data)
    assert total(data) == expected_result, f"Expected {expected_result} for input {data}, but got {total(data)}"

def test_total_mixed_numbers():
    data = [-1, 2, -3, 4, -5]
    expected_result = sum(data)
    assert total(data) == expected_result, f"Expected {expected_result} for input {data}, but got {total(data)}"

if __name__ == "__main__":
    pytest.main([__file__])