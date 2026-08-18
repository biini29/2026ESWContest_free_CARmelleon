
# 전체 시스템 구성 요약

## 1. HW/SW 스택 요약

| 구분 | 구성 |
|---|---|
| 상위 제어기 | Raspberry Pi 3 (ROS 2 Humble) |
| 하위 제어기 | Arduino Mega |
| 프레임워크 | ROS 2 Humble, rclpy(Python) |
| 등받이 구동 | 리니어 액추에이터 5개 + L298N 드라이버 3개 |
| 안전벨트 구동 | Dynamixel XL430-W250-T 2개 + U2D2 Power Hub Board |
| 입력 | 4x4 매트릭스 키패드, HC-SR04 초음파 센서 |
| 출력 | I2C LCD 16x2 |
| 전원 | 12V SMPS(모터 계통), 12V/5V 겸용 어댑터(라즈베리파이 전용, 완전 독립 계통) |
| 통신 | USB Serial(Pi↔Arduino, 115200bps), USB(Pi↔U2D2, Dynamixel Protocol 2.0, 1,000,000bps), GPIO(키패드/LCD/초음파) |

상세 부품 목록은 [`03_Hardware/01_하드웨어_사용_부품_목록표.md`](../../03_Hardware/01_하드웨어_사용_부품_목록표.md) 참고.

## 2. 상위/하위 제어기 역할 분담

### Raspberry Pi (상위 제어기)
- ROS 2 노드 5개 전체 실행 (`keypad_node`, `profile_inference_node`, `seat_controller_node`, `belt_controller_node`, `arduino_bridge_node`)
- 체형 데이터 계산(회귀식, 가우시안 곡선)
- 키패드/LCD/초음파 센서 직접 제어 (GPIO)
- 다이나믹셀 직접 제어 (U2D2를 통한 Protocol 2.0 통신)
- Arduino에 시리얼로 모터 명령 전달

### Arduino Mega (하위 제어기)
- Raspberry Pi로부터 받은 `M,모터번호,방향,속도` 명령을 해석
- L298N 드라이버 3개를 통해 리니어 액추에이터 5개의 PWM 속도·방향 직접 제어
- 위치 피드백 센서가 없어, 모터별 실측 속도(mm/s) 기반 시간 제어로 위치를 추정

> 다이나믹셀(안전벨트)은 Arduino를 거치지 않고 Raspberry Pi가 U2D2를 통해 직접 제어한다 — 등받이(리니어)와 벨트(다이나믹셀)는 완전히 분리된 두 개의 구동 경로다.

## 3. 데이터 흐름 개요

```
입력(키패드/초음파) → 체형 데이터 계산 → 목표값 산출
                                              ├─→ 등받이 구동 (Pi → Arduino → L298N → 액추에이터5개)
                                              └─→ 벨트 구동 (Pi → U2D2 → 다이나믹셀2개)
```

더 상세한 노드/토픽 구조는 [`04_Software/01_Ros_Architecture.md`](../../04_Software/01_Ros_Architecture.md), 계산 알고리즘은 [`04_Software/02_Seat_Control_Algorithm.md`](../../04_Software/02_Seat_Control_Algorithm.md) 참고.

## 4. 상위 개념도

전체 기능 블록 흐름은 [`06_Demo/01_System_Block_Diagram.md`](../../06_Demo/01_System_Block_Diagram.md), 전기적 배선/전원 계통은 [`electrical/`](../electrical/) 폴더 참고.
