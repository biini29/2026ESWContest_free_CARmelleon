# 스마트 시트 전체 결선도

```mermaid
flowchart TD

    %% =========================
    %% Raspberry Pi 3
    %% =========================

    PI["Raspberry Pi 3"]

    LCD["I2C LCD 16x2<br/>SDA: GPIO 2<br/>SCL: GPIO 3<br/>VCC: 5V<br/>GND: GND"]

    KEYPAD["4x4 Matrix Keypad<br/>COL1: GPIO 5<br/>COL2: GPIO 6<br/>COL3: GPIO 13<br/>COL4: GPIO 19<br/>ROW1: GPIO 26<br/>ROW2: GPIO 12<br/>ROW3: GPIO 16<br/>ROW4: GPIO 20"]

    PI -->|"I2C"| LCD
    PI -->|"GPIO"| KEYPAD


    %% =========================
    %% Arduino Mega 2560
    %% =========================

    ARD["Arduino Mega 2560"]

    PI -->|"USB / Serial + 전원"| ARD


    %% =========================
    %% HC-SR04 초음파 센서
    %% =========================

    ULTRA["HC-SR04 초음파 센서<br/>VCC: 5V<br/>GND: GND<br/>TRIG: D7<br/>ECHO: D8"]

    ARD -->|"D7 / D8"| ULTRA


    %% =========================
    %% L298N #1
    %% =========================

    L1["L298N #1<br/>ENB: D3<br/>IN1: D22<br/>IN2: D23"]

    M1["Linear Motor 1"]

    ARD -->|"PWM / 방향 제어"| L1
    L1 -->|"OUT3 / OUT4"| M1


    %% =========================
    %% L298N #2
    %% =========================

    L2["L298N #2<br/>ENA: D4<br/>ENB: D5<br/>IN1: D26<br/>IN2: D27<br/>IN3: D28<br/>IN4: D29"]

    M3["Linear Motor 3"]
    M4["Linear Motor 4"]

    ARD -->|"PWM / 방향 제어"| L2

    L2 -->|"OUT1 / OUT2"| M3
    L2 -->|"OUT3 / OUT4"| M4


    %% =========================
    %% L298N #3
    %% =========================

    L3["L298N #3<br/>ENA: D6<br/>ENB: D2<br/>IN1: D30<br/>IN2: D31<br/>IN3 / IN4: 확인 필요"]

    M5["Linear Motor 5"]
    M2["Linear Motor 2"]

    ARD -->|"PWM / 방향 제어"| L3

    L3 -->|"OUT1 / OUT2"| M5
    L3 -->|"OUT3 / OUT4"| M2


    %% =========================
    %% 리니어 모터 전원
    %% =========================

    SMPS["12V SMPS"]

    SMPS -->|"12V + GND"| L1
    SMPS -->|"12V + GND"| L2
    SMPS -->|"12V + GND"| L3


    %% =========================
    %% U2D2 / DYNAMIXEL
    %% =========================

    U2D2["U2D2"]

    HUB["U2D2 Power Hub"]

    DX1["DYNAMIXEL<br/>XL430-W250-T #1"]

    DX2["DYNAMIXEL<br/>XL430-W250-T #2"]

    PI -->|"USB"| U2D2

    U2D2 -->|"3핀 케이블"| HUB

    HUB -->|"3핀 케이블"| DX1
    HUB -->|"3핀 케이블"| DX2
```

---

## 주요 연결 요약

| 제어 장치 | 연결 대상 | 연결 방식 |
|---|---|---|
| Raspberry Pi 3 | Arduino Mega 2560 | USB |
| Raspberry Pi 3 | I2C LCD | GPIO 2 / GPIO 3 |
| Raspberry Pi 3 | 4×4 Matrix Keypad | GPIO |
| Raspberry Pi 3 | U2D2 | USB |
| Arduino Mega | HC-SR04 | D7 / D8 |
| Arduino Mega | L298N #1 | PWM + 방향 제어 |
| Arduino Mega | L298N #2 | PWM + 방향 제어 |
| Arduino Mega | L298N #3 | PWM + 방향 제어 |
| L298N #1 | Linear Motor 1 | OUT3 / OUT4 |
| L298N #2 | Linear Motor 3 | OUT1 / OUT2 |
| L298N #2 | Linear Motor 4 | OUT3 / OUT4 |
| L298N #3 | Linear Motor 2 | OUT3 / OUT4 |
| L298N #3 | Linear Motor 5 | OUT1 / OUT2 |
| U2D2 | U2D2 Power Hub | 3핀 케이블 |
| U2D2 Power Hub | DYNAMIXEL #1 | 3핀 케이블 |
| U2D2 Power Hub | DYNAMIXEL #2 | 3핀 케이블 |
| 12V SMPS | L298N #1 / #2 / #3 | 12V + GND |
