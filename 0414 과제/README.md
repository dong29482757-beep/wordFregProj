# NaverNewsCrawler

네이버 검색 API를 사용하여 뉴스 데이터를 수집하고, HTML 태그 등 노이즈를 제거하는 크롤러 클래스입니다.

## 주요 기능

✅ 네이버 뉴스 검색 API 연동  
✅ HTML 태그 자동 제거 (노이즈 제거)  
✅ HTML 엔티티 변환 (&quot;, &amp; 등)  
✅ CSV 파일 자동 저장  
✅ pandas DataFrame 지원  
✅ 에러 처리 및 재시도 로직  
✅ API 호출 제한 방지 (자동 대기)  

## 설치 방법

```bash
pip install pandas
```

## 사용 방법

### 1. 기본 사용법

```python
from NaverNewsCrawler import NaverNewsCrawler

# API 인증 정보
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"

# 크롤러 생성
crawler = NaverNewsCrawler(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    keyword="인공지능",
    display=10,        # 한 번에 가져올 개수
    max_results=100    # 최대 수집 개수
)

# 크롤링 실행
results = crawler.crawl_all()

# 결과 요약 출력
crawler.print_summary()

# CSV 저장
crawler.save_to_csv()
```

### 2. DataFrame으로 데이터 분석

```python
# DataFrame 가져오기
df = crawler.get_dataframe()

# 데이터 확인
print(df.head())
print(df.info())

# description 컬럼 활용
for desc in df['description']:
    print(desc)
```

### 3. 여러 키워드로 크롤링

```python
keywords = ["ChatGPT", "딥러닝", "머신러닝"]

for keyword in keywords:
    crawler = NaverNewsCrawler(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        keyword=keyword,
        max_results=50
    )
    
    crawler.crawl_all()
    crawler.save_to_csv(filename=f'{keyword}_news.csv')
```

## 클래스 메서드

### `__init__(client_id, client_secret, keyword, display=10, max_results=1000)`
크롤러 초기화

**Parameters:**
- `client_id` (str): 네이버 API Client ID
- `client_secret` (str): 네이버 API Client Secret
- `keyword` (str): 검색 키워드
- `display` (int): 한 번에 가져올 개수 (기본값: 10)
- `max_results` (int): 최대 수집 개수 (기본값: 1000)

### `crawl_all()`
모든 뉴스 데이터 수집

**Returns:**
- `list`: 수집된 뉴스 데이터 리스트

### `save_to_csv(filename=None, directory='./data')`
CSV 파일로 저장

**Parameters:**
- `filename` (str): 파일명 (None이면 자동 생성)
- `directory` (str): 저장 디렉토리 (기본값: './data')

**Returns:**
- `str`: 저장된 파일 경로

### `get_dataframe()`
DataFrame으로 변환

**Returns:**
- `pandas.DataFrame`: 뉴스 데이터 DataFrame

### `clean_data(item)`
노이즈 제거 (HTML 태그, 엔티티 변환)

**Parameters:**
- `item` (dict): 뉴스 아이템

**Returns:**
- `dict`: 노이즈가 제거된 뉴스 아이템

## 노이즈 제거 기능

### HTML 태그 제거
```
원본: <b>인공지능</b> 기술이 <em>발전</em>하고 있다
결과: 인공지능 기술이 발전하고 있다
```

### HTML 엔티티 변환
```
원본: &quot;AI&quot;는 &amp; 머신러닝
결과: "AI"는 & 머신러닝
```

### 연속 공백 제거
```
원본: 인공지능    기술     발전
결과: 인공지능 기술 발전
```

## 수집되는 데이터 필드

- `title`: 뉴스 제목 (노이즈 제거됨)
- `description`: 뉴스 요약/설명 (노이즈 제거됨) ← **과제에서 사용**
- `originallink`: 원본 기사 링크
- `link`: 네이버 뉴스 링크
- `pubDate`: 발행일

## 주의사항

⚠️ 네이버 API 사용 제한
- 일일 호출 한도: 25,000건
- 초당 호출 한도: 약 10건
- 자동으로 0.5초 대기 적용됨

⚠️ API 키 발급
- [네이버 개발자센터](https://developers.naver.com/)에서 발급
- Application 등록 후 Client ID/Secret 발급

## 파일 구조

```
.
├── NaverNewsCrawler.py    # 크롤러 클래스
├── example_usage.py       # 사용 예시
├── README.md              # 설명서
└── data/                  # CSV 저장 디렉토리 (자동 생성)
    ├── 인공지능_navernews_20240414_153025.csv
    └── 룰러_navernews_20240414_153130.csv
```

## 과제 활용 팁

### description 필드 사용하기

```python
# 크롤링
crawler = NaverNewsCrawler(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    keyword="인공지능"
)

crawler.crawl_all()

# DataFrame으로 가져오기
df = crawler.get_dataframe()

# description만 추출
descriptions = df['description'].tolist()

# description으로 텍스트 분석
for desc in descriptions:
    print(desc)
    # 여기서 텍스트 분석, 감정 분석, 키워드 추출 등 수행
```

## 라이센스

MIT License
