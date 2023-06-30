# Snowflake Semi-structured Data 

### 1. Snowflake Semi-structured Data JSON

#### 1-1. JSON Data Loading

```sql
-- 1. FILE FORMAT 생성 후 STAGE 생성
CREATE FILE FORMAT <name>
TYPE = { JSON | AVRO | ORC | PARQUET | XML }
[<FORMAT OPTIONS>];

-- 2. PUT 명령어로 STAGE에 파일 적재
```

##### 1-1-1. JSON File Format options

| Option            | Details                                                      |
| ----------------- | ------------------------------------------------------------ |
| DATE_FORMAT       |                                                              |
| TIME_FORMAT       |                                                              |
| COMPRESSION       |                                                              |
| ALLOW_DUPLICATE   |                                                              |
| STRIP_OUTER_ARRAY | Loading할때만 사용되며, TRUE일 경우 JSON Parser가 외부 bracket을 삭제함. |
| STRIP_NULL_VALUES |                                                              |

