# 스마트 시트 핀맵 (Pin Map)

## 1. 개요

본 문서는 스마트 시트 시스템에 사용되는 각 장치의 제어 핀 및 통신 연결 정보를 정리한다.

### 시스템 구성

| 장치                        | 수량 | 역할                 |
| ------------------------- | -: | ------------------ |
| Raspberry Pi              |  1 | 메인 컨트롤러 / ROS 2 실행 |
| Arduino Mega 2560         |  1 | 리니어 모터 및 초음파 센서 제어 |
| L298N Motor Driver        |  3 | 리니어 모터 구동          |
| Linear Motor              |  5 | 등받이 위치 조절          |
| HC-SR04 Ultrasonic Sensor |  1 | 거리 측정              |
| 4×4 Matrix Keypad         |  1 | 사용자 입력             |
| I2C LCD 16×2              |  1 | 상태 및 안내 표시         |
| U2D2                      |  1 | DYNAMIXEL 통신       |
| U2D2 Power Hub            |  1 | DYNAMIXEL 전원 공급    |
| DYNAMIXEL XL430-W250-T    |  2 | 안전벨트 제어            |

---

# 2. Arduino Mega 2560 Pin Map

Arduino Mega 2560은 5개의 리니어 모터와 초음파 센서를 제어한다.

## 2.1 리니어 모터 제어 핀

| Arduino Pin | 연결 장치    | 연결 핀 | 기능                   |
| ----------- | -------- | ---- | -------------------- |
| D2          | L298N #1 | ENA  | Linear Motor 1 PWM   |
| D3          | L298N #1 | ENB  | Linear Motor 2 PWM   |
| D4          | L298N #2 | ENA  | Linear Motor 3 PWM   |
| D5          | L298N #2 | ENB  | Linear Motor 4 PWM   |
| D6          | L298N #3 | ENA  | Linear Motor 5 PWM   |
| D22         | L298N #1 | IN1  | Linear Motor 1 방향 제어 |
| D23         | L298N #1 | IN2  | Linear Motor 1 방향 제어 |
| D24         | L298N #1 | IN3  | Linear Motor 2 방향 제어 |
| D25         | L298N #1 | IN4  | Linear Motor 2 방향 제어 |
| D26         | L298N #2 | IN1  | Linear Motor 3 방향 제어 |
| D27         | L298N #2 | IN2  | Linear Motor 3 방향 제어 |
| D28         | L298N #2 | IN3  | Linear Motor 4 방향 제어 |
| D29         | L298N #2 | IN4  | Linear Motor 4 방향 제어 |
| D30         | L298N #3 | IN1  | Linear Motor 5 방향 제어 |
| D31         | L298N #3 | IN2  | Linear Motor 5 방향 제어 |

---

## 2.2 L298N #1

| L298N Pin | Arduino Mega | 대상             |
| --------- | ------------ | -------------- |
| ENA       | D2           | Linear Motor 1 |
| IN1       | D22          | Linear Motor 1 |
| IN2       | D23          | Linear Motor 1 |
| ENB       | D3           | Linear Motor 2 |
| IN3       | D24          | Linear Motor 2 |
| IN4       | D25          | Linear Motor 2 |

---

## 2.3 L298N #2

| L298N Pin | Arduino Mega | 대상             |
| --------- | ------------ | -------------- |
| ENA       | D4           | Linear Motor 3 |
| IN1       | D26          | Linear Motor 3 |
| IN2       | D27          | Linear Motor 3 |
| ENB       | D5           | Linear Motor 4 |
| IN3       | D28          | Linear Motor 4 |
| IN4       | D29          | Linear Motor 4 |

---

## 2.4 L298N #3

| L298N Pin | Arduino Mega | 대상             |
| --------- | ------------ | -------------- |
| ENA       | D6           | Linear Motor 5 |
| IN1       | D30          | Linear Motor 5 |
| IN2       | D31          | Linear Motor 5 |
| ENB       | 미사용          | -              |
| IN3       | 미사용          | -              |
| IN4       | 미사용          | -              |

---

# 3. Linear Motor 배치

5개의 리니어 모터는 모두 스마트 시트 등받이에 배치된다.

| Motor          |     위치 | Driver   | 제어 핀         |
| -------------- | -----: | -------- | ------------ |
| Linear Motor 1 | 150 mm | L298N #1 | D2, D22, D23 |
| Linear Motor 2 | 320 mm | L298N #1 | D3, D24, D25 |
| Linear Motor 3 | 490 mm | L298N #2 | D4, D26, D27 |
| Linear Motor 4 | 660 mm | L298N #2 | D5, D28, D29 |
| Linear Motor 5 | 830 mm | L298N #3 | D6, D30, D31 |

> 5개의 모터는 위치에 따라 고정된 역할을 갖지 않는다.
> 각 모터의 위치를 기준으로 Gaussian Curve를 계산하여 사용자 체형에 따른 목표값을 결정한다.

---

