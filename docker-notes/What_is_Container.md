# What is Container

어떤 App을 하나 만든다고 가정해보자.

여러가지 기술 스택을 사용할것이고, 설치해야한다.

다른 동료들의 데스크탑과 노트북도 마찬가지로 설치를 해야하는데

그들이 설치한 버전(환경)이 나와 같다고 확신할 수 있을까?

App이 요구하는 기술 스택들의 버전이

이미 사용중인 기기의 영향을 받지 않으려면 어떻게 해야할까?

그때 우리가 사용할 수 있는것이 **Container**

Container는 App의 구성 요소에 대한 **독립적인 프로세스**다.

PN의 react, BN의 Python API, DB 등 각 구성요소는 격리된 고유한 환경에서 실행된다.

<br>


## Container는 어디서부터 오게 되었는가

### **Chroot and Chroot jail**

루트 시스템 호출 및 명령줄 도구가 유닉스의 일부로 제공되기 시작했을 때

**Chroot** 를 사용하여 프로세스의 root 디렉토리를 변경하여

파일 시스템에서 **특정 파일 및 디렉토리 집합**으로 보기를 좁힐 수 있었다.

<br>

한마디로 현재 실행중인 프로세스와 자녀 프로세스의 루트 디렉토리를 변경할 수 있었다.

변경된 루트 디렉토리(자녀 프로세스)에서는 그 상위에 디렉토리에 파일 및 명령에 접근할 수 없게한다.

이렇게 변경된 환경을 chroot jail이라고 부른다.

<br>

chroot는 **파일 시스템 사용을 제한**할 수 있었다.

하지만 **여전히** 일반 IPC(Inter-Process Communication)을 사용하거나 네트워크 인터페이스로 서로 통신이 가능했고(완전한 격리 불가능)

root user로 실행되는 프로세스가 시스템에 미치는 영향, 권한을 제한하는 데는 사용할 수 없었다.

<br>

구성하는 방법도 까다롭기도 했고 위 같은 이유 때문에 chroot jail의 프로세스가 쉽게 외부로 영향을 줄 수 있었고, 이것이 우리가 흔히 아는 “JailBreak(탈옥)” 이라는 용어가 등장하게 된 배경이다.

이후 OS 수준의 가상화를 제공하기 위해 FreeBSD 4.0은 크게 확장된 jail 개념을 도입했다.

1. 각 jail에는 고유한 IP, root, CPU, 메모리등의 리소스 제한이 있다.
2. 모든 jail은 동일한 커널을 공유하지만 각 jail에서 동일한 UID, GID가 존재하더라도 구분할 수 있다.
    1. A jail의 root user만 제한없이 기능을 사용할 수 있다.
    2. 현재 jail에서 실행중인 프로세스는 다른 jail의 프로세스에 신호를 보낼 수 없다.(UID가 일치하더라도)
    3. 파일 시스템의 마운트 및 마운트 해제, 장치 노드 생성 및 라우팅 테이블 수정도 금지된다.

<br>

위 같은 환경을 제공하면서 기존 시스템 과의 호환성 유지를 위해 몇가지 엄격한 제한이 존재했다.

- jail은 통신을 위해 하나의 IPv4 주소만 가질 수 있다.
- UDP 또는 TCP만 사용할 수 있다 (raw sockets, IPv6 등 금지)
- 호스트 커널을 공유하므로 커널 자체를 격리하거나 서로 다른 커널 버전을 실행할 수 없다
- …

FreeBSD jail은 OS 수준의 가상화의 중요한 출발점이었지만, 기능적인 제약도 분명했다.

<br>

### Solaris Container

Solaris 10은 **Solaris Zones**를 도입하여 프로세스와 파일 시스템을 독립적으로 격리할 수 있는 OS 수준의 가상화를 제공하였다.

이후 여기에 CPU,메모리 등의 **리소스 관리**기능이 결합되면서 **Solaris Containers**라는 개념으로 발전했다.


<br>

FreeBSD Jail이 주로 “격리”에 초점을 맞췄다면

Solaris Container는 **격리와 리소스 제어를 통합하여 하나의 물리 서버에서 여러 워크로드를 안정적으로 운영하는 것**을 목표로 하였다.

한마디로 Solaris Container는 “하나의 서버” 즉, **경량 운영체제 인스턴스**를 만드는데에 가까웠다.

<br>

### LXC의 등장

