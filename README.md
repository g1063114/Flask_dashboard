# Python을 활용한 통합 페이지 구현 및 데이터 분석 대시보드 프로젝트

기존 메일 전송 방식에서 통합 페이지 구현으로 업무 생산성 향상

사용한 기술

Python3, Flask Framework, ORM

# Flask_dashboard
flask_dashboard

localhost test complete

개발 서버로 이관 방안 연구...
sqllite -> oracle??

apache 연동

첫번째 시도
1. 서버에 가상환경 세팅
2. Apache 다운
3. pip install mod_wsgi
4. cmd -> mod_wsgi-express module-config
5. httpd.conf 설정
6. 포트 번호 설정
7. .wsgi 파일 생성
8. 서버 실행

문제 발생 
1. pip install mod_wsgi 다운로드 할 때 오류 발생
   -> vc14++ 컴파일러가 없다는 에러 발생...
   -> visual studio tools로 MSVS v140 - VS 2015 C++ 빌드 도구 다운로드 (구글 검색)
   -> 해결 되어야 하는데 계속 오류...
   -> 구글링 중 mod_wsgi가 32bit만 지원하는거 같음 (스택오버플로우 검색)
   -> python 32bit, apache 32bit로 다시 다운로드
   -> pip install mod_wsgi 성공!!