# 4. HC-SR04 Ultrasonic Sensor

HC-SR04 초음파 센서는 Arduino Mega 2560에 연결한다.

| HC-SR04 Pin | Arduino Mega | 기능     |
| ----------- | ------------ | ------ |
| VCC         | 5V           | 전원     |
| GND         | GND          | 접지     |
| TRIG        | D7           | 초음파 송신 |
| ECHO        | D8           | 초음파 수신 |

### Arduino 설정

```cpp
#define TRIG_PIN 7
#define ECHO_PIN 8
```

---

# 5. Raspberry Pi Pin Map

Raspberry Pi는 ROS 2 기반 메인 컨트롤러로 사용하며 LCD, Matrix Keypad, Arduino Mega, U2D2와 연결된다.

---

## 5.1 I2C LCD 16×2

| LCD Pin | Raspberry Pi | Physical Pin | 기능      |
| ------- | ------------ | -----------: | ------- |
| VCC     | 5V           |        Pin 2 | 전원      |
| GND     | GND          |        Pin 6 | 접지      |
| SDA     | GPIO 2       |        Pin 3 | I2C 데이터 |
| SCL     | GPIO 3       |        Pin 5 | I2C 클럭  |

### LCD 설정

```text
I2C Address : 0x27
Interface   : I2C
```

---

## 5.2 4×4 Matrix Keypad

4×4 Matrix Keypad는 Raspberry Pi GPIO를 이용하여 사용자 입력을 처리한다.

| Keypad Pin | Raspberry Pi GPIO | 기능       |
| ---------- | ----------------: | -------- |
| COL1       |            GPIO 5 | Column 1 |
| COL2       |            GPIO 6 | Column 2 |
| COL3       |           GPIO 13 | Column 3 |
| COL4       |           GPIO 19 | Column 4 |
| ROW1       |           GPIO 26 | Row 1    |
| ROW2       |           GPIO 12 | Row 2    |
| ROW3       |           GPIO 16 | Row 3    |
| ROW4       |           GPIO 20 | Row 4    |

### GPIO 요약

```text
COL1 → GPIO 5
COL2 → GPIO 6
COL3 → GPIO 13
COL4 → GPIO 19

ROW1 → GPIO 26
ROW2 → GPIO 12
ROW3 → GPIO 16
ROW4 → GPIO 20
```

---

# 6. U2D2 / DYNAMIXEL Pin Map

DYNAMIXEL XL430-W250-T 2개는 U2D2를 통해 Raspberry Pi에서 제어한다.

| 장치             | 연결 대상          | 연결 방식         | 기능           |
| -------------- | -------------- | ------------- | ------------ |
| Raspberry Pi   | U2D2           | USB           | DYNAMIXEL 통신 |
| U2D2           | U2D2 Power Hub | DYNAMIXEL Bus | 통신/전원 연결     |
| U2D2 Power Hub | XL430 #1       | DYNAMIXEL Bus | 안전벨트 제어      |
| U2D2 Power Hub | XL430 #2       | DYNAMIXEL Bus | 안전벨트 제어      |

### U2D2 통신 포트

```text
Device Port : /dev/ttyUSB1
```

### 통신 구조

```text
Raspberry Pi
     │
     │ USB
     ▼
   U2D2
     │
     ▼
U2D2 Power Hub
     │
     ├── XL430-W250-T #1
     │
     └── XL430-W250-T #2
```

---

# 7. Raspberry Pi ↔ Arduino Mega

Raspberry Pi와 Arduino Mega는 USB Serial을 통해 통신한다.

| 장치           | 연결 방식      | 기능              |
| ------------ | ---------- | --------------- |
| Raspberry Pi | USB        | Arduino Mega 연결 |
| Arduino Mega | USB Serial | ROS 2와 데이터 통신   |

### 통신 구조

```text
Raspberry Pi
      │
      │ USB Serial
      ▼
Arduino Mega 2560
      │
      ├── L298N #1 → Linear Motor 1, 2
      ├── L298N #2 → Linear Motor 3, 4
      ├── L298N #3 → Linear Motor 5
      └── HC-SR04
```

---

# 8. Arduino Mega 전체 핀 요약

| Pin | 연결 장치        | 기능          |
| --- | ------------ | ----------- |
| D2  | L298N #1 ENA | Motor 1 PWM |
| D3  | L298N #1 ENB | Motor 2 PWM |
| D4  | L298N #2 ENA | Motor 3 PWM |
| D5  | L298N #2 ENB | Motor 4 PWM |
| D6  | L298N #3 ENA | Motor 5 PWM |
| D7  | HC-SR04 TRIG | 거리 측정       |
| D8  | HC-SR04 ECHO | 거리 측정       |
| D22 | L298N #1 IN1 | Motor 1 방향  |
| D23 | L298N #1 IN2 | Motor 1 방향  |
| D24 | L298N #1 IN3 | Motor 2 방향  |
| D25 | L298N #1 IN4 | Motor 2 방향  |
| D26 | L298N #2 IN1 | Motor 3 방향  |
| D27 | L298N #2 IN2 | Motor 3 방향  |
| D28 | L298N #2 IN3 | Motor 4 방향  |
| D29 | L298N #2 IN4 | Motor 4 방향  |
| D30 | L298N #3 IN1 | Motor 5 방향  |
| D31 | L298N #3 IN2 | Motor 5 방향  |