FreeBSD는 jail, Solaris는 Zones가 존재했지만 Linux에는 OS 수준의 가상화(Container)기능이 존재하지 않았다.

chroot, vserver(독립된 가상 사설 서버), OpenVz(운영체제 가상화)같은 여러 프로젝트들이 존재했으나

모두 커널 패치(리눅스 커널의 소스 코드를 직접 수정하는 과정)가 필요하거나 특정 기능만 제공하는 등 한계가 존재했다.

<br>

이후 namespace, cgroups가 Linux 커널에 공식적으로 추가 되면서

커널 자체의 기능만으로 Container를 만들 수 있게 되었고, 이를 최초로 종합해서 사용한 프로젝트가 LXC다.

1. cgroups(control groups)

    LXC가 각 Container에 리소스를 제어하고 효율적인 방식으로 할당한다.

    한 Container가 너무 많은 리소스를 소비하여 다른 Container의 성능에 영향을 미치는것을 방지한다.

2. namespace

    각 Container에 대해 별도의 네임스페이스를 생성하여 격리하는데

    프로세스 ID, 네트워크 인터페이스, 파일 시스템 등 각 Container에 대한 다양한 시스템 리소스를 격리한다.

    이런 격리를 통해 한 Container 내의 프로세스가 다른 Container의 리소스를 간섭하거나 액세스 할 수 없게 한다.

3. chroot

    각 Container는 고유한 파일 시스템 계층 구조를 가지고, 한 컨테이너 내의 프로세스가 다른 컨테이너의 파일에 액세스 하거나 수정할 수 없게한다.

<br>

### Docker

초기에는 LXC를 기반으로 Container를 구현했었다.

하지만 LXC는 하나의 작은 OS container에 중점을 두었다면

Docker는 하나의 App container를 만들고 싶었다.

<br>

그래서 Docker는 **libcontainer**(Docker자체 컨테이너 라이브러리)를 개발하여 LXC의 의존성을 제거했다.

libcontainer는 Linux 커널이 제공하는 namespace, cgroups, capabilities, seccomp등의 기능을 직접 사용하여 컨테이너를 생성하고 관리할 수 있도록 추상화한 라이브러리다.

<br>

이후 컨테이너 기술이 표준화 되면서 **OCI(Open Container Initative)** 가 등장하고

Docker는 libcontainer를 기반으로 **runc**를 개발하여 OCI 표준 런타임으로 공개했다.

Docker CLI → `dockerd`  → `containerd` → `runc` → `libcontainer` → **Linux Kernel**

같은 흐름으로 Docker의 실행흐름을 그릴 수 있다.

<br>

`dockerd`(Docker daemon)

- 사용자 인터페이스(CLI/API)와 상호작용하며 Docker 객체(Storage, Network, Image 등)와 상호작용한다.
- containerd와 통신하여 컨테이너 생명주기를 관리한다.

`containerd`

- 컨테이너 런타임
- dockerd의 요청을 받아 컨테이너 생명주기를 관리한다.
- OCI 표준을 준수한다.
- runc를 사용하여 실제 컨테이너를 생성 및 실행한다.

`runc`

- 저수준 컨테이너 런타임
- OCI 표준에 따라 컨테이너를 생성하고 실행한다.
- Linux 커널의 namespaces와 cgroups를 사용하여 컨테이너를 격리한다.

`libcontainer`

- runc의 전신이자 현재는 runc의 핵심 라이브러리로 Go 언어로 작성됨
- Linux커널의 컨테이너 기능(namespaces, cgroups 등)을 추상화 하여 제공함.

<br>

마지막이 **Linux Kernel** 이므로

Linux base OS가 아닌 OS환경에서는 Docker 직접 띄울 수 없다.

그래서 보통 Docker Desktop을 설치하고 Linux 가상환경을 띄우고 그 안에서 Docker Engine을 실행하는 방식으로 사용된다.

---

[Docker korea](https://docker-ko.github.io/#/get-started/docker-concepts/the-basics/what-is-a-container)

[그래서 도커(Docker)랑 컨테이너(Container)가 뭐냐구요](https://colevelup.tistory.com/30)

[chroot](https://c0wb3ll.tistory.com/entry/chroot)

[FreeBSD jail](https://ko.wikipedia.org/wiki/FreeBSD_jail)

[01.컨테이너 이해하기](https://kblch.tistory.com/3)

[OCI](https://github.com/opencontainers/runtime-spec)
