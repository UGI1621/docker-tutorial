About Dockerfile

Docker Image를 생성하기위한 스크립트(설정파일)

명령어를 토대로 Dockerfile을 생성한 후 **Build**하면

Dockerfile에 나열된 명령문을 차례대로 수행하며 (Layer) Docker Image를 생성한다.

Dockerfile을 읽을 줄 안다면 해당 Image의 구성을 파악할 수 있다는 의미이기도 하다.

Dockerfile은 확장자 없이 `Dockerfile` 이다. (`Makefile` 과 비슷하다)

<br>

## FROM

새로운 **Build Stage**를 시작하고, 이후에 실행되는 명령어들의 Base Image를 지정한다.

**유효한 Dockerfile은 반드시 `FROM` 으로 시작해야한다.**

`FROM` 에서 지정하는 이미지는 Docker에서 사용할 수 있는 모든 유효한 Image를 사용할 수 있다.

```docker
FROM [--platform=<platform>] <image> [AS <name>]
```

`<image> [AS <name>]`

- `<image>` 를 기반으로 빌드를 수행하고, 이 빌드 스테이지의 이름을 `<name>` 으로 지정한다.
- 이후 Multi-stage Build에서 `COPY --from=<name>` 으로 참조가 가능하다.

`--platform=<platform>`

- 특정 플랫폼(`linux/amd64` , `linux/arm64`)용 이미지를 사용할 때 지정한다.

```docker
FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]
```

`:<tag>`

- 사용할 이미지의 버전을 지정한다. (`python:3.12` , `nginx:1.29` )

```docker
FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]
```

`@<digest>`

- tag 대신 Image Digest를 사용하여 정확히 동일한 이미지를 지정할 수 있다.
- 태그는 변경될 수 있지만 Image Digest는 변경되지 않으므로 Reproducible(재현 가능한) Build에 유용하다

<br>

`tag` , `digest` 는 선택사항이나, 둘중 하나를 생략하면 빌더는 기본적으로 `latest` 태그를 사용한다.

지정한 태그 값을 찾을 수 없는 경우 빌더는 오류를 반환한다.

<br>

하나의 Dockerfile에는 여러 개의 `FROM` 명령어를 사용할 수 있다.

이를 통해 여러 이미지를 생성하거나, 하나의 빌드 스테이지를 다른 빌드 스테이지의 의존성으로 사용할 수 있다.

새로운 `FROM` 명령어가 실행되기 전에 생성된 마지막 이미지 ID를 기준으로 새로운 빌드가 시작되고

각 `FROM` 명령어는 이전 명령어들에서 생성된 모든 상태를 초기화한다.

<br>

이전 빌드 스테이지를 이후 스테이지의 기반으로 사용하는 것은 공통된 기본 환경을 공유하기 위한 일반적인 패턴이다.

```docker
FROM ubuntu AS base
RUN apt-get update && apt-get install -y shared-tooling

FROM base AS dev
RUN apt-get install -y dev-tooling

FROM base AS prod
COPY --from=build /app /app
```

<br>

## ARG

`FROM` 명령어는 첫 번째 `FROM` 이전에 선언된 모든 `ARG` 명령어의 변수를 사용할 수 있다.

```docker
ARG CODE_VERSION=latest
FROM base:${CODE_VERSION}
CMD /code/run-app

FROM extras:${CODE_VERSION}
CMD /code/run-extras
```

첫 번째 `FROM` 이전에 선언된 `ARG` 는 빌드 스테이지 밖에서 선언된 것으로,

`FROM` 이후의 다른 명령에서는 사용할 수 없다.

<br>

첫 번째 `FROM` 이전에 선언한 `ARG` 의 기본값을 빌드 스테이지 내부에서도 사용하려면

빌드 스테이지 안에서 값 없이 `ARG` 명령어를 다시 선언해야한다.

```docker
ARG VERSION=latest
FROM busybox:$VERSION
ARG VERSION
RUN echo $VERSION > image_version
```

<br>

## WORKDIR

```docker
WORKDIR /path/to/workdir
```

`WORKDIR` 명령어는 Dockerfile에서 이후에 오는 `RUN` , `CMD` , `ENTRYPOINT` , `COPY` , `ADD` 명령어의 작업 디렉토리를 설정한다.

