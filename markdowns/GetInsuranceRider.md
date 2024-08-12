## Tool Name

```
특약보험 조회
```

## API Spec

```
{
  "info": {
    "title": "특약보험 조회 API",
    "version": "1.0.0",
    "description": "특약보험을 조회하는 API입니다."
  },
  "paths": {
    "/v1/skillsets/insurance": {
      "post": {
        "summary": "보험특약에 대한 데이터베이스 검색",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "coverage_code": {
                        "type": "string",
                        "example": "8"
                      },
                      "coverage_name": {
                        "type": "string",
                        "example": "암"
                      },
                      "insurance_code": {
                        "type": "string",
                        "example": "60760"
                      },
                      "insurance_name": {
                        "type": "string",
                        "example": "암생활비보장특약(갱신형) 무배당 최초계약"
                      }
                    }
                  }
                }
              }
            },
            "description": "쿼리로 매칭 된 보험특약 정보 목록"
          }
        },
        "description": "보험 특약 데이터베이스를 검색하고 결과를 반환합니다.",
        "operationId": "listInsuranceRiders",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": [
                  "query"
                ],
                "properties": {
                  "query": {
                    "type": "string",
                    "description": "특약보험 검색에 필요한 보험명 및 보험에 대한 설명"
                  }
                }
              }
            }
          },
          "required": true,
          "description": "Query to search for diseases"
        }
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
GetInsuranceRider
```

## Description for human
```
특약보험을 조회 합니다.
```

## Description for model
```
특약보험 정보를 조회하는 API 입니다..
사용자가 정확한 특약을 선택 할 수 있게 목록을 제공하세요.
```
