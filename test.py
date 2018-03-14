try:
    res = 1/0
except Exception as e:
    print('str(Exception):\t', str(Exception))
    print('str(e):\t\t', str(e))
else:
    print(res)

