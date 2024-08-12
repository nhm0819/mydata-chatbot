## Tool Name

```
특약보험 가입조건 조회
```

## API Spec

```
{
  "info": {
    "title": "조건 목록 API",
    "version": "1.0.0"
  },
  "paths": {
    "/v1/skillsets/conditions": {
      "post": {
        "summary": "특정 질병 코드와 담보명을 입력 받고 해당질병과 담보에 대한 특약 가입조건을 반환합니다. 해당 조건들을 보고 유저에게 질문하여 승인여부를 판단하세요.",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "conditions": {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    },
                    "description": {
                      "type": "string"
                    }
                  }
                },
                "example": {
                  "conditions": [
                    "결핵 완치 후 5년 미경과, 약제내성/속립성결핵 이라면 승인가능",
                    "... 생략 ..."
                  ],
                  "description": "유저에게 각 조건에 대해서 한개씩 물어보고 승인 가능한지 확인하세요.\n\nExample:\nai: 결핵은 완치 되었나요?\nuser: 아니오 완치 되지 않았습니다.\n... 생략 .."
                }
              }
            },
            "description": "조건 목록을 성공적으로 반환합니다."
          }
        },
        "parameters": [
          {
            "in": "query",
            "name": "disease_code",
            "schema": {
              "type": "string"
            },
            "required": true,
            "description": "질병 코드"
          },
          {
            "in": "query",
            "name": "rider",
            "schema": {
              "type": "string"
            },
            "required": true,
            "description": "보험 담보 이름 ex) 암, 뇌질환, 재해사망, 일반사망 등등 "
          }
        ],
        "operationId": "listConditions"
      }
    }
  },
  "openapi": "3.0.0",
  "servers": [
    {
      "url": "https://rag.nlpworks.club",
      "description": "Main Production Server"
    }
  ]
}
```

## Name for Model
```
GetJoinCondition
```

## Description for human
```
질병코드 (질병디비에서 조회 후 얻는 키값) 와 담보명( 예를 들자면 암, 뇌질환, 재해사망 같은 것들 )을 입력하면 해당 담보에 대한 특약보험 가입 조건을 반환합니다.
```

## Description for model
```
해당 plan을 사용 하려면 질병 데이터베이스 조회 후 disease_code를 반드시 알아와야 합니다.

질병코드 (질병디비에서 조회 후 얻는 키값) 와 담보명( 예를 들자면 암, 뇌질환, 재해사망 같은 것들 )을 입력하면 해당 담보에 대한 특약보험 가입 조건을 반환합니다.

해당 가입 조건을 보고 유저에게 질문을 하여 가입이 가능한지 불가능한지를 판단하세요.
```
