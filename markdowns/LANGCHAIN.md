# Runnable 클래스 개요

`Runnable` 클래스는 비동기 프로그래밍이나 작업 실행과 관련된 소프트웨어 라이브러리나 프레임워크 내에서 사용되는 프로그래밍 개념입니다. 이는 작업을 수행하고, 데이터를 처리하며, 결과를 계산하는 단위로, 유연하고 재사용 가능한 구성 요소로 설계되었습니다.

## 핵심 개념

### 일반적인 작업 단위
- `Runnable`은 특정 작업을 수행하는 단위입니다.
- 더 큰 처리 체인이나 워크플로우 내에서 유연하고 재사용 가능한 구성 요소로 기능합니다.

### 입력 및 출력 타입
- 각 `Runnable`은 입력과 출력에 대한 타입을 지정할 수 있습니다.
- 이를 통해 타입 안전성과 명확성을 제공합니다.

### 비동기 및 배치 처리
- 동기 및 비동기 실행(`invoke`/`ainvoke` 및 `batch`/`abatch`)을 지원합니다.
- 작업이 I/O 바운드거나 계산 집약적인 환경에서 효율성과 확장성을 제공합니다.

### 스트리밍 지원
- `stream`과 `astream` 메소드는 점진적인 출력을 생산할 수 있는 상황에 유용합니다.
- 대규모 데이터셋이나 실시간 데이터 스트림 처리에 적합합니다.

### 구성
- `Runnable`은 순차적 또는 병렬 그룹으로 구성될 수 있습니다.
- 복잡한 워크플로우를 구축할 때 간단한 구성 요소를 기반으로 합니다.

## 고급 기능

### 구성 및 사용자 정의
- 추가 파라미터나 설정을 통해 `Runnable`의 동작을 변경할 수 있습니다.
- 다양한 사용 사례에 대한 유연성과 적응성을 제공합니다.

### 스키마 지원
- 입력, 출력, 구성 스키마를 정의할 수 있습니다.
- Pydantic 모델을 사용하여 검증 및 문서화를 지원합니다.

### 디버깅 및 추적
- 디버깅과 실행 추적을 위한 기능을 제공합니다.
- 복잡한 애플리케이션에서 문제를 진단하고 시스템 동작을 이해하는 데 중요합니다.

### 재시도 및 대체 메커니즘
- 재시도 정책과 오류 또는 예외 상황에 대한 대체 전략을 제공합니다.
- 실패 시나리오와 견고함을 고려한 디자인입니다.

## 맥락

- 현대적이고 확장 가능한 애플리케이션 아키텍처를 위한 라이브러리나 프레임워크의 일부일 가능성이 높습니다.
- 데이터 처리 파이프라인, 마이크로서비스, 웹 서버 등 다양한 시스템에서 활용될 수 있습니다.
- 모듈성, 재사용성, 추상화에 초점을 맞춘 설계 원칙을 반영합니다.


# Serializable 클래스 개요

LangChain 프레임워크 내에서 사용되는 `Serializable` 클래스는 객체를 직렬화 가능한 형태로 변환하는 데 사용됩니다. 이 클래스는 객체의 상태를 JSON 형태로 변환하여, 네트워크 전송이나 저장 매체에 저장할 때 사용할 수 있게 합니다.

## 주요 기능과 사용 의도

### 직렬화 가능성 확인

- `is_lc_serializable`: 클래스가 직렬화 가능한지 여부를 반환합니다.

### 네임스페이스 추출

- `get_lc_namespace`: 클래스의 네임스페이스(모듈 경로)를 리스트 형태로 반환합니다.

### 비밀 정보 관리

- `lc_secrets`: 생성자 인자 이름과 비밀 ID의 매핑을 제공합니다. 객체 생성 시 필요한 민감한 정보를 관리합니다.

### 직렬화 대상 속성 관리

- `lc_attributes`: 직렬화 과정에서 포함될 객체의 속성을 지정합니다. 생성자에 전달되어야 하는 중요한 속성을 선택적으로 직렬화에 포함시킵니다.

### 고유 식별자 생성

- `lc_id`: 객체의 고유 식별자를 생성하여 반환합니다. 객체의 유형과 네임스페이스를 기반으로 합니다.

### JSON 변환

- `to_json`: 객체를 직렬화 가능한 JSON 형태로 변환합니다. 비밀 정보, 직렬화 대상 속성, 고유 식별자가 고려되며, 필요한 경우 비밀 정보는 안전하게 처리됩니다.

