# Snowflake Schema Detection

### 1. Snowflake Schema Detection

- 참고 링크 : https://docs.snowflake.com/en/user-guide/data-load-overview#loading-data-from-apache-kafka-topics

#### 1-1. Overview

- 반정형 데이터는 수천 개의 열을 포함할 수 있는데, Snowflake의 Schema Detection은 반정형 데이터에서 자동으로 **열**과 **데이터 타입**을 생성해줌.
- **활용처** :
  - Cloud Storage에 저장되어 있는 데이터를 External Table로 직접 참조할 경우
  - VARIANT 타입으로 되어 있는 반정형 데이터를 loading 할 경우
  - Standard Table or View로 데이터를 loading할 경우

- 데이터 파일에서 Column names, Data types, and ordering of columns를 탐색하여 Column Definition을 함.

#### 1-2. 현재 지원되는 파일 포맷

- Apache Parquet

- Apache Avro

- ORC

  ##### 1-2-1.  현재 Preview 파일 포맷

  - CSV
  - JSON

### 2. Query 구문

#### 2-1. INFER_SCHEMA

- 참고 링크 : https://docs.snowflake.com/en/sql-reference/functions/infer_schema

- 이 구문을 사용하여, 준비된 반정형 데이터 파일 집합에서 **Column Definition**(ex : Column names, Data types, and ordering of columns)를 탐색함.

- **참고** : 이 함수는 Named Stage(Internal or External) 그리고 User Stage만 지원. Table Stage는 지원안함.

  - **Named Stage** : 일반적으로 사용하는 Stage로, 여러 사용자 또는 객체 간에 데이터를 공유,이동하는데 사용.
    - 구문 ex : @MY_STAGE; 

  - **Table Stage** :  특정 Table과 관련된 Stage, 특정 Table에 대한 데이터 이동 작업을 수행할 때 사용.
    - 구문 ex : @%MY_TABLE;

  - **User Stage** : 각각의 사용자에게 생성되는 Stage
    - 구문 ex : @~;

- ```sql
  INFER_SCHEMA(
    LOCATION => '{ internalStage | externalStage }'
    , FILE_FORMAT => '<file_format_name>'
    , FILES => '<file_name>' [ , '<file_name>' ] [ , ... ]
    , IGNORE_CASE => TRUE | FALSE
  )
  
  
  ```

- **Arguments** :

  - | Name        | Description                                                  | 참고                                                         |
    | :---------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
    | LOCATION    | - 파일이 저장된 Stage Name 또는 클라우드 스토리지 경로       | -INFER_SCHEMA 함수가 Stage의 모든 하위 디렉토리에 있는 파일을 검색할 수 있음. |
    | FILES       | - Location에 지정된 Stage나 경로 안의 파일 목록              | - 최대 1000개까지 지정가능. stage에 미리 파일이 준비되어야 함.<br />- 지정된 파일을 찾을 수 없으면 쿼리 중단. |
    | FILE_FORMAT | - 파일 형식에 맞게 사용자가 생성한 파일 포맷.                | - 참고링크 : https://docs.snowflake.com/en/sql-reference/sql/create-file-format |
    | IGNORE_CASE | - 탐지된 열 이름이 대소문자를 구분하는 것으로 처리되는지 여부를 지정. | - default = False => 대소문자 구분<br />- True : 구분(X), 모든 열 이름을 대문자로 함. |

- **Output**

  - | Column Name | Data Type | Description                                                  |
    | :---------- | :-------- | :----------------------------------------------------------- |
    | COLUMN_NAME | TEXT      | Name of a column in the staged files.                        |
    | TYPE        | TEXT      | Data type of the column.                                     |
    | NULLABLE    | BOOLEAN   | 스캔된 데이터 파일 셋에서 각 열의 데이터에 NULL을 저장할 수 있는지 여부를 지정. |
    | EXPRESSION  | TEXT      | - 컬럼의 표현 방식 : `$1:COLUMN_NAME::TYPE` <br />- IGNORE_CASE 을 True로 설정하면 컬럼의 표현방식 :`GET_IGNORE_CASE ($1, COLUMN_NAME)::TYPE`. |
    | FILENAMES   | TEXT      | Names of the files that contain the column.                  |
    | ORDER_ID    | NUMBER    | Column order in the staged files.                            |

##### 2-1-1. INFER_SCHEMA 주의사항

- CSV File 인 경우, File format을 생성할 때, "PARSE_HEADER" 옵션 사용 가능.

  - PARSE_HEADER = True : 데이터 파일의 첫 번째 행 헤더를 열 이름으로 지정. True일 경우, "SKIP_HEADER" 사용 못함.
  - Default는 False로, column 이름을 ex : "c1"로 나타냄. (1은 컬럼 위치)

- CSV 파일을 COPY INTO 할때, "MATCH_BY_COLUMN_NAME" 사용가능.

  - MATCH_BY_COLUMN_NAME : 데이터 파일의 열과 테이블 열을 매칭 시킴.

  - 사용하기 위해선 File format 에서 "RARSE_HEADER = True" 해야 함.

- CSV 파일과 JSON 파일의 경우, File Format에서 현재 "DATE_FORMAT", "TIME_FORMAT" 및 "TIMESTAMP_FORMAT" 파일 형식 옵션이 지원되지 않음.
- JSON 파일의 File Format 옵션에서 "TRIM_SPACE" 옵션 지원되지 않음.
- CSV와 JSON 파일에서 모든 컬럼은 "NULLABLE"로 식별됨.
- JOSN 파일에서 "ex : 1e2" 는 REAL data type으로 추론함.
- 다양한 timestamp data type은 time zone 정보가 없는 Snowflake의 "TIMESTAMP_NTZ" Type으로 추론함. 

