## Tool Name

```
환자가 걸린 질병 및 질병코드 조회
```

## 답변 형식
1. 
"KCD차수": "8",
"대표질병대분류명": "신생물",
"대표질병코드": "C22",
"영문질병명": "Malignant neoplasm of liver and intrahepatic bile ducts",
"유사질병명": "간내담관암, 간육종, 간암",
"한글질병명": "간 및 간내 담관의 악성 신생물"

2. 
"KCD차수": "9",
"대표질병대분류명": "간암",
"대표질병코드": "C22",
"영문질병명": "Malignant neoplasm of liver and intrahepatic bile ducts",
"유사질병명": "간내담관암, 간육종, 간암",
"한글질병명": "간 및 간내 담관의 악성 신생물"

## API Spec

```
{
  "info": {
    "title": "질병 조회 API",
    "version": "1.0.0",
    "description": "질병에 대해서 조회 합니다. 질병코드를 얻을 수 있습니다."
  },
  "paths": {
    "/v1/skillsets/disease": {
      "post": {
        "summary": "질병에 대해서 조회 합니다. 질병코드를 얻을 수 있습니다.",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "KCD차수": {
                        "type": "string",
                        "example": "8"
                      },
                      "영문질병명": {
                        "type": "string",
                        "example": "Malignant neoplasm of liver and intrahepatic bile ducts"
                      },
                      "유사질병명": {
                        "type": "string",
                        "example": "간내담관암, 간육종, 간암"
                      },
                      "한글질병명": {
                        "type": "string",
                        "example": "간 및 간내 담관의 악성 신생물"
                      },
                      "대표질병코드": {
                        "type": "string",
                        "example": "C22"
                      },
                      "대표질병대분류명": {
                        "type": "string",
                        "example": "신생물"
                      }
                    }
                  }
                }
              }
            },
            "description": "조회 된 질병 object 스키마."
          }
        },
        "description": "질병을 조회하고 검색 결과를 반환합니다.",
        "operationId": "listDiseases",
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
                    "description": "질병 이름 및 질병에 대한 자세힌 설명."
                  }
                }
              }
            }
          },
          "required": true,
          "description": "질병 이름 및 질병에 대한 자세힌 설명을 입력하면 질병을 조회 할 수 있습니다."
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
GetDisease
```

## Description for human
```
질병정보를 조회 하는 API.
```

## Description for model
```
환자가 걸린 질병을 데이터베이스에서 조회 한 뒤 disease_code 및 관련 정보를 찾아옵니다.
사용자가 정확한 질병을 선택 할 수 있게 목록을 제공하세요.
```
