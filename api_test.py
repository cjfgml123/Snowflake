import requests

_serviceKey = "L5+wEznc4lc6qqxMMXyaUImi6Xg7yfcAUrVd4WYfEFqH9xyu25dllgJ0rzXOAC3CDh4nl0ksjRhR722YvG25qQ=="
_dataType = "JSON"
_startDate = "20230620"
_endDate = "20230621"
url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
params ={'serviceKey' : _serviceKey, 'pageNo' : '1', 'numOfRows' : '10',
         'dataType' : _dataType, 'dataCd' : 'ASOS', 'dateCd' : 'DAY', 
         'startDt' : _startDate, 'endDt' : _endDate, 'stnIds' : '108' }

response = requests.get(url, params=params)
print(response.text)