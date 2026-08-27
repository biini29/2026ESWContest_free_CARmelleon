
# 문서 목차

가변형 스마트시트(Family Care) 프로젝트의 전체 개발 문서입니다. 아래 순서대로 읽으시면 프로젝트를 처음부터 이해할 수 있습니다.

## 📋 [01_Project_Overview](./01_Project_Overview/)
개발 배경, 목표, 사용 시나리오, 팀 구성, 전체 개발 일정을 담고 있습니다. **여기부터 읽으시는 걸 추천합니다.**

- [01_Background_and_Goal.md](./01_Project_Overview/01_Background_and_Goal.md) — 개발 배경 및 목표
- [02_System_Architecture_Overview.md](./01_Project_Overview/02_System_Architecture_Overview.md) — 전체 시스템 구성 요약
- [03_Team_Roles_and_Schedule.md](./01_Project_Overview/03_Team_Roles_and_Schedule.md) — 팀원 역할 및 개발 일정

## 🎨 [02_Design](./02_Design/)
전기·기구 설계 문서입니다.

- [electrical/](./02_Design/electrical/) — 전원 계통도, 전체 결선도, Arduino/L298N 핀맵
- [mechanical/](./02_Design/mechanical/) — 3D 모델(조립도, 부품별 CAD), third-party CAD 출처

## 🔧 [03_Hardware](./03_Hardware/)
사용한 하드웨어 부품 목록(BOM)과 실제 구매 비용을 정리했습니다.

## 💻 [04_Software](./04_Software/)
ROS 2 소프트웨어 구조와 핵심 알고리즘 문서입니다.

- [01_Ros_Architecture.md](./04_Software/01_Ros_Architecture.md) — 노드 구성, 토픽/메시지 구조
- [02_Seat_Control_Algorithm.md](./04_Software/02_Seat_Control_Algorithm.md) — 회귀식, 가우시안 곡선, 벨트 계산식
- [03_Arduino_Ros_Protocol.md](./04_Software/03_Arduino_Ros_Protocol.md) — Arduino ↔ ROS 2 시리얼 프로토콜

## 🧪 [05_Test](./05_Test/)
개발 중 발생한 장애요인과 해결방안을 정리한 트러블슈팅 로그입니다.

## 🎬 [06_Demo](./06_Demo/)
시스템 블록 다이어그램, 하드웨어 실물 사진, 시연 영상입니다.

---

## 관련 코드

- [`../src/`](../src/) — ROS 2 노드 5개 소스코드
- [`../launch/`](../launch/) — 전체 시스템 실행 launch 파일
- [`../msg/`](../msg/) — 커스텀 메시지 정의
- [`../scripts/`](../scripts/) — `keypad_node.py` 내 세 기능(게스트모드, 프로필관리, 초음파필터) 설명 문서

전체 프로젝트 개요는 저장소 최상위 [README.md](../README.md)를 참고하세요.