지정한 `WORKDIR` 이 존재하지 않는경우 자동으로 생성된다. (이후에 사용되지 않더라도 생성됨)

`WORKDIR` 은 하나의 Dockerfile에서 여러번 사용할 수 있다.

<br>

상대 경로를 지정하면 이전 `WORKDIR` 를 기준으로 해석된다

```docker
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
# /a/b/c
```

`WORKDIR` 는 이전에 `ENV` 명령어로 설정한 환경 변수를 사용할 수 있다.

단, Dockerfile에서 명시적으로 설정한 환경 변수만 사용할 수 있다.

```docker
ENV DIRPATH=/path
WORKDIR $DIRPATH/$DIRNAME
RUN pwd
# /path/$DIRNAME
```

<br>

`WORKDIR` 을 지정하지 않으면 기본 작업 디렉토리는 `/` 이다.

`FROM scratch` 가 아닌 기존 이미지를 기반으로 Dockerfile을 작성하는 경우,

사용하는 베이스 이미지에서 이미 `WORKDIR` 가 설정되어 있을 수 있다.

따라서 알 수 없는 디렉토리에서 의도치 않은 작업이 수행되는 것을 방지하기 위해

`WORKDIR` 을 명시적으로 설정하는 것이 권장된다.

<br>

## COPY

`COPY` 는 두가지 형식이 존재하는데 두 번째 형식은 공백이 포함된 경로를 사용할 때 반드시 사용해야한다.

```docker
COPY [OPTIONS] <src> ... <dest>
COPY [OPTIONS] ["<src>", ... "<dest>"]
```

`<src>` 에 있는 새로운 파일 또는 디렉토리를 복사하고

이미지의 파일 시스템에서 `<dest>` 경로에 추가한다.

파일과 디렉토리는 다음 위치에서 복사할 수 있다.

- Build context (Dockerfile 이 빌드 중에 접근할 수 있는 파일들의 집합)
- Build stage (한번의 `FORM` 명령어 블록 영역)
- Named Context

    ```docker
    docker build \
      --build-context config=./configs \
      --build-context docs=./documents .
    ```

    처럼 `--build-context` 를 사용하여 만들어진 context

    프로젝트와는 별개의 디렉토리에서 파일을 가져오고 싶을 때 유용하다.

- Image

<br>

**마지막 인수는 항상 목적지**여야 하고, 목적지는 **반드시 디렉토리**여야 하며 **경로 끝에 `/` 를 붙인다**.

```docker
COPY file1.txt file2.txt /usr/src/things/
```

<br>

### Build Context에서 복사하기

빌드 컨텍스트에서 원본 파일을 복사할 때, 경로는 **빌드 컨텍스트의 루트 디렉토리를 기준으로 한 상대경로**로 해석된다.

원본 경로를 `/` 로 시작하거나 끝나거나 빌드 컨텍스트 밖으로 이동하는 경로를 지정하면 (`../`) 자동으로 제거된다.

`COPY something/ /something` 과 `COPY something /something` 은 동일하게 작동한다.

<br>

원본이 **디렉토리**라면 **디렉토리 자체가 아니라 디렉토리 내부의 내용, 파일 시스템 메타데이터가 복사**된다.

하위 디렉토리가 있다면 함께 복사되고, 목적지에 같은 이름의 디렉토리가 존재한다면 내용이 병합된다.

파일 충돌이 발생하면 추가되는 파일이 우선 적용되나, 파일 위에 디렉토리를 복사하려고 하면 오류가 발생한다.

<br>

원본이 **파일**이라면 파일과 해당 메타데이터가 목적지로 복사된다. 파일 권한도 그대로 유지된다.

목적지에 같은 이름의 **디렉토리**가 존재한다면 오류가 발생한다.

Build Context로 Git 저장소를 사용하는 경우, 복사된 파일의 기본 권한은 664다.

저장소에서 실행 권한이 설정된 파일은 744로 복사되고 디렉토리 권한은 755로 설정된다.

<br>

### Pattern Matching

로컬 파일을 복사할 때 각 `<src>` 에는 Wildcard를 사용할 수 있으며, 매칭은 Go의 filepath.Match 룰을 따른다.