## 사용 의도

`Serializable` 클래스는 LangChain 프레임워크 내에서 객체의 상태를 표현하고, 다른 시스템이나 저장 매체에 전송하거나 저장하기 위한 표준화된 방법을 제공합니다. 이를 통해 LangChain 프레임워크 내의 구성 요소들이 일관된 방식으로 객체를 직렬화하고, 상호 운용성을 향상시킬 수 있습니다. 민감한 정보의 안전한 관리와 필요한 속성의 선택적 직렬화 기능을 통해 데이터의 안전성과 효율성을 보장합니다.

# RunnableSerializable 클래스 개요

`RunnableSerializable` 클래스는 `Serializable`과 `Runnable`을 결합하여, JSON으로 직렬화할 수 있는 실행 가능한 유닛을 제공합니다. 이 클래스는 LangChain 프레임워크 내에서 사용되며, 실행 가능한 작업을 정의하고, 이를 직렬화하여 구성, 저장, 또는 전송할 수 있게 합니다.

## 주요 특징 및 기능

### 직렬화 가능한 Runnable

- `RunnableSerializable`은 `Runnable`의 모든 기능을 상속받아, 입력을 받아 처리하고 출력을 생성하는 실행 단위로 기능합니다. 추가적으로, 이를 JSON 형태로 직렬화할 수 있는 기능을 제공합니다.

### 이름 속성

- `name`: 실행 가능한 단위의 이름을 나타내며, 디버깅과 추적에 사용됩니다. 선택적으로 설정할 수 있습니다.

### JSON으로 직렬화

- `to_json`: 인스턴스를 JSON 형태로 직렬화하는 메서드입니다. 이 과정에서 실행 가능한 단위의 이름과 그래프 표현이 포함될 수 있습니다.

### 구성 가능한 필드

- `configurable_fields`: 실행 가능한 단위에 구성 가능한 필드를 추가하는 메서드입니다. 이를 통해 실행 시 동적으로 특정 속성을 조정할 수 있습니다.

### 구성 가능한 대안

- `configurable_alternatives`: 실행 가능한 단위에 여러 구성 대안을 제공하는 메서드입니다. 특정 조건에 따라 다른 실행 가능한 단위를 선택적으로 사용할 수 있게 합니다.

## 사용 의도

`RunnableSerializable` 클래스는 LangChain 프레임워크 내에서 복잡한 작업을 정의하고, 이를 구성, 실행, 저장 및 전송하는 과정에서의 유연성과 확장성을 제공합니다. 직렬화를 통해 생성된 JSON 표현은 원격 시스템과의 통신, 설정의 저장 및 로딩, 실행 구성의 공유 등 다양한 상황에서 활용될 수 있습니다.

이 클래스를 사용함으로써 개발자는 실행 로직과 해당 로직의 구성을 명확하게 분리할 수 있으며, 실행 가능한 단위의 재사용성과 유지보수성을 향상시킬 수 있습니다.

# RunnableSequence 클래스 개요

`RunnableSequence`는 `RunnableSerializable`을 상속받는 클래스로, LangChain 프레임워크 내에서 여러 `Runnable` 객체들을 순차적으로 연결하여 실행할 수 있는 구조를 제공합니다. 이 클래스는 각각의 `Runnable` 실행 단위의 출력을 다음 실행 단위의 입력으로 사용합니다. 이는 LangChain에서 가장 중요한 구성 연산자 중 하나로, 거의 모든 체인에서 사용됩니다.

## 주요 특징 및 기능

### 순차적 실행
`RunnableSequence`는 여러 `Runnable` 객체들을 순차적으로 연결하여, 첫 번째 `Runnable`의 출력을 다음 `Runnable`의 입력으로 전달합니다.

### 동기화 및 비동기화 지원
동기(`invoke`) 및 비동기(`ainvoke`) 실행을 자동으로 지원하며, `batch` 및 `abatch` 메서드를 통해 I/O 바운드 `Runnable`에 대해 나이브한 호출보다 빠른 실행을 제공합니다.

### 스트리밍 지원
모든 구성 요소가 `transform` 메서드를 구현한 경우, 입력 스트림을 출력 스트림으로 매핑할 수 있습니다. 이를 통해 스트리밍 입력을 스트리밍 출력으로 직접 전달할 수 있습니다.

