# 1. Snowflake Dynamic Table

- 참고 : https://docs.snowflake.com/en/user-guide/dynamic-tables-about#a-simple-example

### 1-1. Dynamic Table Overview

- 선언적 데이터 변환 파이프라인의 구성요소로 사용할 데이터를 안정적이고 비용 효율적이며 자동화된 방식으로 변환할 수 있음.
- 데이터 변환 단계를 일련의 작업으로 정의하고 스케줄링을 모니터링해야 하는 대신 Dynamic Table을 사용하여 단순화할 수 있음.

### 1-2. Dynamic Table 정의

- 사용자가 지정한 쿼리의 결과를 구체화하는 테이블로 별도의 대상 테이블을 생성하고 해당 테이블의 데이터를 변환 및 업데이트하는 코드를 작성하는 대신 대상 테이블을 Dynamic Table로 정의하고 변환을 수행하는 SQL문을 지정할 수 있음.
- 참고 및 주의사항
  - Dynamic Table은 지정된 쿼리에 의해 완전히 결정되므로 DML을 통해 데이터 변경 불가(삽입, 업데이트 or 삭제) 못함.
  - Dynamic Table이 있는 Database는 Replicating이 불가함. 하려면 DB를 복제하기 전에 DB의 Dynamic Table을 삭제해야 함.

### 1-3. Dynamic Table Example

- 기존 stream & Task SQL과 비교 : https://docs.snowflake.com/en/user-guide/dynamic-tables-about#a-simple-example
- raw 테이블에 json 데이터가 들어올때 Dynamic Table은 TARGET_LAG 주기로 데이터 최신상태 유지.

```sql
-- Create a landing table to store
-- raw JSON data.
CREATE OR REPLACE TABLE raw
(var VARIANT);

-- Create a dynamic table containing the
-- names of office visitors from
-- the raw data.
-- Try to keep the data up to date within
-- 1 minute of real time.
CREATE OR REPLACE DYNAMIC TABLE names
TARGET_LAG = '1 minute'
WAREHOUSE = mywh
AS
SELECT var:id::int id, var:fname::string first_name,
var:lname::string last_name FROM raw;
```

### 1-4. Dynamic Table 을 쓰면 좋은 Case

- stream & task 의 복잡한 작업 필요 없음.
- 여러 base 테이블을 사용하여 쿼리를 구체화 할 경우.
- 세분화된 새로 고침 일정 제어가 필요하지 않음.

### 1-5. Dynamic Table 작동방식

![dynamic_table](./image/dynamic_table.png)