<br>

### Destination

목적지 경로가 `/` 로 시작되면 **절대 경로**로 해석되고,  현재 빌드 스테이지의 루트 디렉터리를 기준으로 파일이 복사된다.

경로 끝의 `/` 도 다음처럼 중요한 의미를 가진다.

```docker
COPY test.txt /abs
# /abs 파일 생성
```

```docker
COPY test.txt /abs/
# /abs/test.txt 생성
```

목적지 경로가 `/` 로 시작되지 않으면 **`WORKDIR` 를 기준으로 하는 상대 경로**로 해석된다.

목적지 경로가 존재하지 않으면, 해당 경로와 필요한 상위 디렉토리까지 모두 자동으로 생성된다.

<br>

### ADD and COPY

`ADD` 와 `COPY` 명령어는 기능적으로 비슷하지만, 각각 약간 다른 목적을 가지고 있다.

`COPY` 는 Build Context 또는 Multi-stage Build의 다른 Build stage에서 파일을 컨테이너로 복사하는 기본적인 기능을 제공한다.

`ADD` 는 원격 HTTPS 및 Git URL에서 파일을 가져오는 기능, Built Context에서 추가하는 압축 파일을 자동으로 압축 해제하는 기능을 지원한다.

대부분의 경우에는 Multi-stage Build에서 한 stage의 파일을 다른 stage로 복사할 때 `COPY` 를 사용하는것이 좋다.

Build Context의 파일을 `RUN` 명령어를 실행하기 위해 **일시적으로만** 컨테이너에 추가해야 하는 경우엔

`COPY` 대신 **Bind Mount**를 사용하는것이 더 효율적이다.

예를 들어, `RUN pip install` 명령을 위해 `requirements.txt` 파일을 일시적으로 추가하려면

```docker
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
pip install --requirement /temp/requirements.txt
```

처럼 사용할 수 있다.

<br>

다만, Bind Mount로 추가된 파일은 **해당 `RUN` 명령이 실행되는 동안에만 일시적으로 존재**한다.

즉, 최종 Image에는 포함되어있지 않다.

Build Context의 파일을 **최종 Image에도 포함해야 한다면 `COPY` 를 사용해야한다.**

<br>

`ADD` 명령어는 **빌드 과정에서 원격 리소스를 다운로드해야 하는 경우**에 가장 적합하다.

압축 파일을 직접 해제하는 것보다 `ADD` 를 사용하는 것이 더 정확한 Build Cache를 보장한다.

또한 `ADD` 는 리소스의 Checksum 검증을 기본적으로 지원하고,

Git URL의 branch, tag, subdirectory를 해석하는 기능도 제공한다.

<br>

다음은 `ADD` 를 사용하여 `.NET` 런타임 설치 파일을 다운로드 한다.

Multi-stage Build와 함께 사용하면 최종 stage에는 `.NET` 런타임만 남고 중간 파일은 포함하지 않는다.

```docker
# syntax=docker/dockerfile:1

FROM scratch AS src
ARG DOTNET_VERSION=8.0.0-preview.6.23329.7
ADD --checksum=sha256:270d731bd08040c6a3228115de1f74b91cf441c584139ff8f8f6503447cebdbb \
    https://dotnetcli.azureedge.net/dotnet/Runtime/$DOTNET_VERSION/dotnet-runtime-$DOTNET_VERSION-linux-arm64.tar.gz /dotnet.tar.gz

FROM mcr.microsoft.com/dotnet/runtime-deps:8.0.0-preview.6-bookworm-slim-arm64v8 AS installer

# Retrieve .NET Runtime
RUN --mount=from=src,target=/src <<EOF
mkdir -p /dotnet
tar -oxzf /src/dotnet.tar.gz -C /dotnet
EOF

FROM mcr.microsoft.com/dotnet/runtime-deps:8.0.0-preview.6-bookworm-slim-arm64v8

COPY --from=installer /dotnet /usr/share/dotnet
RUN ln -s /usr/share/dotnet/dotnet /usr/bin/dotnet
```

<br>

### Options

