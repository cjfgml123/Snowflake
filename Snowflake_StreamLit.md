# StreamLit in Snowflake(SiS) 

### 1. Snowflake SteamLit 

- Streamlit : Python기반의 대화형 데이터 기반 웹 응용 프로그램을 만들 수 있는 Python 라이브러리.

- 참고 :

  - SnowSight에서 DB -> Schema 하위에 생성할 수 있음.

  - Streamlit을 실행할 warehouse 필요.

  - DDL로 create, alter, drop 함.

  - Stage에 저장된 코드에서 Streamlit 생성 가능.

  - RBAC를 통해 접근 제어 (역할 기반)

  - 개발자가 편집하는 동안 App 실행하면 변경 내용이 App Viewer에 즉시 실시간으로 표시됨.

  - AWS PrivateLink를 사용하여 Snowflake 앱에서 Streamlit에 액세스하는 것은 지원되지 않음. 

#### 1-1. 제한사항

- 일부 SQL command 금지(and their Snowpark Python analogs)
  - USE : Warehouse, Role, Database, Schema
  - PUT and GET
  - Some SHOW limitations(see the doc)

#### 1-2. 가격

- App이 editing or viewing mode 일때 계산 비용 발생.
- 15분 동안 비활성화이면 Sleep 됨.
- App Code 저장 시 Storage 비용 발생.
- Streamlit 비용은 Snowflake의 전체 compute and storage billing에 포함됨.

- 비용 추적을 원활하게 하기 위해 전용 Warehouse 사용 권장.
