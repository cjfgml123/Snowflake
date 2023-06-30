```sql
USE ROLE ACCOUNTADMIN;
USE WAREHOUSE PENTA_WH;
USE DATABASE PENTA_DB;
USE SCHEMA PARIS_POC_CH;

-- Local File 연동 --
-- dw_comn_cd definition
CREATE OR REPLACE TABLE dw_comn_cd (
  cd_key varchar(30) NOT NULL PRIMARY KEY,
  parent_cd varchar(8) NOT NULL,
  cd varchar(8) NOT NULL,
  lvl smallint NOT NULL,
  sort smallint NOT NULL,
  use_yn tinyint NOT NULL,
  cd_nm varchar(100) DEFAULT NULL,
  cd_nm_eng varchar(100) DEFAULT NULL,
  cd_nm_chn varchar(100) DEFAULT NULL,
  cd_nm_jpn varchar(100) DEFAULT NULL,
  cd_nm_etc varchar(100) DEFAULT NULL,
  rmk varchar(1000) DEFAULT NULL,
  erp_parent_cd varchar(24) DEFAULT NULL,
  erp_table varchar(24) DEFAULT NULL,
  val1 varchar(100) DEFAULT NULL,
  val2 varchar(100) DEFAULT NULL,
  val3 varchar(100) DEFAULT NULL,
  val4 varchar(100) DEFAULT NULL,
  val5 varchar(100) DEFAULT NULL,
  val6 varchar(100) DEFAULT NULL,
  val7 varchar(100) DEFAULT NULL,
  val8 varchar(100) DEFAULT NULL,
  val9 varchar(100) DEFAULT NULL,
  val10 varchar(100) DEFAULT NULL
);

-- Create csv file format to files in stage
CREATE OR REPLACE FILE FORMAT CSV_FORMAT
    TYPE                         = 'CSV',
    FIELD_DELIMITER              = ',',
    RECORD_DELIMITER             = '\n',
    SKIP_HEADER                  = 1,
    FIELD_OPTIONALLY_ENCLOSED_BY = '"',
    ESCAPE                       = 'NONE',
    ESCAPE_UNENCLOSED_FIELD      = 'NONE';

/* Create Stage */
CREATE OR REPLACE STAGE CSV_STAGE
    FILE_FORMAT = CSV_FORMAT;

-- PUT file://C:\Users\User\Desktop\PentaSideProject\dw_comn_cd_paris_test.csv @CSV_STAGE auto_compress=false;

list @CSV_STAGE;

COPY INTO dw_comn_cd FROM @CSV_STAGE; 

select * from dw_comn_cd;

--반정형 데이터 적재 --
create or replace file format json_file_format
TYPE='JSON'
STRIP_OUTER_ARRAY = TRUE --외부 bracket 삭제
;

CREATE OR REPLACE STAGE JSON_STAGE
    FILE_FORMAT = json_file_format;

-- PUT file://C:\Users\User\Desktop\PentaSideProject\films.json @JSON_STAGE auto_compress=false;

CREATE OR REPLACE TABLE JSON_TABLE (
JSON_VARIANT VARIANT
);

COPY INTO JSON_TABLE
FROM @JSON_STAGE/films.json
FILE_FORMAT = json_file_format;

select * from json_table;

-- 반정형 데이터 활용 --
select JSON_VARIANT['id'] from json_table;

select json_variant:title, json_variant:ratings from json_table;

SELECT 
json_variant['id'] as id, 
json_variant['title'] as title, 
json_variant['release_date']::date AS release_date, 
json_variant['actors'][0] as first_actor,
json_variant['ratings']['imdb_rating'] AS IMDB_rating
FROM json_table
WHERE release_date >= date('2000-01-01');


select
    act.value::string as actor, 
    json_variant:id::string as id,
    json_variant:ratings:imdb_rating::float as IMDB_rating,
    json_variant:ratings.metacritic_rating_percentage::float as metacritic_rating_percentage,
    json_variant:release_date::date as release_date,
    json_variant:title::string as title
    from 
    json_table
    ,lateral flatten(input=>json_variant:actors) act;

-- Procedure Test
create or replace procedure chlee_test(PARAM1 string)
    returns string
    language javascript
    execute as OWNER
    as 
    $$
        var param1 = PARAM1;
        var sql_command = "SELECT * FROM " + param1; 
        snowflake.execute({sqlText: sql_command});
        return "Succeeded.";   
    $$;

call chlee_test('JSON_TABLE');


-- Stream Test --




```
