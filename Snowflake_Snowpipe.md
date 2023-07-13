# Snowflake Snowpipe

- 참고 : https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro

### 1. Snowpipe Overview

- Snowpipe를 사용하면 파일이 stage에 loading과 동시에 파일에서 데이터를 load할 수 있음.
- 참조된 pipe에 정의된 COPY문에 따라 데이터가 load됨.
- JSON 및 Avro와 같은 반정형 데이터를 포함한 모든 데이터 유형을 지원함.

#### 1-1. Snowpipe 작동 방법

##### 1-1-1. Automating Snowpipe using cloud messaging

- 자동화된 데이터 load 방법으로 클라우드 스토리지에 대한 이벤트 알림을 활용하여 로드할 새 데이터 파일이 있으면 Snowpipe에 알림을 보냄.

##### 1-1-2. Calling Snowpipe REST Endpoints

- pipe의 이름과 데이터 파일 이름 목록을 사용하여 REST endpoint를 호출함. pipe 객체에서 참조하는 stage에서 데이터 파일 이름 목록과 일치하는 새 데이터 파일이 발견되면 pipe가 load를 수행.

#### 1-2. Pipe 사용 쿼리

- CREATE PIPE
- ALTER PIPE
- DROP PIPE
- DESCRIBE PIPE
- SHOW PIPES
- GRANT `<privileges>`
- REVOKE `<privileges>`
- SHOW GRANTS

### 1-3 Automating Snowpipe for Amazon S3

- 참고 : https://docs.snowflake.com/en/user-guide/data-load-snowpipe-auto-s3#step-3-create-a-cloud-storage-integration-in-snowflake
- S3 버킷에 대한 Amazon SQS(Simple Queue Service) 알림을 사용하여 Snowpipe 데이터 로드를 자동으로 트리거하는 예.

  - S3 버킷에 충돌하는 이벤트 알림이 있는 경우 "옵션2(참고->Determining the Correct Option)"로 수행, AWS는 동일한 대상 경로에 대해 충돌하는 알림을 생성하는 것을 금지함.
- STORAGE_ALLOWED_LOCATIONS : 필수 파라미터 , STORAGE_BLOCKED_LOCATIONS : 옵션 파라미터

  - 생성한 INTEGRATION을 참조하는 stage가 생성되거나 수정될 때 이 버킷에 대한 액세스를 각각 제한 하거나 차단.
  - `<path> : 버킷의 객체를 세부적으로 제어하는데 사용할 수 있는 선택적 경로.`

```sql
USE ROLE ACCOUNTADMIN;
USE WAREHOUSE PENTA_WH;
USE DATABASE PENTA_DB;
USE SCHEMA PARIS_POC_CH;

-- create table -- pipe 기능 테스트
CREATE OR REPLACE TABLE JSON_TABLE (
JSON_VARIANT VARIANT);

-- create json file format -- 
create or replace file format json_file_format
TYPE='JSON'
STRIP_OUTER_ARRAY = TRUE -- 외부 bracket 삭제 , Loading 할때만 사용.
;

-- INTEGRATION을 create or replace 할 경우, 외부 ID는 AWS의 IAM -> role -> 생성한 role -> 신뢰 관계에서 계속 편집 필요. 
CREATE STORAGE INTEGRATION chlee_intergration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = '<iam_role>' -- AWS에서 IAM -> role 에서 만든 역할의 ARN(AWS에서 조회 가능)
  STORAGE_ALLOWED_LOCATIONS = ('s3://<bucket>/<path>/', 's3://<bucket>/<path>/') -- stage에서 참조할 수 있는 버킷
  STORAGE_BLOCKED_LOCATIONS = ('s3://<bucket>/<path>/', 's3://<bucket>/<path>/'); -- stage에서 참조 할수 없는 버킷

-- STORAGE_AWS_IAM_USER_ARN, STORAGE_AWS_EXTERNAL_ID 두 개의 정보를 AWS -> IAM -> role -> 생성한 role -> 신뢰 관계에서 편집 
-- STORAGE_AWS_EXTERNAL_ID  : The external ID that is needed to establish a trust relationship.
  desc integration chlee_intergration; -- desc : describe

-- stage 생성 --
 CREATE STAGE mystage
  URL = 's3://<bucket>/snowflake/'
  STORAGE_INTEGRATION = chlee_intergration;

-- pipe 생성 --
 -- auto_ingest : 새 데이터를 로드할 준비가 되었을 때 S3 버킷에서 SQS 대기열로 전송된 이벤트 알림을 읽도록 지정함.
  create pipe mypipe auto_ingest=true as
  copy into JSON_TABLE
  from @mystage
  file_format = json_file_format;

-- notification_channel 을 복사 후 AWS 버킷의 이벤트 알림 생성할때 입력 해줘야 함.
-- 이벤트 알림 생성 : 참고에서 Option 1: Creating a New S3 Event Notification to Automate Snowpipe
  show pipes;

  list @mystage;

  select * from JSON_TABLE;
```

### 참고사항

- 각각의 Snowpipe 객체는 load 대기 중인 데이터 파일의 순서를 지정하는 단일 대기열이 있음. Stage에서 새 데이터 파일이 발견되면 Snowpipe는 이를 대기열에 추가함. 일반적으로 먼저 대기열에 들어온 파일을 처리하지만, stage에 파일이 업로드 되는 순서와 동일하다는 보장은 없음.
- Snowpipe & AWS 설정
  - https://medium.com/plumbersofdatascience/how-to-ingest-data-from-s3-to-snowflake-with-snowpipe-7729f94d1797
  - https://docs.snowflake.com/en/user-guide/data-load-snowpipe-auto-s3