- **`COPY --from`**

    기본적으로 `COPY` 명령어는 Build Context 에서 파일을 복사한다.

    `--from` 옵션을 사용하면 Build Context대신 Image, Build Stage, Named Context 에서 파일을 복사할 수 있다.

    ```docker
    COPY [--from=<image|stage|context>] <src> ... <dest>
    ```

    `--from` 에서 사용하는 원본 경로는 항상 지정한 이미지 또는 Build Stage의 파일 시스템 루트(`/`)를 기준으로 해석된다

<br>

- **`COPY --chmod`**

    ```docker
    COPY [--chmod=<perms>] <src> ... <dest>
    ```

    권한을 설정할 수 있다.

    8진수 표기법과 기호 표기법을 지원한다. chmod(1) manual

<br>

- **`COPY --chown`** : 복사되는 파일의 소유자와 그룹을 설정함

    ```docker
    COPY [--chown=<user>:<group>] <src> ... <dest>
    ```

<br>

- **`copy --link`**

    ```docker
    COPY [--link[=<boolean>]] <src> ... <dest>
    ```

    `COPY` , `ADD` 명령어에서 `--link` 옵션을 사용하면 **복사된 파일이 독립적인 Layer에 저장된다**.

    따라서 이전 레이어의 명령이 변경되더라도, 해당 파일이 포함된 레이어는 무효화 되지 않는다.

    즉, 이전 레이어의 파일을 읽지 않도록 분리 시킨다.

    그렇다 보니 `--link` 옵션을 사용했을때 목적지가 심볼릭 링크라면 따라가지 못한다.

    예를들어

    `/var/log` → `/real_logs` 같은 심볼릭 링크가 존재한다면

    ```docker
    COPY logs/ /val/log/

    /
    ├── real_logs/
    │   ├── app.log
    │   └── ...
    └── var/
        └── log -> /real_logs
    ```

    ```docker
    COPY --link logs/ /var/log/

    /
    ├── real_logs/
    │   ├── app.log
    │   └── ...
    └── var/
        └── log/ (create new dir)
    ```

    위 처럼 아예 새로운 디렉토리를 만들어 버린다.

    이 옵션의 핵심은 레이어 구조를 바꾸는 것이 아니라

    **COPY 레이어의 캐시를 이전 레이어와 최대한 분리해서 관리하는 것**이 핵심이다.

	<br>

    예를 들어

    ```docker
    RUN apt install ...
    COPY --link assets /assets
    ```

    `assert` 가 2GB인데 거의 바뀌지 않고,

    `RUN apt install ...` 만 자주 수정된다면 2GB를 다시 `COPY`하지 않아도 된다.

    반대로

    ```docker
    COPY --link . .
    ```

    처럼 매일 수정되는 소스 코드를 독립적인 Layer로 저장한다면

    매번 업데이트 될때마다 똑같이 매번 `COPY`하기에 이점이 없고

    오히려 매번 모든 파일이 통째로 새로운 Layer에 잡히기에 Image build가 더 오래걸릴 수 있다.

    그래서 보통 Multi-stage Build의 결과물만 복사할 때, 빌드 산출물만 골라서 복사할 때 사용하면 빌드가 효율적으로 이루어진다.


<br>

- **`COPY --parents`** : 원본(src)의 상위 디렉토리 구조를 유지한 채 복사한다.

    기본값은 `false`

    ```docker
    # syntax=docker/dockerfile:1
    FROM scratch

    COPY ./x/a.txt ./y/a.txt /no_parents/

    # 결과1
    # /no_parents/a.txt

    COPY --parents ./x/a.txt ./y/a.txt /parents/

    # 결과2
    # /parents/x/a.txt
    # /parents/y/a.txt
    ```

    `--parent` 를 사용하지 않으면 같은 이름을 복사할 때 Buildkit은 나중에 복사한 파일로 기존 파일을 조용히 덮어쓴다. (결과 1)


<br>

- **`COPY --exclude`** : 복사 대상에서 제외할 파일이나 디렉토리의 경로 패턴을 지정할 수 있다.

    ```docker
    COPY [--exclude=<path> ...] <src> ... <dest>
    ```

    경로패턴은 `<src>` 와 동일한 형식을 사용하고 Wildcard를 사용할 수 있으며, 매칭은 Go의 filepath.Match 룰을 따른다.

    예를들어 `hom` 으로 시작하는 모든 파일을 복사하되 `.txt` 확장자를 가진 파일을 제외하려면

    ```docker
    # syntax=docker/dockerfile:1
    FROM scratch

    COPY --exclude=*.txt hom* /mydir/
    ```