---

# 9. Raspberry Pi 전체 핀 요약

| Physical Pin |    GPIO | 연결 장치        | 기능           |
| -----------: | ------: | ------------ | ------------ |
|        Pin 2 |      5V | LCD          | 전원           |
|        Pin 3 |  GPIO 2 | LCD SDA      | I2C 데이터      |
|        Pin 5 |  GPIO 3 | LCD SCL      | I2C 클럭       |
|        Pin 6 |     GND | LCD          | 접지           |
|            - |  GPIO 5 | Keypad COL1  | Column 1     |
|            - |  GPIO 6 | Keypad COL2  | Column 2     |
|            - | GPIO 13 | Keypad COL3  | Column 3     |
|            - | GPIO 19 | Keypad COL4  | Column 4     |
|            - | GPIO 26 | Keypad ROW1  | Row 1        |
|            - | GPIO 12 | Keypad ROW2  | Row 2        |
|            - | GPIO 16 | Keypad ROW3  | Row 3        |
|            - | GPIO 20 | Keypad ROW4  | Row 4        |
|          USB |       - | Arduino Mega | Serial 통신    |
|          USB |       - | U2D2         | DYNAMIXEL 통신 |

---

# 10. 전체 시스템 핀 연결 구조

```text
                         ┌──────────────────────┐
                         │    Raspberry Pi      │
                         │       ROS 2          │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │ USB                 │ USB                 │ GPIO / I2C
              ▼                     ▼                     ▼
       ┌──────────────┐       ┌──────────┐       ┌──────────────┐
       │ Arduino Mega │       │  U2D2    │       │ LCD / Keypad │
       └──────┬───────┘       └────┬─────┘       └──────────────┘
              │                    │
       ┌──────┼──────┐             ▼
       │      │      │       ┌──────────────┐
       ▼      ▼      ▼       │ U2D2 Power   │
    L298N #1 L298N #2 L298N  │     Hub      │
       │      │      │       └──────┬───────┘
      M1 M2  M3 M4   M5             │
                                    ├── XL430 #1
                                    └── XL430 #2

              Arduino Mega
                   │
                   ▼
                HC-SR04
```

---

# 11. 핀 사용 현황

## Arduino Mega

```text
D2  → L298N #1 ENA → Motor 1 PWM
D3  → L298N #1 ENB → Motor 2 PWM

D4  → L298N #2 ENA → Motor 3 PWM
D5  → L298N #2 ENB → Motor 4 PWM

D6  → L298N #3 ENA → Motor 5 PWM

D7  → HC-SR04 TRIG
D8  → HC-SR04 ECHO

D22 → L298N #1 IN1
D23 → L298N #1 IN2
D24 → L298N #1 IN3
D25 → L298N #1 IN4

D26 → L298N #2 IN1
D27 → L298N #2 IN2
D28 → L298N #2 IN3
D29 → L298N #2 IN4

D30 → L298N #3 IN1
D31 → L298N #3 IN2
```

## Raspberry Pi

```text
Pin 2 / 5V       → LCD VCC
Pin 3 / GPIO 2   → LCD SDA
Pin 5 / GPIO 3   → LCD SCL
Pin 6 / GND      → LCD GND

GPIO 5           → Keypad COL1
GPIO 6           → Keypad COL2
GPIO 13          → Keypad COL3
GPIO 19          → Keypad COL4

GPIO 26          → Keypad ROW1
GPIO 12          → Keypad ROW2
GPIO 16          → Keypad ROW3
GPIO 20          → Keypad ROW4

USB              → Arduino Mega
USB              → U2D2 (/dev/ttyUSB1)
```

---

# 12. 핀맵 관리 기준

* 본 문서는 각 장치의 **핀 번호 및 신호 연결 정보**를 관리한다.
* 전원 공급 구조는 `전원 계통도.md`에서 관리한다.
* 실제 부품 간 물리적 배선은 `결선도.md`에서 관리한다.
* Raspberry Pi GPIO 번호와 Physical Pin 번호를 구분하여 표기한다.
* Arduino Mega의 D2~D8, D22~D31을 리니어 모터 및 초음파 센서 제어에 사용한다.
* DYNAMIXEL은 U2D2를 통해 통신한다.
* U2D2의 Raspberry Pi 장치 포트는 `/dev/ttyUSB1`을 사용한다.
* 키패드는 Raspberry Pi GPIO 5, 6, 13, 19, 26, 12, 16, 20을 사용한다.
* L298N #3의 ENB, IN3, IN4는 사용하지 않는다.
