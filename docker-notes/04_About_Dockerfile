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

---

https://docs.docker.com/reference/dockerfile

https://daylog.frogset.com/481