<br>

## RUN

`RUN` 명령어는 현재 이미지 위에 **새로운 레이어를 생성**하기 위해 명령을 실행한다.

추가된 레이어는 Dockerfile의 다음 단계에서 사용된다.

```docker
# Shell format
RUN [OPTIONS] <command> ...

# Exec format
RUN [OPTIONS] ["<command>", ...]
```

보통 shell format이 사용되고, 줄바꿈 이스케이프`\` 나 Heredoc을 사용하여 긴 명령을 여러 줄에 걸쳐 작성할 수 있다.

<br>

`RUN` 명령의 캐시는 다음 빌드에서 무효화되지 않는다.

예를들어 다음 명령어를 이전에 실행했었다면

```docker
RUN apt-get dist-upgrade -y
```

새로 Build할 때 `RUN`을 수행하지 않고 이전에 실행했던 결과의 캐시를 가져오게 된다.

`--no-cache` 옵션을 사용하여 캐시를 무효화 할 수 있다.

<br>

또한 `ADD` , `COPY` 명령어는 `RUN` 의 캐시를 무효화할 수도 있다.

예를들어

```docker
FROM ubuntu
COPY requirements.txt .
RUN pip install -r requirements.txt
```

같은 Dockerfile을 build한 상황에서 다음 build 때 `requirements.txt` 가 변경되었다면

Docker입장에서 “`COPY` 결과가 바뀌었네” 라고 판단하고 `RUN` 을 다시 실행시킨다.

### OPTIONS

- `RUN --mount`

    ```docker
    RUN --mount=[type=TYPE][,option=<value>[,option=<value>]...]
    ```

    현재 빌드중인 `RUN` 명령에서만 사용할 수 있는 File System Mount를 생성할 수 있게 해주는 옵션

    - Host File System이나 다른 Build Stage를 Bind Mount한다.
    - Secrets나 SSH Agent 소켓에 접근한다.
    - 패키지 관리자나 컴파일러의 캐시를 유지하여 빌드 속도를 향상시킨다.

    - `type`

		- `bind`
			- Build Context나 다른 Build Stage를 Read-only로 바인드 마운트한다.
			- Options
				- `target` , `dst` , `destination` : 마운트될 대상 경로
				- `source` : `from` 에서 가져올 원본 경로. 기본값은 `from` 의 루트 디렉토리
				- `from` : 원본이 되는 Build Stage, Context, Image의 이름. 기본값은 Build Context
				- `rw` , `readwrite` : 마운트에 대한 쓰기권한을 허용. 단, `RUN` 명령이 끝나면 작성된 데이터는 모두 삭제되며, 이미지 레이어 저장되지않음.

			```docker
			FROM gcc

			RUN --mount=type=bind,source=hello.c,target=/hello.c \
				gcc /hello.c -o /hello
			```

			`RUN` 이 끝나면 `/hello.c` 는 없어진다.

		<br>

		- `cache`
			- 컴파일러나 패키지 관리자의 캐시 디렉토리를 임시로 마운트하여 빌드 속도를 높인다.
			- 오직 성능 향상만을 위한 기능이다.
			- 위에 의해 캐시 디렉토리의 내용에 의존해서는 안된다.
				- 다른 빌드가 같은 캐시를 덮어쓸 수도 있고, Buildkit이 캐시를 삭제할 수도 있다.

		<br>

		- `tmpfs`
			- 빌드 컨테이너 내부의 `tmpfs` (메모리 기반 임시 파일 시스템)을 마운트한다.
			- 엄청 큰 임시파일을 만들때나 민감한 데이터를 잠깐 저장할 때 사용된다
			- 일반적인 웹서비스같은 소규모 빌드 환경에서는 사용할 일이 거의 없다.
			- 빌드 성능을 극한까지 최적화 하거나, 대규모 빌드 환경에서 주로 사용된다.

		<br>

		- `secret`
			- 개인 키와 같은 민감한 파일을 이미지나 빌드 캐시에 포함시키지 않고 빌드 컨테이너에서 사용할 수 있도록 한다.
			- Options
				- `id` : secret의 ID. 기본값은 target 경로의 basename
				- `target` , `dst` , `destination`  : secret을 지정한 경로에 마운트한다.
					- 경로와 `env` 둘다 지정하지 않으면 `/run/secrets/` + `id` 에 마운트
				- `env` : 파일 대신 환경 변수로 secret을 마운트하거나, 두 형태로 마운트한다.
				- `required` : `true` 로 설정하면 secret을 사용할 수 없을 때 명령이 오류를 발생한다. 기본값은 `false`
				- `mode` : secret 파일의 권한 모드. 기본값은 `0400`
				- `uid` : secret 파일의 사용자 id. 기본값 `0`
				- `gid` : secret 파일의 그룹 id. 기본값 `0`

			```docker
			# syntax=docker/dockerfile:1

			FROM alpine

			RUN --mount=type=secret,id=API_KEY,env=API_KEY \
				some-command --token-from-env $API_KEY
			```

			위 같은 빌드 환경에서 `API_KEY` 가 환경변수로 설정되어 있다고 가정하면

			```bash
			docker buildx build --secret id=API_KEY .
			```

			같은 명령어로 빌드가 가능하다.

		<br>

		- `ssh`
			- SSH Agent를 통해 SSH 키에 접근할 수 있도록 하며, 암호가 설정된 키도 지원한다.

<br>

## `ENV`

```docker
ENV <key>=<value> [<key>=<value>...]
```

이 값은 해당 Build Stage의 이후 모든 명령에서 환경 변수로 사용되며, 여러 명령에서 인라인으로 치환될 수 있다.

명령줄 파싱과 마찬가지로, 값 안에 공백을 포함하려면 따옴표와 백슬래시`\` 를 사용하 수 있다.

```docker
ENV MY_NAME="John Doe"
ENV MY_DOG=Rex\ The\ Dog
ENV MY_CAT=fluffy