#### 2-2.  쿼리 예시

##### 2-2-1. parquet 파일 형식 및 mystage내의 모든 파일 예제

- 참고 : "LOCATION=>'@mystage/geography/cities.parquet' " 이렇게 단일 파일도 가능.

```sql
-- Create a file format that sets the file type as Parquet.
CREATE FILE FORMAT my_parquet_format
  TYPE = parquet;

-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage'
        
      , FILE_FORMAT=>'my_parquet_format'
      )
    );

+-------------+---------+----------+---------------------+--------------------------+----------+
| COLUMN_NAME | TYPE    | NULLABLE | EXPRESSION          | FILENAMES                | ORDER_ID |
|-------------+---------+----------+---------------------+--------------------------|----------+
| continent   | TEXT    | True     | $1:continent::TEXT  | geography/cities.parquet | 0        |
| country     | VARIANT | True     | $1:country::VARIANT | geography/cities.parquet | 1        |
| COUNTRY     | VARIANT | True     | $1:COUNTRY::VARIANT | geography/cities.parquet | 2        |
+-------------+---------+----------+---------------------+--------------------------+----------+

-- 데이터 파일로 부터 Detected Schema를 사용하여 table 생성 예제
CREATE TABLE mytable
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
      FROM TABLE(
        INFER_SCHEMA(
          LOCATION=>'@mystage/',
          FILE_FORMAT=>'my_parquet_format'
        )
      ));
```

##### 2-2-2. CSV파일에 대한 열 정의를 검색하고 MATCH_BY_COUMN_NAME을 사용하여 CSV 파일을 로드하는 예제

```sql
-- Create a file format that sets the file type as CSV.
CREATE FILE FORMAT my_csv_format
  TYPE = csv
  PARSE_HEADER = true;

-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage/csv/'
      , FILE_FORMAT=>'my_csv_format'
      )
    );

+-------------+---------------+----------+---------------------------+--------------------------+----------+
| COLUMN_NAME | TYPE          | NULLABLE | EXPRESSION                | FILENAMES                | ORDER_ID |
|-------------+---------------+----------+---------------------------+--------------------------|----------+
| col_bool    | BOOLEAN       | True     | $1:col_bool::BOOLEAN      | json/schema_A_1.csv      | 0        |
| col_date    | DATE          | True     | $1:col_date::DATE         | json/schema_A_1.csv      | 1        |
| col_ts      | TIMESTAMP_NTZ | True     | $1:col_ts::TIMESTAMP_NTZ  | json/schema_A_1.csv      | 2        |
+-------------+---------------+----------+---------------------------+--------------------------+----------+

-- Load the CSV file using MATCH_BY_COLUMN_NAME.
COPY into mytable from @mystage/csv/' FILE_FORMAT = (FORMAT_NAME= 'my_csv_format') MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;
```

#### 2-2. GENERATE_COLUMN_DESCRIPTION

- 이 함수는 INFER_SCHEMA 함수 결과[ **Column Definition**(ex : Column names, Data types, and ordering of columns)]를 기반으로 사용하여 Table, External Table, View를 수동으로 생성할 때 사용함.
  - "USING TEMPLATE" 절과 함께 CREATE TABLE or CREATE EXTERNAL TABEL 명령어를 실행하여 객체를 생성.

- ```sql
  GENERATE_COLUMN_DESCRIPTION( <expr> , '<string>' )
  ```

##### 2-2-1. Arguments

| Name       | 설명                                                         |
| ---------- | ------------------------------------------------------------ |
| <expr>     | Array로 포맷된 INFER_SCHEMA 함수의 Output , (2-2-3) 참고     |
| '<string>' | 컬럼 list로 부터 생성될 수 있는 객체 ex : 'table', 'external_table', 'view' |

##### 2-2-2. Returns

- '<string>' 에 명시한 객체를 만들 때 입력으로 사용할 수 있는 열 목록들을 반환함. (2-2-3) 참고

##### 2-2-3. 예제 쿼리

- 일반적인 "Table" 생성 예제

```sql
-- Create a file format that sets the file type as Parquet.
CREATE FILE FORMAT my_parquet_format
  TYPE = parquet;

-- Query the GENERATE_COLUMN_DESCRIPTION function.
SELECT GENERATE_COLUMN_DESCRIPTION(ARRAY_AGG(OBJECT_CONSTRUCT(*)), 'table') AS COLUMNS
  FROM TABLE (
    INFER_SCHEMA(
      LOCATION=>'@mystage',
      FILE_FORMAT=>'my_parquet_format'
    )
  );

+--------------------+
| COLUMN_DESCRIPTION |
|--------------------|
| "country" VARIANT, |
| "continent" TEXT   |
+--------------------+

-- GENERATE_COLUMN_DESCRIPTION의 출력을 사용하여 Table의 열을 정의할 수 있음.
CREATE TABLE mytable ("country" VARIANT, "continent" TEXT);
```

- "External Table"생성 예제

```sql
-- Query the GENERATE_COLUMN_DESCRIPTION function.
SELECT GENERATE_COLUMN_DESCRIPTION(ARRAY_AGG(OBJECT_CONSTRUCT(*)), 'external_table') AS COLUMNS
  FROM TABLE (
    INFER_SCHEMA(
      LOCATION=>'@mystage',
      FILE_FORMAT=>'my_parquet_format'
    )
  );

+---------------------------------------------+
| COLUMN_DESCRIPTION                          |
|---------------------------------------------|
| "country" VARIANT AS ($1:country::VARIANT), |
| "continent" TEXT AS ($1:continent::TEXT)    |
+---------------------------------------------+
```

