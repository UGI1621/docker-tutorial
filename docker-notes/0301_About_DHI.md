# About DHI

**Docker Hardened Image**

Image를 더 작고, 더 안전하고, 더 믿을 수 있게 만든 Docker의 보안 강화 이미지.

### 이전엔 어떤문제가 있었는가?

1. 필요 없는 것까지 다 들어있는 이미지

    예를들어 Python을 실행한다고 가정한다면 Image 내부에

    - Python
    - bash
    - 각종 리눅스 명령어
    - 디버깅 도구
    - 패키지 관리 프로그램
    - 사용하지 않는 라이브러리

    등이 함께 들어있는 경우가 많았다

<br>

2. 해커가 사용할 수 있는 도구가 그대로 존재

    만약 해커가 서버에 침입했다면, 이미지 안에있는

    - bash
    - curl
    - wget
    - ssh

    같은 도구를 통해 서버를 공격하거나 악성 프로그램을 다운로드 하거나

    내부 시스템을 탐색하기가 매우 쉬웠다.

    **즉, 필요없는 기능이 공격에 활용 될 수 있었다.**

<br>


3. Image안에 무엇이 있는지 명확하지 않았다.

    Image안에 어떤 라이브러리가 들어있는지 명확하게 명시되어있지 않았다.

    그래서 보안에 취약점이 발견되더라도

    - 어떤 영향을 받는지
    - 어떤 버전을 사용하는지

    확인하는데 시간이 많이 걸렸다.

<br>



4. 이 Image가 신뢰할 수 있는지 알 수 없었다.

    인터넷에는 Docker 이미지는 차고 넘친다.

    심지어 `python:3.12` 라는 이미지라도 진짜 공식 이미지인지, 누가 바꾼 이미지인지 알기 어려웠다.


<br>

### 그래서 DHI는 어떤 특징을 갖고 있는가?

- **투명성과 최소화**를 핵심으로 하는 보안 이미지 구조

<br>

- **Distroless 런타임**을 사용해 공격 표면을 최소화하면서 필수 개발 도구 유지
    - 최소한의 구성: App에 필요한 최소한의 바이너리 코드와 직접적인 종속성만 포함
    - 불필요한 요소 제거: 패키지 관리자, shell, 기타 프로그램등 표준 Linux 배포판에 있지만 App에 불필요한 요소들을 제거
    - 보안성 강화: 불필요한 프로그램들이 없어 보안적으로 장점.

<br>

- 모든 이미지에 **완전한 SBOM**과 **SLSA Build Level 3 출처 정보** 포함
    - SBOM : Software Bill of Materials
        - 소프트웨어 제품의 모든 구성요소, 구성요소 간의 관계, 오픈소스 및 외부 서비스와의 융합 방식등을 모두 정리한 문서.
        - SBOM만 있다면 문제나 오류가 생겼을 때, 혹은 사이버 공격을 막아야 할 때 대응이 쉬워진다.
    - SLSA : Supply-chain Levels for Software Artifacts
        - Level 3 의 요구:
            - *isolated build environment* — 빌드 머신이 빌드 사이에 **완전 격리**
            - *non-falsifiable provenance* — provenance 가 빌드 시스템에 의해 서명되고, 빌드 자체에서 변조 불가능
            - *parameterless* — 빌드가 외부 파라미터 없이 결정론적
        - 최고 수준의 무결성 보증을 제공하며, 보안 감사 및 충족 여부를 확인하기 위한 높은 수준의 자동화가 포함됩니다.
        - 이는 고도의 보안 요구 사항을 충족하고 아티팩트의 보안을 보다 강력하게 보장합니다.
            - 아티팩트 : 시스템이나 애플리케이션이 자동으로 생성한 데이터

<br>

- **공개 CVE 데이터 기반 평가**로 취약점 은폐 없이 투명성 유지
    - CVE : Common Vulnerabilities and Exposures
        - 공개적으로 알려진 컴퓨터 보안 결함의 목록

<br>

- 모든 이미지에 **진위 검증 서명** 포함

<br>

- **Alpine 및 Debian 기반**으로 기존 개발팀이 최소한의 변경으로 도입 가능

<br>

- **보안 기본값**을 유지하면서도 이미지 크기를 최대 95%까지 축소

<br>

- DHI Enterprise에서는 **CVE 거의 0 수준** 보장

<br>

---

[더 안전한 컨테이너 생태계를 위한 Docker: 무료 Docker Hardened Imag | GeekNews](https://news.hada.io/topic?id=25167)

[[Docker] Distroless 이미지란?](https://peterica.tistory.com/849)

[IT 업게 보안 최대 이슈, SBOM이 뭔데? 개념과 종류](https://blog.naver.com/fkiiwebzine/223409046065)

[지니언스의 SW 공급망 보안 표준(SLSA) 적용 사례](https://www.genians.co.kr/blog/slsa)

[SLSA 도입의 진짜 비용](https://blog.collabops.ai/blog/engineering/supply-chain-slsa-real-cost)

various LLM
