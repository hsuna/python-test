# def log(func):
#     def wrapper(*args, **kw):
#         print('call %s():' % func.__name__)
#         return func(*args, **kw)
#     return wrapper

# def now():
#     print('2018-05-14')

# now()

import os

path = os.environ.get('PATH')
print(path)