### 구성 가능성
`configurable_fields` 및 `configurable_alternatives` 메서드를 통해 실행 시점에 다른 `Runnable`을 선택적으로 사용할 수 있습니다.

## 사용 예시

간단한 함수를 `RunnableLambda`로 변환하고, 이를 `|` 연산자를 사용하여 순차적으로 연결하는 예시입니다.

```python
from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

def mul_two(x: int) -> int:
    return x * 2

runnable_1 = RunnableLambda(add_one)
runnable_2 = RunnableLambda(mul_two)
sequence = runnable_1 | runnable_2
# sequence.invoke(1) 결과는 4
# await sequence.ainvoke(1) 비동기 호출도 가능
```

# RunnableParallel 클래스 개요

`RunnableParallel` 클래스는 `RunnableSerializable`을 상속받아, 여러 `Runnable` 객체들을 병렬로 실행하고, 그 출력을 매핑 형태로 반환합니다. 이 클래스는 LangChain 프레임워크의 두 가지 주요 구성 기본 요소 중 하나로, `RunnableSequence`와 함께 사용됩니다.

## 주요 특징 및 기능

- **병렬 실행**: `RunnableParallel`은 여러 `Runnable`을 동시에 실행하며, 각각에 동일한 입력을 제공합니다.
- **직렬화 지원**: 이 클래스의 인스턴스는 JSON 형태로 직렬화될 수 있으며, `is_lc_serializable` 메서드를 통해 직렬화 가능 여부를 확인할 수 있습니다.
- **동적 구성 지원**: 병렬로 실행되는 각 `Runnable`의 구성을 동적으로 조정할 수 있습니다.

## 사용 예시

### 간단한 함수를 사용한 예시

```python
from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

def mul_two(x: int) -> int:
    return x * 2

def mul_three(x: int) -> int:
    return x * 3

runnable_1 = RunnableLambda(add_one)
runnable_2 = RunnableLambda(mul_two)
runnable_3 = RunnableLambda(mul_three)

sequence = runnable_1 | {  # 이 dict는 RunnableParallel로 변환됩니다.
    "mul_two": runnable_2,
    "mul_three": runnable_3,
}
# 동등한 방법:
# sequence = runnable_1 | RunnableParallel(
#     {"mul_two": runnable_2, "mul_three": runnable_3}
# )
# 또는:
# sequence = runnable_1 | RunnableParallel(
#     mul_two=runnable_2,
#     mul_three=runnable_3,
# )

sequence.invoke(1)
await sequence.ainvoke(1)

sequence.batch([1, 2, 3])
await sequence.abatch([1, 2, 3])
```

## 스트리밍 출력을 동시에 처리하는 예시


### RunnableParallel 클래스 개요

`RunnableParallel` 클래스는 `RunnableSerializable`을 상속받아, 여러 `Runnable` 객체들을 병렬로 실행하고, 그 출력을 매핑 형태로 반환합니다. 이 클래스는 LangChain 프레임워크의 두 가지 주요 구성 기본 요소 중 하나로, `RunnableSequence`와 함께 사용됩니다.

### 주요 특징 및 기능

- **병렬 실행**: `RunnableParallel`은 여러 `Runnable`을 동시에 실행하며, 각각에 동일한 입력을 제공합니다.
- **직렬화 지원**: 이 클래스의 인스턴스는 JSON 형태로 직렬화될 수 있으며, `is_lc_serializable` 메서드를 통해 직렬화 가능 여부를 확인할 수 있습니다.
- **동적 구성 지원**: 병렬로 실행되는 각 `Runnable`의 구성을 동적으로 조정할 수 있습니다.

### 사용 예시

#### 간단한 함수를 사용한 예시

```python
from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

def mul_two(x: int) -> int:
    return x * 2

def mul_three(x: int) -> int:
    return x * 3

runnable_1 = RunnableLambda(add_one)
runnable_2 = RunnableLambda(mul_two)
runnable_3 = RunnableLambda(mul_three)

sequence = runnable_1 | {  # 이 dict는 RunnableParallel로 변환됩니다.
    "mul_two": runnable_2,
    "mul_three": runnable_3,
}
# 동등한 방법:
# sequence = runnable_1 | RunnableParallel(
#     {"mul_two": runnable_2, "mul_three": runnable_3}
# )
# 또는:
# sequence = runnable_1 | RunnableParallel(
#     mul_two=runnable_2,
#     mul_three=runnable_3,
# )

sequence.invoke(1)
await sequence.ainvoke(1)

sequence.batch([1, 2, 3])
await sequence.abatch([1, 2, 3])
```

