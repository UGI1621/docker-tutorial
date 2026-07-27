# What is Docker

### Docker, Docker Image, Docker Container, Docker Daemon

Docker는 **Container**라는 격리된 환경에서 App을 패키징하고 실행할 수 있는 기능을 제공한다.

각 Container는 격리되어 있는 환경이기 때문에

하나의 호스트에서 여러 Container를 동시에 실행할 수 있다.

Container는 App 실행에 필요한 모든것을 갖고 있으므로

호스트에 설치된 환경에 의존하지 않는다.

작업중인 Conatiner를 다른 사람들과 공유할 수 있고

공유 받은 모든 사람들이 동일한 방식으로 작동하는 동일한 Container를 사용할 수 있다.

Docker는 다음 처럼 Container를 관리할 수 있는 도구와 플랫폼을 제공한다.

- Container를 App과 App을 위한 구성 요소를 개발하는 공간으로
- Container를 App을 배포하고 테스트하기위한 기본 단위로
- 준비가 완료되면 App을 Container 형태로 프로덕션 환경에 배포하도록
    - 로컬 데이터 센터든, 클라우드 제공업체이든, 하이브리드 환경이든 동일하게 동작됨

Docker는 Client(Docker)-Server(Docker daemon)아키텍처를 사용한다.

Client는 Container를 빌드,실행,배포하는 고성능 작업을 Docker daemon에게 요청한다.

Client와 daemon은 동일한 시스템에서 실행될 수도 있고, Client를 원격 daemon에 연결할 수도 있다.

Client와 daemon은 REST API, UNIX 소켓, 네트워크 인터페이스를 사용하여 통신한다.

![docker](https://docs.docker.com/get-started/images/docker-architecture.webp)

Client중 Compose가 존재하는데

Compose는 여러개의 컨테이너로 구성된 App을 다룰 수 있도록 해준다.

Docker daemon은 Docker API 요청을 수신하고

Image, Container, Network, Volume같은 도커 객체들을 관리한다.

daemon은 다른 daemon과 통신하여 Docker service를 관리할 수도 있다.

Docker Client는 `docker run` 같은 명령을 daemon(`dockerd`)에 보내고 daemon이 이를 실행한다.

Docker Client는 두개 이상의 Daemon과 통신할 수 있다.

---
[docker docs](https://docs.docker.com/get-started/docker-overview/)
