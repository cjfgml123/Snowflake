# Snowflake Create And Use

### 1. Snowflake DW Create_Use

```sql
/* Create WareHouse */
CREATE OR REPLACE WAREHOUSE PENTA_WH
    WAREHOUSE_SIZE = 'LARGE'
    AUTO_RESUME    = TRUE
    AUTO_SUSPEND   = 300;

USE WAREHOUSE PENTA_WH;
```

### 2. Snowflake DB Create_Use

```sql
/* Create Database */
CREATE OR REPLACE DATABASE PENTA_DB;

USE DATABASE PENTA_DB;
```

### 3. Snowflake SCHEMA Create_Use

```sql
/* Create Schema */
CREATE OR REPLACE SCHEMA PENTA_SIDE_SCHEMA;

USE SCHEMA PENTA_SIDE_SCHEMA;
```

### 4. Snowflake TABLE Create

```sql
/* Create Table [Traffic Data] */
CREATE OR REPLACE TABLE PENTA_SIDE_SCHEMA.TRAFFIC (
    ID                     VARCHAR(20),
    BASE_DATE              NUMBER,
    DAY_OF_WEEK            VARCHAR(10),
    BASE_HOUR              NUMBER,
    LANE_COUNT             NUMBER,
    ROAD_RATING            NUMBER,
    ROAD_NAME              VARCHAR(50),
    MULIT_LINKED           NUMBER,
    CONNECT_CODE           NUMBER,
    MAXIMUM_SPPED_LIMIT    FLOAT,
    VEHICLE_RESTRICTED     FLOAT,
    WEIGHT_RESTRICTED      FLOAT,
    HEIGHT_RESTRICTED      FLOAT,
    ROAD_TYPE              NUMBER,
    START_NODE_NAME        VARCHAR(50),
    START_TURN_RESTRICTED  VARCHAR(20),
    END_NODE_NAME          VARCHAR(50),
    END_TURN_RESTRICTED    VARCHAR(20),
    TARGET                 FLOAT,
    START_TIME             VARCHAR(20),
    DATA_SOURCE            VARCHAR(10),
    DISTANCE               FLOAT
);
```

### 5. Snowflake Stage Create

```sql
/* Create External Stage */
CREATE OR REPLACE STAGE PENTA_SIDE_SCHEMA.TRAFFIC_STAGE
    URL = 's3_url'
    CREDENTIALS = (AWS_KEY_ID = 'aws_key', AWS_SECRET_KEY = 'aws_secret_key')
    FILE_FORMAT = (TYPE                         = 'CSV',
                   FIELD_DELIMITER              = ',',
                   RECORD_DELIMITER             = '\n',
                   SKIP_HEADER                  = 1,
                   FIELD_OPTIONALLY_ENCLOSED_BY = '"',
                   ESCAPE                       = 'NONE',
                   ESCAPE_UNENCLOSED_FIELD      = 'NONE'
                   )
;
```