# RunnableGenerator 클래스 개요

`RunnableGenerator`는 `Runnable` 인터페이스를 구현한 클래스로, 제너레이터 함수를 통해 커스텀 동작을 구현할 수 있습니다. 이 클래스는 스트리밍 기능을 유지하면서 커스텀 출력 파서 등의 커스텀 동작을 쉽게 구현하고자 할 때 유용하게 사용됩니다.

## 핵심 기능

- **제너레이터 함수 실행**: 제너레이터 함수를 실행하여, 이전 단계에서 스트리밍된 출력을 즉시 생성하고 스트리밍할 수 있습니다.
- **스트리밍 지원**: 입력 스트림을 받아, 각 입력 요소에 대해 즉시 출력을 생성하고 스트리밍합니다.
- **동기 및 비동기 실행 지원**: 동기 제너레이터 함수와 비동기 제너레이터 함수를 모두 지원하며, 각각에 대한 동기(`transform`) 및 비동기(`atransform`) 메서드를 제공합니다.

## 사용 예시

### 기본 사용법

```python
from langchain_core.runnables import RunnableGenerator

def gen(input: Iterator[Any]) -> Iterator[str]:
    for token in ["Have", " a", " nice", " day"]:
        yield token

runnable = RunnableGenerator(gen)
runnable.invoke(None)  # 결과: "Have a nice day"
list(runnable.stream(None))  # 결과: ["Have", " a", " nice", " day"]
runnable.batch([None, None])  # 결과: ["Have a nice day", "Have a nice day"]

# 비동기 버전
async def agen(input: AsyncIterator[Any]) -> AsyncIterator[str]:
    for token in ["Have", " a", " nice", " day"]:
        yield token

runnable = RunnableGenerator(agen)
await runnable.ainvoke(None)  # 결과: "Have a nice day"
[p async for p in runnable.astream(None)]  # 결과: ["Have", " a", " nice", " day"]
```

## 스트리밍 컨텍스트에서 커스텀 동작 구현

```python
from langchain_core.runnables import RunnableGenerator, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI()
chant_chain = (
    ChatPromptTemplate.from_template("Give me a 3 word chant about {topic}")
    | model
    | StrOutputParser()
)

def character_generator(input: Iterator[str]) -> Iterator[str]:
    for token in input:
        if "," in token or "." in token:
            yield "👏" + token
        else:
            yield token

runnable = chant_chain | character_generator
assert type(runnable.last) is RunnableGenerator
"".join(runnable.stream({"topic": "waste"}))  # "Reduce👏, Reuse👏, Recycle👏."
```


# RunnableLambda 클래스 개요

`RunnableLambda` 클래스는 파이썬의 호출 가능한 객체(callable)를 `Runnable`로 변환하여, 동기(sync) 또는 비동기(async) 컨텍스트에서 사용할 수 있도록 해주는 유틸리티입니다. 이를 통해 함수나 람다 등을 LangChain의 다른 `Runnable` 구성 요소와 함께 조합하고, 효율적인 데이터 처리 파이프라인을 구축할 수 있습니다.

## 주요 기능

- **Callable을 Runnable로 변환**: 일반 함수, 람다, 또는 다른 호출 가능한 객체를 `Runnable` 인터페이스로 감싸 사용할 수 있습니다.
- **동기 및 비동기 실행 지원**: 제공된 함수가 동기 함수인 경우와 비동기 함수인 경우 모두를 자동으로 처리합니다. 또한, 동기 및 비동기 함수를 모두 명시적으로 제공할 수 있습니다.
- **배치 처리 및 스트리밍 지원**: 단일 입력에 대한 처리뿐만 아니라 여러 입력에 대한 배치 처리를 지원합니다. 스트리밍 처리를 통해 입력 스트림을 받아 출력 스트림을 생성할 수도 있습니다.

## 사용 예시

### 기본 사용법

