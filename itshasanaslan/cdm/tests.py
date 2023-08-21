from django.test import TestCase
from datetime import datetime

# Create your tests here.

s = "2021-05-08 21:00:00"
x = "2021-05-08 22:00:00"

d = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
c = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
print(x > s)
