# SimpleScalar 시뮬레이션 설정 및 데이터 수집 가이드

## 1. 개요
이 문서는 SimpleScalar를 사용하여 캐시 구성에 따른 성능 분석을 위한 설정 파일 생성 및 데이터 수집 방법을 설명합니다.

## 2. 설정 파일 자동 생성
### 2.1 Config Generator 스크립트
Config Generator는 다양한 캐시 구성에 대한 설정 파일을 자동으로 생성하는 Python 스크립트입니다.

### 2.2 파라미터 수정 방법
스크립트 상단의 파라미터를 수정하여 원하는 설정을 변경할 수 있습니다:
```python
# Parameters
block_sizes = [32, 64, 128]           # 캐시 블록 크기 설정
associativities = [2, 4, 8]           # 연관도 설정
applications = ['anagram', 'compress95', 'go']  # 테스트할 애플리케이션
policy = 'r'                          # 교체 정책 (r: Random, l: LRU, f: FIFO)
```

### 2.3 시뮬레이터 설정 수정 방법
generate_config() 함수 내의 설정을 수정하여 시뮬레이터 파라미터를 변경할 수 있습니다:
```python
# 예시: decode width 변경
-decode:width                     4    # 4를 원하는 값으로 변경

# 예시: issue width 변경
-issue:width                      4    # 4를 원하는 값으로 변경

# 예시: cache 설정 변경
-cache:dl1   dl1:128:{block_size}:{assoc}:{policy}  # 128을 원하는 캐시 크기로 변경
```

### 2.4 스크립트 실행 방법
```bash
python3 config_generator.py
```

## 3. 새로운 애플리케이션 추가
### 3.1 애플리케이션 추가 방법
1. applications 리스트에 새로운 애플리케이션 이름 추가
2. run.sh 스크립트에 새로운 애플리케이션을 위한 섹션 추가:
```bash
# Run new_application configurations
for config in new_application_b*_random.cfg; do
    echo "Running $config..."
    ./sim-outorder -config $config benchmarks/new_application.alpha [추가 인자] 2>&1 | tee "results/${config%.cfg}_output.txt"
    echo "----------------------------------------"
done
```

### 3.2 실행 명령어 수정
각 애플리케이션의 실행 명령어 형식:
- anagram: `benchmarks/anagram.alpha benchmarks/words < benchmarks/anagram.in`
- compress95: `benchmarks/compress95.alpha < benchmarks/compress95.in`
- go: `benchmarks/go.alpha 50 9 benchmarks/2stone9.in`
- 새로운 애플리케이션: 해당 애플리케이션의 필요한 인자 구성

# SimpleScalar 시뮬레이션 데이터 수집 가이드

## 1. 개요
이 문서는 SimpleScalar를 사용하여 캐시 구성에 따른 성능 분석 데이터를 수집하는 방법을 설명합니다.

## 2. 설정 파일 생성
### 2.1 테스트할 캐시 구성
- Block size: 32B, 64B, 128B
- Associativity: 2-way, 4-way, 8-way
- Replacement policy: Random
- 테스트할 애플리케이션: anagram, compress95, go

### 2.2 설정 파일 생성 방법
1. 기존 cfg 파일을 템플릿으로 사용
```bash
cp T1_anagram.cfg anagram_b32_a2_random.cfg
```

2. 캐시 설정 수정
- dl1과 dl2 캐시의 설정을 수정
- 형식: dl1:size:block_size:associativity:replacement_policy
```
-cache:dl1             dl1:128:32:2:r
-cache:dl2             ul2:1024:32:2:r
```

## 3. 데이터 수집 자동화
### 3.1 스크립트 생성
아래 내용으로 `run.sh` 파일을 생성:
```bash
#!/bin/bash

# Create results directory if it doesn't exist
mkdir -p results

# Run anagram configurations
for config in anagram_b*_random.cfg; do
    echo "Running $config..."
    ./sim-outorder -config $config benchmarks/anagram.alpha benchmarks/words < benchmarks/anagram.in 2>&1 | tee "results/${config%.cfg}_output.txt"
    echo "----------------------------------------"
done

# Run compress95 configurations
for config in compress95_b*_random.cfg; do
    echo "Running $config..."
    ./sim-outorder -config $config benchmarks/compress95.alpha < benchmarks/compress95.in 2>&1 | tee "results/${config%.cfg}_output.txt"
    echo "----------------------------------------"
done

# Run go configurations
for config in go_b*_random.cfg; do
    echo "Running $config..."
    ./sim-outorder -config $config benchmarks/go.alpha 50 9 benchmarks/2stone9.in 2>&1 | tee "results/${config%.cfg}_output.txt"
    echo "----------------------------------------"
done

echo "All simulations completed. Results are saved in results directory"
```

### 3.2 스크립트 실행 방법
1. 스크립트에 실행 권한 부여
```bash
chmod +x run.sh
```

2. 스크립트 실행
```bash
./run.sh
```

## 4. 결과 확인
### 4.1 결과 파일 위치
- 모든 결과는 results 디렉토리에 저장됨
- 파일명 형식: [application]_b[block_size]_a[associativity]_random_output.txt

### 4.2 수집되는 주요 데이터
- sim_num_insn: 총 명령어 수
- sim_num_loads: 로드/스토어 명령어 수
- sim_num_branches: 분기 명령어 수
- sim_cycle: 총 시뮬레이션 사이클
- sim_IPC: 사이클당 명령어 수
- sim_CPI: 명령어당 사이클 수

## 5. 주의사항
- 각 시뮬레이션은 상당한 시간이 소요될 수 있음
- 모든 결과는 자동으로 파일로 저장되며 동시에 화면에도 출력됨
- 시뮬레이션 중간에 중단된 경우, 해당 설정만 다시 실행 가능

## 6. 문제 해결
만약 결과가 제대로 저장되지 않는 경우:
1. 입력/출력 리다이렉션이 올바른지 확인
2. 권한 설정 확인
3. 디스크 공간 확인  
## 7. 자주 발생하는 오류 및 해결방법
### 7.1 설정 파일 생성 관련
- Permission denied: `chmod +x config_generator.py` 실행
- ModuleNotFoundError: Python itertools 모듈 설치 확인
- UnicodeEncodeError: 파일 인코딩이 UTF-8인지 확인

### 7.2 시뮬레이션 실행 관련
- Command not found: 실행 권한 확인
- Input file not found: 벤치마크 파일 경로 확인
- Invalid configuration: 설정 파일 형식 확인

## 8. 팁과 추천사항
- 설정 변경 전 기존 설정 백업
- 소규모 테스트 후 전체 실행
- 디스크 공간 여유 확인
- 장시간 실행 시 nohup 사용 고려