```python
from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

# 동기 함수를 RunnableLambda로 감싸기
runnable = RunnableLambda(add_one)
# 단일 입력 처리
runnable.invoke(1)  # 2를 반환
# 배치 처리
runnable.batch([1, 2, 3])  # [2, 3, 4]를 반환

# 비동기 실행 지원 (동기 함수를 이용)
await runnable.ainvoke(1)  # 2를 반환
await runnable.abatch([1, 2, 3])  # [2, 3, 4]를 반환

# 동기 및 비동기 함수를 모두 제공
async def add_one_async(x: int) -> int:
    return x + 1

runnable = RunnableLambda(add_one, afunc=add_one_async)
# 동기 함수 사용
runnable.invoke(1)  # add_one 사용
# 비동기 함수 사용
await runnable.ainvoke(1)  # add_one_async 사용
```

# RunnableEachBase 클래스 개요

`RunnableEachBase` 클래스는 입력 시퀀스의 각 요소에 대해 다른 `Runnable`에 호출을 위임하는 `Runnable`입니다. 이 클래스는 다른 `__init__` 인수를 가진 새로운 `RunnableEach` 하위 클래스를 생성할 때만 사용됩니다. `RunnableEach`에 대한 자세한 내용은 해당 문서를 참조하세요.

## 주요 특징 및 기능

- **입력 시퀀스 처리**: 입력으로 받은 리스트의 각 요소를 대상 `Runnable`의 `batch` 또는 `abatch` 메서드에 전달하여 처리합니다.
- **동기 및 비동기 실행 지원**: `invoke`와 `ainvoke` 메서드를 통해 동기 및 비동기 실행을 지원합니다.
- **스트리밍 및 이벤트 스트리밍 미지원**: 현재 `RunnableEach`는 `astream_events`를 지원하지 않으며, 이 메서드를 호출하면 `NotImplementedError`가 발생합니다.

## 사용 방법

`RunnableEachBase` 클래스는 직접 사용되기보다는, 다른 `Runnable`을 감싸는 데 사용되는 베이스 클래스로서의 역할을 합니다. 사용자는 `RunnableEachBase`를 상속받아, 특정 동작을 구현하는 새로운 클래스를 정의할 수 있습니다.

```python
class MyRunnableEach(RunnableEachBase):
    pass

# 예제 사용
bound_runnable = MyRunnable(...)
my_runnable_each = MyRunnableEach(bound=bound_runnable)
result = my_runnable_each.invoke([...])
```

## 구현 세부 사항

- InputType 및 OutputType 속성은 각각 입력 및 출력 타입을 정의합니다. 이들은 bound Runnable의 입력 및 출력 타입을 기반으로 리스트 타입으로 확장됩니다.
- get_input_schema 및 get_output_schema 메서드는 입력 및 출력의 스키마를 생성합니다. 이 스키마는 bound Runnable의 스키마를 기반으로 하며, 리스트로 래핑됩니다.
- _invoke 및 _ainvoke 메서드는 실제 실행 로직을 구현합니다. 이들은 bound Runnable의 batch 또는 abatch 메서드를 호출하여 입력 리스트를 처리합니다.

RunnableEachBase는 복잡한 데이터 처리 파이프라인을 구축할 때 유용하게 사용될 수 있으며, 특히 여러 데이터 항목을 동시에 처리해야 하는 경우에 적합합니다.

# RunnableEach 클래스 개요

`RunnableEach` 클래스는 입력 시퀀스의 각 요소에 대해 다른 `Runnable`에 호출을 위임하는 `Runnable`입니다. 이 클래스를 사용하면, 입력 리스트의 각 항목에 대해 `bound` `Runnable`을 호출하여, 여러 입력에 대한 처리를 간편하게 수행할 수 있습니다.

## 주요 특징 및 기능

- **복수 입력 처리**: `RunnableEach`는 입력으로 받은 리스트의 각 요소를 대상 `Runnable`에 적용하여, 복수의 입력을 효율적으로 처리할 수 있게 합니다.
- **동적 바인딩 지원**: `bind` 및 `with_config` 메서드를 통해, 실행 시간에 입력 인자나 설정을 `bound` `Runnable`에 동적으로 바인딩할 수 있습니다.
- **생명주기 리스너 지원**: `with_listeners` 메서드를 사용하여, `Runnable` 실행 전후 또는 오류 발생 시 호출될 리스너를 설정할 수 있습니다.

## 사용 예시

아래 예시는 `ChatOpenAI` 모델을 사용하여 다양한 주제에 대한 짧은 농담을 생성하는 `Runnable`을 구성하고, `RunnableEach`를 사용하여 여러 입력에 대해 동시에 처리하는 방법을 보여줍니다.

