Ubuntu 22.04에서 `sudo apt update` 명령을 실행할 때 발생하는 "Hash Sum mismatch" 오류는 패키지 인덱스 파일이 손상되었거나, 다운로드 중 문제가 발생했을 때 나타나는 오류입니다. 이 문제를 해결하기 위해 다음 단계를 따라 보세요:

### 1. 패키지 캐시 정리
먼저, 로컬에 저장된 패키지 캐시를 정리합니다.

```bash
sudo apt clean
```

이 명령은 로컬에 저장된 모든 패키지 캐시를 삭제합니다.

### 2. 패키지 리스트 다시 다운로드
패키지 리스트를 다시 다운로드합니다.

```bash
sudo apt update
```

이 명령은 패키지 리스트를 다시 다운로드하여 최신 상태로 만듭니다.

### 3. 문제가 지속될 경우, 캐시 강제 삭제
만약 문제가 계속된다면, `/var/lib/apt/lists` 디렉토리에 있는 모든 파일을 삭제하고 다시 시도해 보세요.

```bash
sudo rm -rf /var/lib/apt/lists/*
sudo apt update
```

이 명령은 패키지 리스트를 저장하는 디렉토리의 모든 파일을 삭제하고, 다시 패키지 리스트를 다운로드합니다.

### 4. 미러 서버 변경
위의 방법으로도 해결되지 않는다면, 사용 중인 미러 서버에 문제가 있을 수 있습니다. 다른 미러 서버로 변경해 보세요.

1. `/etc/apt/sources.list` 파일을 편집합니다.

   ```bash
   sudo nano /etc/apt/sources.list
   ```

2. `kr.archive.ubuntu.com` 대신 `archive.ubuntu.com` 또는 다른 미러 서버로 변경합니다. 예를 들어:

   ```plaintext
   deb http://archive.ubuntu.com/ubuntu/ jammy main restricted
   deb http://archive.ubuntu.com/ubuntu/ jammy-updates main restricted
   ```

3. 파일을 저장하고 나옵니다.

4. 다시 패키지 리스트를 업데이트합니다.

   ```bash
   sudo apt update
   ```

### 5. 네트워크 문제 확인
네트워크 연결이 불안정할 경우에도 이런 문제가 발생할 수 있습니다. 네트워크 연결을 확인하고, 가능하다면 다른 네트워크를 사용해 보세요.

위의 방법들을 시도한 후에도 문제가 해결되지 않는다면, 추가적인 로그나 오류 메시지를 확인하여 더 깊이 있는 문제 해결이 필요할 수 있습니다.