import cubo
import datetime
import pathlib
import numpy as np

def get_time_value(time_value):
    date_time = datetime.datetime.utcfromtimestamp(time_value / 1e9)  
    return date_time.strftime('%Y-%m-%d %H:%M:%S')