# 한번에도 가능
ENV MY_NAME="John Doe" MY_DOG=Rex\ The\ Dog \
    MY_CAT=fluffy
```

<br>

`ENV` 로 설정한 환경 변수는 **생성된 이미지에서 컨테이너를 실행할 때도 유지된다**.

```bash
docker inspect
****# or
****docker run --env <key>=<value>
```

위 같은 명령어로 확인 가능하다.

하나의 stage는 부모 stage 에서 `ENV` 로 설정된 환경 변수를 상속받는다.


<br>

## `CMD`

이미지로부터 컨테이너를 실행할 때 실행될 명령을 설정한다.

```bash
# Exec format
CMD ["executable","param1","param2"]

# Exec format use `ENTRYPOINT`
CMD ["param1","param2"]

# Shell format
CMD command param1 param2
```

하나의 Dockerfile에는 **하나의 `CMD` 만 존재할 수 있다.**

여러개의 `CMD` 를 작성하게되면 마지막 `CMD` 만 적용된다.


<br>

이 명령어의 목적은 **실행되는 컨테이너에 대한 기본값을 제공하는 것**이다.

이 기본값에는 실행파일이 포함될 수도, 실행파일을 생략할 수도 있다.

<br>

실행파일을 생략하는 경우 반드시 `ENTRYPOINT` 명령도 함께 지정해야한다.

컨테이너가 항상 같은 실행 파일을 실행해야 한다면, `CMD` 와 함께 `ENTRYPOINT` 사용을 고려해야 한다.

`docker run` 실행 시 사용자가 인자를 지정하면 `CMD` 에 지정된 기본값은 덮어쓰지만

기본 `ENTRYPOINT` 는 그대로 사용된다.

<br>

`CMD` 를 `ENTRYPOINT` 의 기본 인자로 제공하는 용도로 사용하는 경우

두 명령어 모두 exec format으로 작성해야한다.

<br>

**`RUN` 과 `CMD` 를 혼동해선 안된다.**

- `RUN` 은 실제로 명령을 실행하고 그 결과를 이미지 레이어에 저장한다.
- `CMD` 는 빌드 시점에는 아무것도 하지 않으며, 이미지가 실행될 때 사용할 명령을 지정한다.

<br>

## `ENTRYPOINT`

**컨테이너를 실행 가능한 프로그램처럼 동작하도록 설정**할 수 있게한다.

```docker
# Exec format (recomand)
ENTRYPOINT ["executable", "param1", "param2"]
```

`docker run <image>` 뒤에 전달되는 명령줄 인자들은 exec 형식의 `ENTRYPOINT` 뒤에 추가된다.

그리고 `CMD` 에 지정된 모든 값을 덮어쓰게 된다.

```docker
FROM ubuntu

