# Snowflake Semi-structured Data Types

### 1. Snowflake Semi-structured Data Types

- 종류 : JSON, Avro, ORC, Parquet, XML
- 참고 : https://docs.snowflake.com/en/sql-reference/data-types-semistructured

| 타입    | 설명                                                                                 |
| ------- | ------------------------------------------------------------------------------------ |
| VARIANT |                                                                                      |
| ARRAY   | 일반적인 프로그래밍 언어에서의 배열을 생각하면 됨.                                   |
| OBJECT  | python의 dict형식과 같음. key : varchar type , value : variant or 다른 일반적인 Type |

#### 1-1. VARIANT

- ONJECT, ARRAY를 포함한 모든 유형의 값을 저장할 수 있음.
- 최대 길이는 16MB.

##### 1-1-1. VARIANT casting

- CAST, TO_VARIANT 함수 사용
- "::" operator 사용

```sql
CREATE TABLE varia (float1 FLOAT, v VARIANT, float2 FLOAT);
INSERT INTO varia (float1, v, float2) VALUES (1.23, NULL, NULL);

UPDATE varia SET v = TO_VARIANT(float1);  -- float -> variant
UPDATE varia SET float2 = v::FLOAT;       -- variant -> float.
```

- PARSE_JSON("json_string") : json형식의 문자열을 json타입으로 변환해주는 함수

```sql
INSERT INTO varia (v) SELECT TO_VARIANT(PARSE_JSON('{"key3": "value3", "key4": "value4"}'))
```

#### 1-2. OBJECT

- key-value 형식으로 python의 Dictionary Type과 같음.
- key는 VARCHAR Type , value는 VARIANT를 포함한 float, int 등 가능
- key는 빈 문자열일 수 없으며 NULL 일 수 없음.
- 최대 길이는 16MB
- OBJECT 에는 semi-structured data가 포함될 수 있음.

```sql
-- VARCHAR 타입과 INT 타입을 VARIANT 타입으로 캐스팅하여 조회하는 예제
SELECT OBJECT_CONSTRUCT(
    'name', 'Jones'::VARIANT,
    'age',  42::VARIANT
    );
```

##### 1-2-1. OBJECT Constants

- 고정 데이터 값을 만드는 것.
- "{}"로 구분 되거나 OBJECT_CONSTRUCT 함수를 사용.

```sql
UPDATE my_table SET my_object = { 'Alberta': 'Edmonton' , 'Manitoba': 'Winnipeg' };

UPDATE my_table SET my_object = OBJECT_CONSTRUCT('Alberta', 'Edmonton', 'Manitoba', 'Winnipeg');
```

##### 1-2-2. Accessing Elements of an OBJECT by Key

- "[]" or ":" 으로 접근

```sql
SELECT object_column['thirteen'],
       object_column:thirteen
    FROM object_example;
'''
+---------------------------+------------------------+
| OBJECT_COLUMN['THIRTEEN'] | OBJECT_COLUMN:THIRTEEN |
|---------------------------+------------------------|
| 13                        | 13                     |
+---------------------------+------------------------+
'''
```

##### 1-2-3. OBJECT Data Insert

- OBJECT 상수 Insert Example

```sql
INSERT INTO object_example (object_column)
    SELECT OBJECT_CONSTRUCT('thirteen', 13::VARIANT, 'zero', 0::VARIANT);
  
INSERT INTO object_example (object_column)
    SELECT { 'thirteen': 13::VARIANT, 'zero': 0::VARIANT };   
```

#### 1-3. ARRAY

- 배열의 각 값은 VARIANT Type(VARIANT 타입은 다른 data type도 포함됨.)
- Snowflake에서 배열은 요수의 수를 미리 지정하지 않음. 현재 고정 크기 배열을 지원하지 않음.
- ARRAY_APPEND()와 같은 작업을 기반으로 동적으로 확장 가능.
- NULL 값을 포함할 수 있음.
- 최대 길이는 16MB.

##### 1-3-1. ARRAY Constants

- ARRAY 상수는 "[]" , ARRAY_CONSTRUCT() 로 사용.

```sql
UPDATE my_table SET my_array = [ 1, 2 ];

UPDATE my_table SET my_array = ARRAY_CONSTRUCT(1, 2);
```

##### 1-3-2. Accessing Elements of an ARRAY by Index or by Slice

- array 첫 번째 요소는 0으로 시작.

```sql
select my_array_column[2] from my_table;

-- 중첩 array 접근
select my_array_column[0][0] from my_table;
```

- array 끝을 넘는 요소에 접근하면 NULL이 반환.
- array_slice()사용으로 접근하기

  - ```sql
    select array_slice(my_array_column, 5, 10) from my_table;
    ```

##### 1-3-3. Array Insert Example

```sql
INSERT INTO array_example (array_column)
    SELECT ARRAY_CONSTRUCT(12, 'twelve', NULL);
  
INSERT INTO array_example (array_column)
    SELECT [ 12, 'twelve', NULL ];
```

- ARRAY_INSERT() 예제 : ARRAY_INSERT( `<array>` , `<pos>` , <new_element> )

  - ```sql
    SELECT ARRAY_INSERT(ARRAY_CONSTRUCT(0,1,2,3),2,'hello');
    +--------------------------------------------------+
    | ARRAY_INSERT(ARRAY_CONSTRUCT(0,1,2,3),2,'HELLO') |
    |--------------------------------------------------|
    | [                                                |
    |   0,                                             |
    |   1,                                             |
    |   "hello",                                       |
    |   2,                                             |
    |   3                                              |
    | ]                                                |
    +--------------------------------------------------+
    ```
  - 해당 위치에 기존의 값이 있으면 뒤로 밀려남.

