# What is Volume

Volume은 컨테이너의 데이터를 영구적으로 저장하기 위한 저장소이며, Docker가 생성하고 관리한다.

`docker volmue create` 명령을 사용하여 명시적으로 생성할 수도 있고

컨테이너나 서비스를 생성할때 Docker가 자동으로 Volume을 생성할 수도 있다.

Volume이 생성되면 Docker Host 내부의 특정 디렉토리에 저장된다.

해당 Volume을 컨테이너에 마운트하면, 호스트에 저장된 해당 디렉토리(Volume)이 컨테이너 내부로 마운트 된다.

이는 Bind Mount가 동작하는 방식과 유사하지만, Volume은 Docker가 직접 관리하며 호스트 시스템의 핵심 기능과 격리되어 있다.

<br>

## 언제 쓰는가

Docker 컨테이너에서 생성되고 사용되는 데이터를 영구적으로 저장하기 위한 권장 방식이다.

Bind Mount는 호스트 머신의 디렉토리 구조와 OS에 의존하지만 Volume은 Docker가 완전히 관리한다.

다음과 같은 경우에는 Volume을 사용하는 것이 적합하다.

- 백업 관리나 다른 환경으로 마이그레이션 상황이 있는 경우
- Docker CLI나 Docker API로 데이터를 관리할 경우
- Linux와 Windows 컨테이너 양쪽에서 모두 사용할 데이터가 있는 경우
- 여러개의 컨테이너가 하나의 데이터베이스를 안전하게 공유해야할 경우
- 컨테이너나 빌드 과정에서 미리 데이터를 채워야하는 경우
- App이 높은 성능의 I/O를 요구하는 경우

<br>

다만 호스트와 컨테이너 모두 동일한 파일이나 디렉토리에 접근해야한다면 Bind Mount를 사용해야한다.

앵간해서는 컨테이너 내부에서 데이터를 관리하는 것보다 Volume을 사용하는 경우가 더 좋다.

- Volume은 컨테이너의 크기를 증가시키지 않는다.
- 컨테이너의 Writable layer에 데이터를 기록하면 Storage Driver가 파일 시스템을 관리해야한다.
    - Storage Driver는 Linux kernel의 Union Filesystem을 사용한다.
    - 그 결과 추상화 계층이 추가된다.

<br>

반대로 컨테이너가 영구적으로 저장할 필요 없는 (휘발해야하는) 데이터를 생성하는 경우엔

tmpfs mount 사용을 고려할 수 있다.

- 데이터를 영구적으로 저장하지 않는다.
- 컨테이너의 Writable Layer에 기록하지 않으므로 성능을 향상시킨다.

Volume은 `rprivate` (recursive private) 바인드 전파 (bind propagation)을 사용하며

이 바인드 전파 방식을 변경하거나 설정할 수 없다.

<br>

바인드 전파란 예를들어

어떤 Container에 Host의 `/data` 를 마운트하고 그 내부에 다른 volume `/data/user` 를 마운트 한다면

Host입장에서는 `/data/user` 를 추적하지 않는다.

<br>

## Volume의 Lifecycle

Volume은 특정 Container의 생명주기와는 별도로 존재한다.

Volume에 저장된 데이터는 Container가 삭제되더라도 그대로 유지된다.

어떤 Volume이 mount된 Container들이 모두 사라진다 하더라도 Docker는 이를 자동으로 삭제하지 않고

`docker volume prune` 명령으로 삭제할 수 있다.

<br>

## 기존 데이터 위에 Volume을 마운트하면?

### 이미 데이터가 있는 Volume을 마운트 하는경우

컨테이너의 어떤 디렉토리에 데이터가 존재하는 상태에서

**내용이 존재하는 Volume을 마운트하면 기존 파일들은 가려진다**.

Linux에서 `/mnt` 에 파일을 저장한뒤, 그 위에 USB를 마운트 하면 USB의 내용만 보이는 것과 동일한 원리다.

USB를 언마운트 하기 전까지 원래 `/mnt` 에 있던 파일은 볼 수 없다.

<br>

컨테이너도 마찬가지인데, 위 상황과 좀 다르게 컨테이너는 마운트를 제거해서 원래 파일을 다시 보는게 쉽지않다.

때문에 원래 파일을 다시 보려면 **마운트 없이 컨테이너를 새로 생성하는 것이 가장 좋은 방법이다.**

<br>

### 빈 Volume을 마운트 하는경우

컨테이너의 어떤 디렉토리에 데이터가 존재하는 상태에서

**이미 존재하지만 내용이 없는 Volume을 마운트하면 Container에 있던 파일들을 Voluem으로 복사한다**.

**존재하지 않는 Volume도 마찬가지로 복사한다.**

이 기능은 다른 컨테이너에서도 사용할 초기 데이터를 Volume에 미리 채워 넣고 싶을 때 유용하다.

<br>

## `volume-nocopy`

만약 컨테이너에 있던 기존 파일을 빈 Volume으로 복사하지 않게 하고싶다면

`--mount` 옵션에 `volume-nocopy` 옵션을 사용한다.

<br>

## Named Volume과 Anonymous Volume

### Named Volume (이름이 있는 Volume)

사용자가 직접 이름을 지정하는 Volume이다.

```bash
docker run -v my-volume:/data nginx
```

에서 `my-volume` 이 이름이다.

- 이름이 있으면 다시 사용하기 용이함
- 여러 컨테이너에서 공유하기 쉬움
- `docker volume ls` 에서 쉽게 이름으로 식별 가능

```bash
docker run -d --name container1 -v my-volume:/data nginx
docker run -d --name container2 -v my-volume:/backup nginx

# 라고 하면

	#Container1
	#/data
	   #   ↑
	   #   │
	   #my-volume
	   #   │
	   #   ↓
	#Container2
	#/backup

# 같은 구조를 가진다
```

<br>

### Anonymous Volume (익명 Volume)

이름을 지정하지 않으면 Docker가 랜덤한 이름을 붙여서 생성한다.

```bash
docker run -v /data nginx
```

사용법은 Named Volume과 같다.

---

[docker docs](https://docs.docker.com/engine/storage/volumes/)