```python
from langchain_core.runnables.base import RunnableEach
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}")
model = ChatOpenAI()
output_parser = StrOutputParser()
runnable = prompt | model | output_parser

runnable_each = RunnableEach(bound=runnable)
output = runnable_each.invoke([
    {'topic': 'Computer Science'},
    {'topic': 'Art'},
    {'topic': 'Biology'}
])

print(output)  # 출력 결과는 각 주제에 대한 농담 리스트입니다.
```

## 구현 세부 사항
- RunnableEach 클래스는 RunnableEachBase에서 상속받으며, 주로 bound Runnable에 대한 호출을 위임하는 역할을 합니다.
- get_lc_namespace 메서드를 통해, LangChain 객체의 네임스페이스를 반환합니다.
- get_name 메서드는 RunnableEach 인스턴스의 이름을 반환하며, 필요에 따라 접미사 또는 사용자 지정 이름을 포함할 수 있습니다.
- bind, with_config, with_listeners 메서드를 사용하여, bound Runnable에 대한 추가 구성이나 리스너 바인딩을 수행할 수 있습니다. 

RunnableEach는 다양한 입력을 동시에 처리해야 하는 경우, 특히 데이터 처리 파이프라인이나 비동기 처리 작업에 유용하게 사용될 수 있습니다.


# RunnableBindingBase 클래스 개요

`RunnableBindingBase`는 주어진 인자(`kwargs`) 집합과 함께 다른 `Runnable`에 호출을 위임하는 `Runnable`입니다. 이 클래스는 특정 `Runnable`에 대해 추가적인 인자를 바인딩하거나, 실행 설정을 커스터마이징할 때 사용됩니다. `RunnableBinding` 클래스를 직접 사용하는 것이 아니라, 다른 `__init__` 인자를 가진 새로운 `RunnableBinding` 하위 클래스를 생성할 경우에만 사용합니다.

## 주요 특징 및 기능

- **위임 실행**: `bound` 프로퍼티를 통해 지정된 `Runnable`에 실행을 위임합니다.
- **인자 바인딩**: 실행 시 `bound` `Runnable`에 전달될 추가적인 인자(`kwargs`)를 정의할 수 있습니다.
- **실행 설정 커스터마이징**: `config` 및 `config_factories`를 통해 실행 설정을 커스터마이징할 수 있습니다.
- **입출력 타입 오버라이딩**: `custom_input_type` 및 `custom_output_type`을 통해 입력 및 출력 타입을 오버라이드할 수 있습니다.

## 메서드 및 프로퍼티

- `get_name`: 바인딩된 `Runnable`의 이름을 반환합니다.
- `InputType` 및 `OutputType`: 오버라이딩된 입력 및 출력 타입을 반환합니다. 커스텀 타입이 지정되지 않은 경우 `bound` `Runnable`의 타입을 반환합니다.
- `get_input_schema` 및 `get_output_schema`: 입력 및 출력 스키마를 반환합니다. 커스텀 타입이 지정된 경우 해당 타입을 사용하고, 그렇지 않은 경우 `bound` `Runnable`의 스키마를 반환합니다.
- `config_specs`: `bound` `Runnable`의 설정 스펙을 반환합니다.
- `get_graph`: 실행 그래프를 반환합니다.
- `invoke` 및 `ainvoke`: 동기 및 비동기 실행 메서드로, 추가적인 `kwargs`와 함께 `bound` `Runnable`을 호출합니다.
- `batch` 및 `abatch`: 여러 입력을 동시에 처리하는 메서드로, 동기 및 비동기 버전이 제공됩니다.
- `stream` 및 `astream`: 입력 스트림을 처리하고 출력 스트림을 생성하는 메서드로, 동기 및 비동기 버전이 제공됩니다.
- `transform` 및 `atransform`: 입력 이터레이터 또는 비동기 이터레이터를 변환하는 메서드로, 동기 및 비동기 버전이 제공됩니다.
- `astream_events`: 비동기 이벤트 스트림을 생성하는 메서드입니다.

## 사용 예시 및 구현 세부 사항

`RunnableBindingBase`는 직접 사용되기보다는, 특정 인자 바인딩이나 설정 커스터마이징이 필요한 경우 사용자 정의 하위 클래스를 생성하기 위한 베이스 클래스로 사용됩니다. 사용자는 `RunnableBindingBase`를 상속받아, 필요한 인자나 설정을 구체화한 새로운 `Runnable` 클래스를 만들 수 있습니다.