ENTRYPOINT ["top", "-b"]
CMD ["-c"]
```

컨테이너를 실행하면 `top` 만이 유일한 프로세스로 실행된다.

<br>

`ENTRYPOINT` 도 덮어쓸 수 있는데

```bash
docker run --entrypoint
```

로 덮어쓸 수 있다.

<br>

예시)

`CMD` 의 경우

```docker
FROM ubuntu
CMD ["/bin/df", "-h"]
```

```bash
$ docker build -t ugi/df .
$ docker run --name ugi-df ugi/df
```

 위 경우 Dockerfile에 정의된대로 `df -h` 명령을 실행하게 된다.

컨테이너 실행시 추가 인자 값을 줘서 컨테이너가 수행할 명령을 바꾼다면

```bash
$ docker run --name ugi-df ugi/df ps -aef
```

Dockerfile에 정의된 `df -h` 가 아닌 `ps -aef` 가 실행된다. (`CMD` 덮어쓰게됨)

```bash
$ docker inspect ugi-df
...
				"Cmd": [
						"ps",
						"-aef"
				],
...
```

`docker inspect <image>` 의 `Cmd` 필드에서 설정 내용을 확인할 수 있다.

<br>

`ENTRYPOINT` 의 경우

```docker
FROM ubuntu
ENTRYPOINT ["/bin/df", "-h"]
```

```bash
$ docker build -t ugi/df:entry .
$ docker run --name ugi-df ugi/df:entry
```

`df -h` 의 실행결과가 나온다 `CMD` 의 경우와 다를게 없다. 하지만

```bash
$ docker inspect ugi-df
...
            "Cmd": null,
...

            "Entrypoint": [
                "/bin/df",
                "-h"
            ],
...
```

`docker inspect` 의 결과에서 차이점을 볼 수 있다.

<br>

현재 이미지에서 추가 인자를 넣어 다음과 같이 컨테이너를 실행해보면

```bash
$ docker run --name ugi-df ugi/df:entry ps -aef
```

에러를 출력하며 동작되지 않는다

```bash
 $ docker inspect ugi-df
 ...
            "Cmd": [
                "ps",
                "-aef"
            ],
 ...
            "Entrypoint": [
                "/bin/df",
                "-h"
            ],
...
```

동작이 `df -h ps -aef` 로 수행되어 에러를 출력된것을 확인할 수 있다.

정리하자면

- `CMD` : 컨테이너 실행시 설정될 기본 인자 설정 (실행시 인자값을 받아오면 덮어써짐)
- `ENTRYPOINT` : 컨테이너 실행시 고정적으로 실행될 인자 설정 ( `--entrypoint` 를 사용해야 덮어써짐)

<br>

## `EXPOSE`

```docker
EXPOSE <port> [<port>/<protocol>...]
```

이 컨테이너가 실행될 때 특정 네트워크 포트에서 수신 대기(Listen)한다는 것을 Docker에게 알린다.

포트가 TCP 혹은 UDP중 어떤 프로토콜을 사용하는지 지정할 수 있고 기본값은 TCP다.

실제로 포트를 외부에 공개하는 것이 아니라 **어떤 포트를 공개할 에정인지 알려주는 문서 역할**이다.

컨테이너 실행 시 **실제로 포트를 공개하려면**

`docker run -p` 를 사용하여 하나 이상의 포트를 공개하고 매핑하거나

`-P` 옵션을 사용하여 노출된 모든 포트를 공개하고 높은 번호의 포트와 매핑 해야한다.

<br>


```docker
EXPOSE 80/tcp
EXPOSE 80/udp
# 둘다 있으면 둘다 노출됨
```

단지 **문서 역할**이라 Dockerfile에 명시되어 있지 않더라도 실행 지점에 `-p` 옵션으로 재정의 가능하다.

`docker network` 명령은 특정 포트를 노출하거나 공개하지 않고도 컨테이너 간 통신을 위한 네트워크를 생성할 수 있다.

같은 네트워크에 연결된 컨테이너들은 어떤 포트든 서로 통신할 수 있기 때문이다.

<br>

## `VOLUME`

```docker
VOLUME ["/data"]
```

지정된 이름으로 mount point를 생성하고, 해당 위치가 호스트 또는 다른 컨테이너에서 외부적으로 마운트되는 볼륨을 저장하는 위치임을 표시한다.

<br>

```docker
FROM ubuntu

