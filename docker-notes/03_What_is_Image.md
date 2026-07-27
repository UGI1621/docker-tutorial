# What is Image

- Container의 파일과 구성이 정의된것
- Container를 실행하기위한 모든 파일, 바이너리, 라이브러리 및 구성을 포함하는 표준화된 패키지
- 특정 프로세스를 실행하기 위한(컨테이너 생성에 필요한) 모든 파일과 설정(환경)값을 지닌것

<br>

예를들어 Ubuntu image는 Ubuntu를 실행하기 위한 모든 파일을 정의하고,

Oracle 이미지는 Oracle을 실행하는데 필요한 파일과 실행 명령어, port정보를 정의하고있다.

OOP에서 Class와 instance의 관계와 비슷하다

Class == Image, instance == Container로 볼 수 있다.

Container의 프로세스 실행 환경은 Image에 의해 결정되고

Image는 단순히 어떤 운영체제 기반에서, 어떤 라이브러리와 도구를 포함해야하는지 정의해둔 템플릿이다.

Image는 Dockerfile로 생성된다.

<br>

### Immutable Infrastructure

Docker는 ‘불변 인프라(Immutable Infrastructure)’라는 철학을 따른다.

서버, 컨테이너, 이미지와 같은 인프라 구성 요소를 **배포한 이후에는 절대 수정하지 않는 보안 및 운영 모델**이다.

실행 중인 시스템에 패치를 적용하거나 설정을 변경하는 대신, **새로운 버전으로 완전히 교체하는 방식**.

<br>

Mutable한 시스템은 보안 유지와 검증이 더 어렵다.

실행중인 시스템에 직접 패치를 적용하거나 수동으로 업데이트를 하게된다면 다음과 같은 문제가 따른다.

- Configuration Drift
    - 시간이 지나면서 시스템 설정이 의도와 다르게 변경되어 환경 간 차이가 발생
- Untracked Changes
    - 변경 이력이 기록되지 않아 무엇을 어떻게 누가 변경했는지 확인하기 어려움
- Inconsistent Environments
    - 개발, 테스트, 운영 환경 간 설정 차이로 인해 예상치 못한 문제 발생
- Increased Attack Surface
    - 불필요한 변경과 구성 요소가 늘어나면서 공격자가 악용할 수 있는 취약점 증가


<br>

불변 인프라는 이러한 문제를

**통제되고 반복 가능한 빌드 및 배포를 통해서만 변경**이 이루어지도록 함으로써 해결한다.

시스템의 일관성과 보안성이 향상되고, 변경 사항을 쉽게 추적 및 감시할 수 있으며

필요할 경우 이전 버전으로 안정적으로 롤백할 수 있다.

<br>

### Layer

위 같은 불변 인프라에 따라서

어떤 Container에 변경이 필요하게 된다면 Image를 변경해야하고

Image를 변경해야하니 Dockerfile에 코드 한줄을 추가하게 되고

**다시 이미지를 만들고 그 이미지를 다운받아야한다.**

코드 한줄 때문에 불변 인프라에 따라서 수백 MG ~ 수 GB가 되는 이미지를 다시 생성해야하는 것은 매우 비효율적이다.

그래서 등장한 개념이 **Layer**라는 개념이다.

기존 이미지에 추가적인 파일이 필요할 때 모든 파일을 다시 다운로드 받는것이 아닌

**추가적인 파일만 다운로드 하도록**하는 방법이다.

![image.png](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdna%2FmyiAH%2FbtskRerwcMb%2FAAAAAAAAAAAAAAAAAAAAACMqB_Zm-xEhX5cfMdv8II7GWv5_Fv7HiNw1EMvta5fZ%2Fimg.png%3Fcredential%3DyqXZFxpELC7KVnFOS48ylbz2pIh7yKj8%26expires%3D1785509999%26allow_ip%3D%26allow_referer%3D%26signature%3DvkZ2A4h961A0OSquGy0DICp3FmI%253D)

위 그림에서 ubuntu와 nginx라는 이미지는 A B C Layer가 동일하고 nginx Layer만 다르다.

만약 ubuntu 이미지가 기존에 존재하고 nginx 이미를 다운 받는경우 nginx Layer만 다운받게 된다.

<br>

**현재 Docker Image는 여러 layer로 구성되며 각 layer는 이전 layer의 변경 사항을 갖고있다.**

- layer는 read only layer (변경 사항)
- 변경 거나 새로 추가된 내용을 담은 새로운 layer

로 구성된다

git 에서 commit 로그를 쌓는 것과 유사하다.

<br>

업데이트된 부분만 이미지로 생성하고, 생성된 이미지와 기존 이미지를 조합한다.

git pull 혹은 merge와 유사하다.

<br>

**Container를 생성할 때도 레이어 방식이 적용된다.**

컨테이너 생성시 read-only Image Layer 위에 R/W Layer를 추가한다.

---

[도커 컨테이너(Container)와 이미지(Image)란?](https://hoon93.tistory.com/48)

[[Docker] 그래서 도커(Docker)랑 컨테이너(Container)가 뭐냐구요](https://colevelup.tistory.com/30)

[Docker 이미지 이해하기 -- 불변 인프라의 핵심 개념](https://easyfly.tistory.com/1673)

[Immutable infrastructre](https://docs.docker.com/dhi/explore/security-concepts/immutability/#how-docker-hardened-images-support-immutability)

[[Docker] 도커 레이어(Layer)에 대해 알아보자](https://hstory0208.tistory.com/entry/Docker-%EB%8F%84%EC%BB%A4%EC%9D%98-%EB%A0%88%EC%9D%B4%EC%96%B4Layer%EC%97%90-%EB%8C%80%ED%95%B4-%EC%95%8C%EC%95%84%EB%B3%B4%EC%9E%90)
