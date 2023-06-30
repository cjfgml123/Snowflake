# Snowflake DML

### 1. Snowflake Merge

- 두 번째 테이블이나 하위 쿼리에 있는 값을 기준으로 테이블에 삽입, 업데이트, 삭제 함.
- 두 테이블을 어떠한 조건으로 비교하여 target Table에 조건에 맞으면 "update" or "delete" 하고 조건에 맞지 않으면 "insert"를 한다.

```sql
-- target_table : update되거나 insert되는 Table
-- source : target table과 결합할 table or subquery
-- join_expr : target table과 source를 결합할 식을 지정.
MERGE INTO <target_table>
            USING <source>   
                 ON (join condition)                                     -- WHERE절에 조건 쓰듯이
            WHEN MATCHED THEN                                   -- ON 이하의 조건에 해당하는 데이터가 있는 경우 
                     UPDATE SET col1 = val1[, ...]                -- UPDATE 실행
            WHEN NOT MATCHED THEN                           -- ON 이하의 조건에 해당하는 데이터가 없는 경우
                     INSERT (column lists) VALUES (values);  -- INSERT 실행
```

```sql
MERGE INTO members m
  USING (
    SELECT id, dt
    FROM signup s
    WHERE DATEDIFF(day, '2018-08-15'::date, s.dt::DATE) < -30) s
    ON m.id = s.id
  WHEN MATCHED THEN UPDATE SET m.fee = 90;
```
