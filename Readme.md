## Install


```
bash
pip install -r requirements.txt
python -m manage.py runserver
```

## Documentation


본 프로젝트는 스웨거를 이용하여, 문서화 하였습니다.

![image](https://user-images.githubusercontent.com/101803254/200189707-a11ae34f-5382-4248-885d-48b4de8dbd7a.png)

서버 실행 후

{host_url}/swagger 로 들어가시면, 문서를 확인할 수 있습니다.

### GET, DELETE 의 경우 쿼리 파라미터로 받습니다.

## Database
![Account-Book-Service](https://user-images.githubusercontent.com/101803254/200189740-2137c3ba-aed1-4b2d-9939-85738959b6d1.png)

프로젝트 내 config.config_example.yml 참고해서 config.yml 작성해주세요. 

```yaml
databases:
  host: "localhost"
  port: 3306
  database: "account_book"
  username: "db user name"
  password: "db pw"
  timezone: "+09:00"

secrets:
  django: "django secret"

token:
  scret: "jwt secret"
  referesh_expire_day: 7
  expire_sec: 3600
```

## Features

---

### 요구사항

---

- 고객은 이메일과 비밀번호 입력을 통해서 회원 가입을 할 수 있습니다.
/signup
body
```python
{
    "name": "이름",
    "email": "test@test.com",
    "password": "test1234"
}
```
- 고객은 회원 가입이후, 로그인을 할 수 있습니다.
/login
body
```python
{
    "email": "test@test.com",
    "password": "test1234"
}
return {access:"token"}
```
- 로그인하지 않은 고객은 가계부 내역에 대한 접근 제한 처리가 되어야 합니다.
헤더 Authorization에 붙은 토큰으로 제어합니다. 본인 이외에 조회, 수정, 삭제, 복구는 불가합니다.

### 고객은 로그인 이후 가계부 관련 아래의 행동을 할 수 있습니다.

- 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
/account/create
request
```python
{
 "expend": 300123,
 "memo":"돈을 많이 쓴 날"   
}
```
response
```python
{
    "id": 11,
    "created_at": "2022-11-06T19:20:55.423043Z",
    "expend": 3001232,
    "memo": "돈을 많이 쓴 날",
    "is_deleted": "V",
    "deleted_at": null,
    "recovered_at": null,
    "user": 1
}
```

- 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다.
/account/update
request
```python
{"id":11,
 "expend": 100,
 "memo":"수정된 내용"   
}
```
response
```python
{
    "id": 11,
    "created_at": "2022-11-06T19:20:55.423043Z",
    "expend": 100,
    "memo": "수정된 내용",
    "is_deleted": "V",
    "deleted_at": null,
    "recovered_at": null,
    "user": 1
}
```
- 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다.
account/delete?account_id=11
**return**
```python
{
    "id": 11,
    "created_at": "2022-11-06T19:20:55.423043Z",
    "expend": 100,
    "memo": "수정된 내용",
    "is_deleted": "I",
    "deleted_at": "2022-11-07T04:24:08.918097Z",
    "recovered_at": null,
    "user": 1
}
```
- 삭제한 내역은 언제든지 다시 복구 할 수 있어야 합니다.
http://127.0.0.1:8000/account/recover?account_id=11
return
```python
{
    "id": 11,
    "created_at": "2022-11-06T19:20:55.423043Z",
    "expend": 100,
    "memo": "수정된 내용",
    "is_deleted": "V",
    "deleted_at": "2022-11-07T04:24:08.918097Z",
    "recovered_at": "2022-11-07T04:25:01.149142Z",
    "user": 1
}
```

-추가 : 이미 삭제된 내용을 삭제하거나 이미 복구된 내용을 복구하려 할경우 에러가 발생합니다.
http://127.0.0.1:8000/account/recover?account_id=11
```python
{
    "msg": "HTTP_403_FORBIDDEN : 잘못된 요청입니다"
}
```

- 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다.
/account/list 
```
[
    {
        "id": 8,
        "user_id": 1,
        "expend": 300123,
        "memo": "돈을 많이 쓴 날"
    },
    {
        "id": 10,
        "user_id": 1,
        "expend": 300123,
        "memo": "돈을 많이 쓴날"
    },
    {
        "id": 11,
        "user_id": 1,
        "expend": 100,
        "memo": "수정된 내용"
    }
]
```
- 가계부에서 상세한 세부 내역을 볼 수 있습니다.
/account/details?account_id=11
response
```python
{
    "id": 11,
    "created_at": "2022-11-06T19:20:55.423043Z",
    "expend": 100,
    "memo": "수정된 내용",
    "is_deleted": "V",
    "deleted_at": "2022-11-07T04:24:08.918097Z",
    "recovered_at": "2022-11-07T04:25:01.149142Z",
    "user": 1
}
```

### 차후 고도화 작업을 한다면
1. 테스트 코드 커버리지를 상승
2. 단위 테스트를 더 추가
