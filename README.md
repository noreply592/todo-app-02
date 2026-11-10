# 할일 관리 웹앱 (Flask)

## 로컬 실행

```
pip install -r requirements.txt
python app.py
```

브라우저에서 http://127.0.0.1:5000 접속

## 기능
- 할일 추가 / 완료 체크 / 삭제
- 제목 클릭 후 수정하고 Enter로 저장
- 전체 / 진행중 / 완료 필터
- 완료된 항목 한번에 지우기
- 데이터는 브라우저 localStorage에 저장 (브라우저마다 따로 저장됨)

## 배포
Vercel에 배포되어 있으며, `main` 브랜치에 push하면 자동으로 다시 배포됩니다.