#### 1-4. 주의사항

- 테이블의 열이름은 대소문자를 구분하지 않지만, 데이터에 직접 접근할때는 대소문자를 구분함.

```sql
src:salesperson.name -- 1.
 
SRC:salesperson.name -- 2.

SRC:Salesperson.Name -- 3. 1,2와 다름. 1,2는 결과 같음.
```

- Bracket Notation 방식으로 접근 가능
- ```sql
  SELECT src['salesperson']['name']
      FROM car_sales
      ORDER BY 1;
  +----------------------------+
  | SRC['SALESPERSON']['NAME'] |
  |----------------------------|
  | "Frank Beasley"            |
  | "Greg Northrup"            |
  +----------------------------+
  ```

#### 1-5. FLATTEN() 사용하기

- 참고 : https://docs.snowflake.com/en/user-guide/querying-semistructured
- VARIANT, OBJECT, ARRAY 컬럼의 데이터를 여러 행으로 평평하게 만들어줌.
- LATERAL VIEW 를 생성해주는 함수 : from절에 있는 테이블을 참조
- ```sql
  -- https://docs.snowflake.com/en/sql-reference/functions/flatten
  FLATTEN( INPUT => <expr> [ , PATH => <constant_expr> ]
                           [ , OUTER => TRUE | FALSE ]
                           [ , RECURSIVE => TRUE | FALSE ]
                           [ , MODE => 'OBJECT' | 'ARRAY' | 'BOTH' ] )

  SELECT
    value:name::string as "Customer Name",
    value:address::string as "Address"
    FROM
      car_sales
    , LATERAL FLATTEN(INPUT => SRC:customer);

  +--------------------+-------------------+
  | Customer Name      | Address           |
  |--------------------+-------------------|
  | Joyce Ridgely      | San Francisco, CA |
  | Bradley Greenbloom | New York, NY      |
  +--------------------+-------------------+
  ```

  - Arguments
    - Required :
      - INPUT => `<expr>` : 식은 VARIANT, OBJECT, ARARY
    - Optional :
      - PATH => <constant_expr>: flattened 해야 하는 VARIANT 데이터 구조 내의 요소에 대한 경로.
        - default : Zero-length string(empty path)
      - OUTER => TRUE | FALSE :
        - default : FALSE
      - RECURSIVE => RUE | FALSE: FALSE인 경우 PATH에서 참조하는 요소만 시행. TRUE인 경우 모든 하위 요소에 대해 재귀적으로 확장 수행.
        - default : FALSE
      - MODE => 'OBJECT' | 'ARRAY' | 'BOTH': 둘 다 평평하게 만들 것인지 여부 지정
        - default : BOTH
  - Output
    - 참고 : https://docs.snowflake.com/en/sql-reference/functions/flatten 예제 보면 이해 쉬움.
    - SEQ : 입력 record와 연관된 고유 시퀀스 번호. 공백없음. 특정 방식으로 순서 지정되지 않음.
    - KEY : 분해된 값에 대한 KEY
    - PATH : flatten 해야 하는 데이터 구조 내의 요소에 대한 경로
    - INDEX : array인 경우 요소에 대한 index이며, array 아니면 NULL.
    - VALUE : flatten 된 array/object의 element의 값.
    - THIS : The element being flattened (useful in recursive flattening).

##### 1-5-1. Nested Arrays FLATTEN 함수 사용

```json
"vehicle" : [
     {"make": "Honda", "model": "Civic", "year": "2017", "price": "20275", "extras":["ext warranty", "paint protection"]}
   ]
```

- "vehicle"을 먼저 FLATTEN하고 "extras"를 다시 FLATTEN 한다.

```sql
SELECT
  vm.value:make::string as make,
  vm.value:model::string as model,
  ve.value::string as "Extras Purchased"
  FROM
    car_sales
    , LATERAL FLATTEN(INPUT => SRC:vehicle) vm
    , LATERAL FLATTEN(INPUT => vm.value:extras) ve
  ORDER BY make, model, "Extras Purchased";
+--------+-------+-------------------+
| MAKE   | MODEL | Extras Purchased  |
|--------+-------+-------------------|
| Honda  | Civic | ext warranty      |
| Honda  | Civic | paint protection  |
| Toyota | Camry | ext warranty      |
| Toyota | Camry | fabric protection |
| Toyota | Camry | rust proofing     |
+--------+-------+-------------------+
```

#### 1-6. GET 함수로 값 추출하기

- 참고 : https://docs.snowflake.com/en/sql-reference/functions/get
- 첫번째 인수로 VARIANT, OBJECT, ARRAY 값을 받고 두번째 인수로 조회할 위치를 넣는다.
- ARARY_SIZE함수를 이용하여 VARIANT열에서 각 배열의 마지막 요소를 계산하고 추출한다.

```sql
-- 1. ARRAY (or VARIANT containing an ARRAY)
GET( <array> , <index> )
GET( <variant> , <index> )

-- 2. OBJECT (or VARIANT containing an OBJECT)
GET( <object> , <field_name> )
GET( <variant> , <field_name> )

SELECT *, GET(v, ARRAY_SIZE(v)-1) FROM colors;
```

#### 1-7. GET_PATH로 값 추출하기

- 둘 다 동일한 결과 출력.

```sql
SELECT GET_PATH(src, 'vehicle[0].make') FROM car_sales;

SELECT src:vehicle[0].make FROM car_sales;
```
