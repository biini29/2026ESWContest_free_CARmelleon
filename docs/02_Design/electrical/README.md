# Electrical Subsystem — 개요

전원, 통신, 센서/액추에이터 배선을 다루는 전기 서브시스템 문서입니다. 상세 핀맵은 [`03_Pinout_Table.md`](./03_Pinout_Table.md), 전체 회로도는 [`전원계통도_및_전체_결선도.png`](./전원계통도_및_전체_결선도.png)를 참고하세요.

---

## 1. 전원 계통 (2개 독립 라인)

| 전원 | 대상 | 비고 |
|---|---|---|
| 5V 전원 어댑터 (다이소, 12V/5V 겸용) | Raspberry Pi 3 전용 | 12V SMPS 계통과 완전히 독립된 별도 전원선. 스텝모터 구동 중 저전압 증상이 있었으나 원인은 스텝모터 전류 소모였음(어댑터 자체 문제 아님) — 다이나믹셀 교체 후 해소 |
| 12V SMPS | L298N 드라이버 3개 + U2D2 Power Hub Board | 모터/서보 구동 전원, Pi/Arduino 로직 전원과 분리 |

**⚠️ 공통 접지(GND) 필수**: Raspberry Pi · Arduino Mega · L298N × 3 · 12V SMPS · U2D2의 GND는 모두 하나로 묶여야 합니다. 분리되어 있으면 시리얼 통신 오류나 센서 오작동의 원인이 됩니다.

---

## 2. 통신 계통

| 연결 | 방식 | 고정 장치명 | 비고 |
|---|---|---|---|
| Pi ↔ Arduino Mega | USB Serial, 115200bps | `/dev/arduino_linear` | `M,모터,방향,속도` 프로토콜 |
| Pi ↔ U2D2 | USB, Dynamixel Protocol 2.0, 1,000,000bps | `/dev/belt_u2d2` | GroupSyncWrite로 동시 제어 |
| Pi GPIO ↔ 키패드 4x4 | 폴링 방식(50ms) | — | Row 4핀 OUT, Col 4핀 IN(PUD_DOWN) |
| Pi GPIO(I2C) ↔ LCD | I2C, 주소 0x27 | — | SDA=GPIO2, SCL=GPIO3 |
| Pi GPIO ↔ HC-SR04 | TRIG/ECHO 폴링 | — | TRIG=GPIO23, ECHO=GPIO24 |

### USB 장치명이 고정된 이유

USB 재연결·재부팅마다 `/dev/ttyUSB0/1/2` 번호가 바뀌어 연결 실패가 반복되던 문제를, `udev` 규칙(장치의 USB Vendor/Product ID + 시리얼 번호 기준)으로 고정 심볼릭 링크를 부여해 해결했습니다. 코드에서는 `/dev/ttyUSB*`가 아니라 반드시 `/dev/arduino_linear`, `/dev/belt_u2d2`를 참조합니다.

---

## 3. 주의사항

### HC-SR04 ECHO 핀 레벨시프트

HC-SR04의 ECHO 출력은 5V인데, Raspberry Pi GPIO는 3.3V 입력 기준입니다. **ECHO를 GPIO에 직결하면 장기적으로 GPIO 손상 위험이 있습니다.** 저항 분배(예: 1kΩ + 2kΩ) 또는 레벨시프터를 거치는 것을 권장하며, 현재 구성에서 이 부분을 확인이 필요합니다.

### Arduino Mega 스케치 관리

Arduino에는 리니어 액추에이터 전용 스케치가 항상 올라가 있어야 합니다. 개발 중 다른 테스트 스케치를 업로드한 뒤 리니어 전용 스케치로 되돌리지 않아 전체 시스템이 응답하지 않았던 사고가 있었습니다 — 스케치를 바꿔 테스트할 경우, 작업 종료 시 반드시 리니어 전용 스케치로 재업로드해야 합니다.

### 다이나믹셀 보드레이트

기본값(57600)이 아니라 **1,000,000bps**로 설정되어 있습니다. 다른 보드레이트로는 ping조차 응답하지 않습니다.

---

## 4. 관련 문서

- [`03_Pinout_Table.md`](./03_Pinout_Table.md) — Arduino/L298N 상세 핀맵
- [`전원계통도_및_전체_결선도_통합.md`](./전원계통도_및_전체_결선도_통합.md) — 통합 회로도
- [`03_Arduino_Ros_Protocol.md`](../../04_Software/03_Arduino_Ros_Protocol.md) — 시리얼 프로토콜 명세
- [`01_하드웨어_사용_부품_목록표.md`](../../03_Hardware/01_하드웨어_사용_부품_목록표.md) — 부품 목록(BOM)