RUN mkdir /myvol
RUN echo "hello world" > /myvol/greeting

VOLUME /myvol
```

이 Dockerfile로 생성된 이미지는 `/myvol` 에 새로운 마운트 지점을 생성하고,

기존 이미지 내부에 있던 `greeting` 파일을 새로 생성된 볼륨으로 복사한다.

<br>

Dockerfile 내부에서 Volume을 다룰 때 주의해야 하는점이

1. 이미 mount point를 생성한 이후 해당 Volmue에 대한 변경사항이 생긴다면,
    - Legacy builder를 사용시 변경 사항은 버려진다.
    - BuildKit을 사용시 변경 사항이 유지된다.

1. Mount point(디렉토리)는 컨테이너 내부 위치로만 설정할 수 있다.
    - 실제 호스트 디렉토리로 지정할 경우 호스트 환경에따라 다르기 때문.
        - 호스트 이름도 다를것이고, 호스트의 작업 디렉토리의 위치도 다름
    - 호스트 디렉토리를 지정할 경우 Dockerfile이 아니라 `docker run -v` 를 사용해야한다
        - `docker run -v <host-dir>:<container-dir> image`

<br>

생성된 볼륨에 대한 링크는 다른 컨테이너 생성 시에 아래와 같이 연결한다.

```bash
docker run -v [볼륨 이름]:[컨테이너 내부 디렉토리 경로] --name [컨테이너 이름] [이미지 이름]
```

<br>

## `USER`

```docker
USER <user>[:<group>]
# or
USER UID[:<GID>]
```

현재 Build stage의 나머지 부분에서 사용할 기본 user와 group을 설정한다.

설정된 사용자는

- `RUN` 명령 실행 시
- 컨테이너 실행 시 `ENTRYPOINT` 와 `CMD` 명령 실행 시

에 사용된다.

<br>

사용자와 그룹을 함께 지정하면, 해당 사용자는 **지정한 그룹에만 속한 것으로 처리된다.**

이미 설정되어 있는 다른 그룹 멤버십은 모두 무시된다.

사용자가 **기본(primary) 그룹을 가지고 있지 않으면**, 이미지(또는 이후 명령)는 **root 그룹**으로 실행된다.

<br>

## `HEALTHCHECK`

이 명령은 두가지 형식을 가진다

- `HEALTHCHECK [OPTIONS] CMD command`
    - 컨테이너 내부에서 명령을 실행하여 컨테이너의 상태를 확인한다.
- `HEALTHCHECK NONE`
    - 베이스 이미지로부터 상속받은 `HEALTHCHECK` 를 비활성화 한다.

**컨테이너가 정상적으로 동작하고 있는지 Docker가 검사하는 방법**을 정의한다.

<br>

### `CMD` 앞에서 사용할 수 있는 옵션

- `-interval=DURATION`
    - 기본값: `30s`
- `-timeout=DURATION`
    - 기본값: `30s`
- `-start-period=DURATION`
    - 기본값: `0s`
- `-start-interval=DURATION`
    - 기본값: `5s`
- `-retries=N`
    - 기본값: `3`

---

[Dockfile reference](https://docs.docker.com/reference/dockerfile)

[Dockerfile COPY --link, 다들 쓴다는데 진짜 좋을까](https://daylog.frogset.com/481)

[Dockerfile Entrypoint와 CMD의 올바른 사용 방법](https://bluese05.tistory.com/77)

[[docker] 볼륨(volume)의 개념에 대해 알아보고 활용해봅시다.](https://formulous.tistory.com/17)
