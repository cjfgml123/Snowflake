## DynamicTable vs Stream & Task vs MV

- 세 개의 개체에 큰 차이점을 알고, 활용법 참고.

### 1. 참고사항

- 프로시저를 배치로 사용할 때는 Stream & Task를 활용한다. Dynamic Table에서는 프로시저를 호출할 수 없다.
- MV는 Base Table을 단일로만 사용할 수 밖에 없어서, 여러 Base Table을 join(inner,outer,left가능)하여 지속적으로 변화하는 Table을 생성할때는 Dynamic Table을 활용한다.
- Dynamic Table