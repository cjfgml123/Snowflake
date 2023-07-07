# Snowflake View

### 1. Snowflake View

#### 1-1. What is a View?

- 뷰를 사용하면 쿼리 결과를 Table인 것 처럼 볼 수 있음.
- 데이터 결합, 분리, 보호를 포함한 다양한 용도로 사용됨.
- 뷰는 정의한 대로(Create) 쿼리(select)할때 마다 기반이 되는 테이블을 select해서 결과를 보여줌.

#### 2. Materialized View

- 참고 : https://docs.snowflake.com/en/sql-reference/sql/create-materialized-view

- Enterprise Edition 필요.
- select쿼리에서 파생된 사전 계산되고 지속적인 데이터 세트.
- View의 base Table을 쿼리하는 것보다 속도가 빠름. 
- 쿼리가 자주 실행되거나 대용량 데이터 세트에서 실행되는 뷰를 중심으로 작업 가속화. 
- 일반적인 View와의 차이는 쿼리 시 View는 select를 통해서 나오므로 속도가 느리고 구체화뷰는 미리 계산되어서 조회 속도가 빠른건가?

```sql
CREATE [ OR REPLACE ] [ SECURE ] MATERIALIZED VIEW [ IF NOT EXISTS ] <name>
  [ COPY GRANTS ]
  ( <column_list> )
  [ <col1> [ WITH ] MASKING POLICY <policy_name> [ USING ( <col1> , <cond_col1> , ... ) ]
           [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ , <col2> [ ... ] ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ COMMENT = '<string_literal>' ]
  [ CLUSTER BY ( <expr1> [, <expr2> ... ] ) ]
  AS <select_statement>
```

```sql
CREATE OR REPLACE MATERIALIZED VIEW MV1 AS
SELECT COL1, COL2 FROM T1;

ALTER MATERIALIZED VIEW MV1 SUSPEND;

ALTER MATERIALIZED VIEW MV1 RESUME;

SHOW MATERIALIZED VIEWS LIKE 'MV1%';
```

##### 2-1. 유용할점 및 주의사항

- 쿼리결과가 View 정의된 테이블에 비해 적은 수의 행 및 열을 사용할때 사용.
- 반구조 데이터를 분석할때 사용
- 계산하는데 시간이 오래 걸리는 집계있을때 사용.
- View가 정의된 테이블이 자주 변경되지 않을때 사용.

- 백그라운드에서 자동으로 구체화된 View가 업데이트 됨.

##### 2-2. Example

```sql
-- Example of a materialized view with a range filter
create materialized view v1 as
    select * from table1 where column_1 between 100 and 400;
```

