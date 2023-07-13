# 23.07.13 부트캠프

- 스키마 detection, 스키마 Evolution => 반정형 데이터 테이블 생성하는 것에 도움을 줌. (프리뷰기능)
  - 스키마 없을때 사용
  - json 파일만 있고, 스키마 없을때.


- Snowflake : Raw 데이터 40TB 압축하면 보통 5TB까지 압축가능. => 스토리지 비용 절약
- Time Travel Data로 Clone 사용 가능.
- speed up : Auto Clustering, Search Optimization, MV, Query Acceleration*

  - Query Acceleration* : 쿼리가 무거울때, 자동으로 컴퓨팅 리소스 조정해서 쿼리 사용,웨어하우스 크기가 작아도 이 기능은 알아서 해줌. 서버리스 기능임. 특정 쿼리 수행 시에만 작동.
- Search Optimization : 범위 쿼리는 효과 없음.
- stream - retention 기간 있음. stream에 있는 데이터를 사용할때 소비한다라고 함.
- task , stream 연계작업을 다이나믹 테이블이 간결하게 해결해
