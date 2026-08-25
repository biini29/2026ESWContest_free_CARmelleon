# 시스템 제어 및 회로 구성 핀맵
# 스마트 시트 핀맵 (Pinout)

## 1. 시스템 구성

| 장치                     | 수량 | 역할           |
| ---------------------- | -: | ------------ |
| Raspberry Pi 3         |  1 | 메인 컨트롤러      |
| 4×4 Matrix Keypad      |  1 | 사용자 입력       |
| I2C 16×2 Character LCD |  1 | 상태 및 안내 출력   |
| Arduino Mega 2560      |  1 | 모터 제어        |
| L298N                  |  3 | 리니어 액추에이터 구동 |
| 12V DC Linear Actuator |  5 | 실제 구동부       |
| 12V Power Supply       |  1 | 모터 전원        |
스마트 시트 시스템에서 사용되는 Raspberry Pi 4, Arduino Mega 2560, 4×4 Matrix Keypad, I2C LCD, L298N, Linear Motor, U2D2 및 DYNAMIXEL XL430-W250-T의 핀 연결 정보를 정리한 문서입니다.

---

## 2. Raspberry Pi 3 핀맵
## 1. 전체 시스템 구성

### 2-1. I2C LCD
```text
Raspberry Pi 3
│
├── 4×4 Matrix Keypad
│
├── I2C LCD
│
├── USB ─────► Arduino Mega 2560
│                │
│                ├── L298N #1 ──► Linear Motor #1, #2
│                ├── L298N #2 ──► Linear Motor #3, #4
│                └── L298N #3 ──► Linear Motor #5
│
└── USB ─────► U2D2
                  │
                  │ 3핀 케이블
                  ▼
             U2D2 Power Hub
                  │
             ┌────┴────┐
            3핀       3핀
             │          │
             ▼          ▼
          XL430 #1   XL430 #2
```

| LCD 핀 | Raspberry Pi 물리 핀 |    BCM | 역할      |
| ----- | ----------------: | -----: | ------- |
| VCC   |                2번 |     5V | 전원      |
| GND   |                6번 |    GND | 접지      |
| SDA   |                3번 | GPIO 2 | I2C 데이터 |
| SCL   |                5번 | GPIO 3 | I2C 클럭  |
---

* I2C 주소: `0x27`
* LCD: `16×2 Character LCD`
* I2C 백팩: `PCF8574`
* Python 라이브러리: `RPLCD.i2c.CharLCD('PCF8574', 0x27, cols=16, rows=2)`
# 2. Raspberry Pi 3 핀맵

### 2-2. 4×4 Matrix Keypad
## 2.1 I2C LCD

키패드의 핀은 왼쪽부터 1~8번 순서로 연결한다.
| LCD | Raspberry Pi GPIO | Physical Pin | 기능 |
|---|---:|---:|---|
| VCC | 5V | 2 | 전원 |
| GND | GND | 6 | 접지 |
| SDA | GPIO 2 | 3 | I2C SDA |
| SCL | GPIO 3 | 5 | I2C SCL |

| 키패드 핀 | 역할    | Raspberry Pi 물리 핀 |     BCM |
| ----- | ----- | ----------------: | ------: |
| 1번    | Row 1 |               29번 |  GPIO 5 |
| 2번    | Row 2 |               31번 |  GPIO 6 |
| 3번    | Row 3 |               33번 | GPIO 13 |
| 4번    | Row 4 |               35번 | GPIO 19 |
| 5번    | Col 1 |               37번 | GPIO 26 |
| 6번    | Col 2 |               32번 | GPIO 12 |
| 7번    | Col 3 |               36번 | GPIO 16 |
| 8번    | Col 4 |               38번 | GPIO 20 |
### 결선

```python
ROW_PINS = [5, 6, 13, 19]      # BCM
COL_PINS = [26, 12, 16, 20]    # BCM
```text
Raspberry Pi 3          I2C LCD
────────────────────────────────
Pin 2  (5V)      ─────► VCC
Pin 6  (GND)     ─────► GND
Pin 3  (GPIO 2)  ─────► SDA
Pin 5  (GPIO 3)  ─────► SCL
```

### 키패드 레이아웃
- LCD I2C 주소: `0x27`

---

# 3. Raspberry Pi 3 ↔ 4×4 Matrix Keypad

4×4 Matrix Keypad는 총 8개의 GPIO를 사용합니다.

| Keypad | Raspberry Pi BCM GPIO | Physical Pin | 기능 |
|---|---:|---:|---|
| R1 | GPIO 5 | 29 | Row 1 |
| R2 | GPIO 6 | 31 | Row 2 |
| R3 | GPIO 13 | 33 | Row 3 |
| R4 | GPIO 19 | 35 | Row 4 |
| C1 | GPIO 26 | 37 | Column 1 |
| C2 | GPIO 12 | 32 | Column 2 |
| C3 | GPIO 16 | 36 | Column 3 |
| C4 | GPIO 20 | 38 | Column 4 |

### 결선

```text
[ 1 ][ 2 ][ 3 ][ A ]
[ 4 ][ 5 ][ 6 ][ B ]
[ 7 ][ 8 ][ 9 ][ C ]
[ . ][ 0 ][ E ][ D ]
4×4 Matrix Keypad       Raspberry Pi 3
───────────────────────────────────────
R1 ───────────────────► GPIO 5
R2 ───────────────────► GPIO 6
R3 ───────────────────► GPIO 13
R4 ───────────────────► GPIO 19

C1 ───────────────────► GPIO 26
C2 ───────────────────► GPIO 12
C3 ───────────────────► GPIO 16
C4 ───────────────────► GPIO 20
```

| 키 | 기능            |
| - | ------------- |
| A | 아빠 (178)      |
| B | 엄마 (162, 임산부) |
| C | 딸 (130)       |
| D | 게스트 모드        |
| E | Enter         |
| . | 평상시 리셋        |

---

## 3. Raspberry Pi ↔ Arduino Mega 통신
# 4. Raspberry Pi 3 ↔ Arduino Mega 2560

Raspberry Pi 3와 Arduino Mega 2560은 USB Serial 통신으로 연결한다.
Raspberry Pi 3와 Arduino Mega 2560은 USB로 연결합니다.

```text
Raspberry Pi 3
      │
      │ USB Serial
      │ USB
      ▼
Arduino Mega 2560
      │
      ├── L298N #1
      ├── L298N #2
      └── L298N #3
```

| 연결 | 방식 | 기능 |
|---|---|---|
| Raspberry Pi → Arduino Mega | USB | Serial 통신 |
| Raspberry Pi USB → Arduino | USB 5V | Arduino 로직 전원 |

---

## 4. Arduino Mega 2560 ↔ L298N 핀맵
# 5. Arduino Mega 2560 ↔ L298N 핀맵

### L298N #1
Arduino Mega 2560은 총 5개의 Linear Motor를 제어합니다.

| L298N 핀 | Arduino Mega | 기능         |
| ------- | -----------: | ---------- |
| ENA     |           D2 | PWM 속도 제어  |
| IN1     |          D22 | 모터 1 방향 제어 |
| IN2     |          D23 | 모터 1 방향 제어 |
| ENB     |           D3 | PWM 속도 제어  |
| IN3     |          D24 | 모터 2 방향 제어 |
| IN4     |          D25 | 모터 2 방향 제어 |
| Motor | L298N | EN | IN1 | IN2 |
|---|---|---:|---:|---:|
| M1 | L298N #1 A | D2 | D22 | D23 |
| M2 | L298N #1 B | D3 | D24 | D25 |
| M3 | L298N #2 A | D4 | D26 | D27 |
| M4 | L298N #2 B | D5 | D28 | D29 |
| M5 | L298N #3 A | D6 | D30 | D31 |

**모터 연결**
---

# 6. L298N #1

L298N #1은 Linear Motor #1과 #2를 제어합니다.

## Motor #1

```text
Arduino Mega          L298N #1
───────────────────────────────
D2  ─────────────────► ENA
D22 ─────────────────► IN1
D23 ─────────────────► IN2
```

```text
L298N #1 OUT1 / OUT2 ───► Linear Motor #1
```

## Motor #2

```text
Arduino Mega          L298N #1
───────────────────────────────
D3  ─────────────────► ENB
D24 ─────────────────► IN3
D25 ─────────────────► IN4
```

```text
OUT1, OUT2 → Linear Actuator 1
OUT3, OUT4 → Linear Actuator 2
L298N #1 OUT3 / OUT4 ───► Linear Motor #2
```

### L298N #2
---

# 7. L298N #2

| L298N 핀 | Arduino Mega | 기능         |
| ------- | -----------: | ---------- |
| ENA     |           D4 | PWM 속도 제어  |
| IN1     |          D26 | 모터 3 방향 제어 |
| IN2     |          D27 | 모터 3 방향 제어 |
| ENB     |           D5 | PWM 속도 제어  |
| IN3     |          D28 | 모터 4 방향 제어 |
| IN4     |          D29 | 모터 4 방향 제어 |
L298N #2는 Linear Motor #3과 #4를 제어합니다.

**모터 연결**
## Motor #3

```text
OUT1, OUT2 → Linear Actuator 3
OUT3, OUT4 → Linear Actuator 4
Arduino Mega          L298N #2
───────────────────────────────
D4  ─────────────────► ENA
D26 ─────────────────► IN1
D27 ─────────────────► IN2
```

### L298N #3
```text
L298N #2 OUT1 / OUT2 ───► Linear Motor #3
```

| L298N 핀 | Arduino Mega | 기능         |
| ------- | -----------: | ---------- |
| ENA     |           D6 | PWM 속도 제어  |
| IN1     |          D30 | 모터 5 방향 제어 |
| IN2     |          D31 | 모터 5 방향 제어 |
| ENB     |      사용하지 않음 | 미사용        |
| IN3     |      사용하지 않음 | 미사용        |
| IN4     |      사용하지 않음 | 미사용        |
## Motor #4

**모터 연결**
```text
Arduino Mega          L298N #2
───────────────────────────────
D5  ─────────────────► ENB
D28 ─────────────────► IN3
D29 ─────────────────► IN4
```

```text
OUT1, OUT2 → Linear Actuator 5
OUT3, OUT4 → 사용하지 않음
L298N #2 OUT3 / OUT4 ───► Linear Motor #4
```

---

## 5. 전체 모터 핀맵
# 8. L298N #3

| 액추에이터   | L298N | OUT         | EN(PWM) | IN1 | IN2 |
| ------- | ----- | ----------- | ------: | --: | --: |
| Motor 1 | #1    | OUT1 / OUT2 |      D2 | D22 | D23 |
| Motor 2 | #1    | OUT3 / OUT4 |      D3 | D24 | D25 |
| Motor 3 | #2    | OUT1 / OUT2 |      D4 | D26 | D27 |
| Motor 4 | #2    | OUT3 / OUT4 |      D5 | D28 | D29 |
| Motor 5 | #3    | OUT1 / OUT2 |      D6 | D30 | D31 |
L298N #3은 Linear Motor #5를 제어합니다.

## Motor #5

```text
Arduino Mega          L298N #3
───────────────────────────────
D6  ─────────────────► ENA
D30 ─────────────────► IN1
D31 ─────────────────► IN2
```

```text
L298N #3 OUT1 / OUT2 ───► Linear Motor #5
```

L298N #3의 B채널(ENB, IN3, IN4)은 사용하지 않습니다.

---

## 6. 리니어 액추에이터 연결
# 9. Linear Motor 배치

각 리니어 액추에이터는 2가닥 출력을 사용하며 L298N의 한 채널에 연결한다.
5개의 Linear Motor는 모두 등받이에 배치됩니다.

| 액추에이터             | L298N    | 출력          |
| ----------------- | -------- | ----------- |
| Linear Actuator 1 | L298N #1 | OUT1 / OUT2 |
| Linear Actuator 2 | L298N #1 | OUT3 / OUT4 |
| Linear Actuator 3 | L298N #2 | OUT1 / OUT2 |
| Linear Actuator 4 | L298N #2 | OUT3 / OUT4 |
| Linear Actuator 5 | L298N #3 | OUT1 / OUT2 |
| Motor | 위치 |
|---|---:|
| M1 | 150 mm |
| M2 | 320 mm |
| M3 | 490 mm |
| M4 | 660 mm |
| M5 | 830 mm |

```text
                 등받이
                   │
                   │
              M5 500 mm
                   │
                   │
              M4 415 mm
                   │
                   │
              M3 330 mm
                   │
                   │
              M2 245 mm
                   │
                   │
              M1 160 mm
                   │
                   ▼
```

각 모터는 특정 신체 부위에 고정된 역할을 갖는 것이 아니라, 모터 위치를 기반으로 제어 알고리즘을 통해 등받이 형상을 조절합니다.

---

## 7. 12V 전원 연결
# 10. Raspberry Pi 3 ↔ U2D2

12V 전원공급장치의 출력은 L298N 3개에 병렬로 연결한다.
Raspberry Pi 3와 U2D2는 USB로 연결합니다.

```text
12V Power Supply (+)
        │
        ├── L298N #1 +12V
        ├── L298N #2 +12V
        └── L298N #3 +12V

12V Power Supply (-)
        │
        ├── L298N #1 GND
        ├── L298N #2 GND
        ├── L298N #3 GND
        └── Arduino Mega GND
Raspberry Pi 3
      │
      │ USB
      ▼
    U2D2
```

### Common Ground
| 연결 | 방식 | 기능 |
|---|---|---|
| Raspberry Pi 3 → U2D2 | USB | DYNAMIXEL 통신 |

---

# 11. U2D2 ↔ U2D2 Power Hub

Arduino Mega와 L298N 3개는 반드시 공통 GND를 사용한다.
U2D2와 U2D2 Power Hub는 3핀 케이블로 연결합니다.

```text
                ┌── L298N #1 GND
                │
12V Power (-) ──┼── L298N #2 GND
                │
                ├── L298N #3 GND
                │
                └── Arduino Mega GND
U2D2
 │
 │ 3핀 케이블
 ▼
U2D2 Power Hub
```

### 연결 신호

| 신호 | 기능 |
|---|---|
| DATA | DYNAMIXEL 통신 |
| VDD | 전원 버스 |
| GND | 공통 접지 |

> 실제 커넥터의 물리적인 핀 번호 및 케이블 색상은 사용 중인 케이블과 보드의 표기를 기준으로 확인합니다.

---

## 8. 전체 시스템 연결 구조
# 12. U2D2 Power Hub ↔ DYNAMIXEL

DYNAMIXEL XL430-W250-T 2개는 U2D2 Power Hub에 각각 3핀 케이블로 연결합니다.

```text
                         ┌─────────────────────┐
                         │    Raspberry Pi 3   │
                         │                     │
                         │ GPIO 2 ── SDA ─────┼── I2C LCD
                         │ GPIO 3 ── SCL ─────┼── I2C LCD
                         │                     │
                         │ GPIO 5  ───────────┼── Keypad Row 1
                         │ GPIO 6  ───────────┼── Keypad Row 2
                         │ GPIO 13 ───────────┼── Keypad Row 3
                         │ GPIO 19 ───────────┼── Keypad Row 4
                         │ GPIO 26 ───────────┼── Keypad Col 1
                         │ GPIO 12 ───────────┼── Keypad Col 2
                         │ GPIO 16 ───────────┼── Keypad Col 3
                         │ GPIO 20 ───────────┼── Keypad Col 4
                         └──────────┬──────────┘
                                    │
                              USB Serial
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Arduino Mega 2560  │
                         │                     │
                         │ D2  ~ D6  : PWM    │
                         │ D22 ~ D31 : 방향제어 │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
             ┌─────────┐      ┌─────────┐      ┌─────────┐
             │ L298N #1│      │ L298N #2│      │ L298N #3│
             └────┬────┘      └────┬────┘      └────┬────┘
                  │                 │                 │
             ┌────┴────┐       ┌────┴────┐           │
             ▼         ▼       ▼         ▼           ▼
          Motor 1   Motor 2  Motor 3   Motor 4     Motor 5


                   ┌──────────────────────┐
                   │  12V Power Supply   │
                   └──────────┬───────────┘
                              │
                         병렬 연결
                              │
                   ┌──────────┴──────────┐
                   ▼                     ▼
              L298N #1~#3           Common GND
                                          │
                                   Arduino Mega
                    U2D2 Power Hub
                         │
             ┌───────────┴───────────┐
             │                       │
            3핀                     3핀
             │                       │
             ▼                       ▼
      XL430-W250-T #1        XL430-W250-T #2
```

| 장치 | 연결 |
|---|---|
| XL430-W250-T #1 | U2D2 Power Hub → 3핀 |
| XL430-W250-T #2 | U2D2 Power Hub → 3핀 |

---

# 13. DYNAMIXEL 전체 연결

```text
Raspberry Pi 3
      │
      │ USB
      ▼
    U2D2
      │
      │ 3핀
      ▼
U2D2 Power Hub
      │
      ├──── 3핀 ────► XL430-W250-T #1
      │
      └──── 3핀 ────► XL430-W250-T #2
```

---

# 14. 전원 연결

## Raspberry Pi

```text
12V / 5V 어댑터
       │
      5V
       ▼
Raspberry Pi 3
```

| 장치 | 공급 전원 |
|---|---:|
| Raspberry Pi 3 | 5V |

---

## Arduino Mega

```text
Raspberry Pi 3
      │
      │ USB
      ▼
Arduino Mega 2560
```

| 장치 | 공급 전원 |
|---|---:|
| Arduino Mega 2560 | USB 5V |

Arduino Mega의 USB 연결은 로직 전원 및 Serial 통신에 사용합니다.

---

## 9. Arduino Mega 코드용 핀 상수

```cpp
// ================================
// L298N #1
// ================================
#define M1_EN  2
#define M1_IN1 22
#define M1_IN2 23

#define M2_EN  3
#define M2_IN1 24
#define M2_IN2 25

// ================================
// L298N #2
// ================================
#define M3_EN  4
#define M3_IN1 26
#define M3_IN2 27

#define M4_EN  5
#define M4_IN1 28
#define M4_IN2 29

// ================================
// L298N #3
// ================================
#define M5_EN  6
#define M5_IN1 30
#define M5_IN2 31
## L298N

```text
12V SMPS
   │
   ├──► L298N #1
   ├──► L298N #2
   └──► L298N #3
```

## 10. 주의사항
| 장치 | 공급 전원 |
|---|---:|
| L298N #1 | 12V |
| L298N #2 | 12V |
| L298N #3 | 12V |

---

## U2D2 Power Hub

```text
12V SMPS
    │
   12V
    ▼
U2D2 Power Hub
```

| 장치 | 공급 전원 |
|---|---:|
| U2D2 Power Hub | 12V |

Power Hub를 통해 XL430-W250-T 2개에 전원 및 통신을 공급합니다.

---

# 15. 전체 핀맵 요약

## Raspberry Pi 3

| 장치 | GPIO | Physical Pin | 기능 |
|---|---:|---:|---|
| LCD SDA | GPIO 2 | 3 | I2C SDA |
| LCD SCL | GPIO 3 | 5 | I2C SCL |
| LCD VCC | 5V | 2 | 전원 |
| LCD GND | GND | 6 | 접지 |
| Keypad R1 | GPIO 5 | 29 | Row 1 |
| Keypad R2 | GPIO 6 | 31 | Row 2 |
| Keypad R3 | GPIO 13 | 33 | Row 3 |
| Keypad R4 | GPIO 19 | 35 | Row 4 |
| Keypad C1 | GPIO 26 | 37 | Column 1 |
| Keypad C2 | GPIO 12 | 32 | Column 2 |
| Keypad C3 | GPIO 16 | 36 | Column 3 |
| Keypad C4 | GPIO 20 | 38 | Column 4 |

## Arduino Mega 2560

| Motor | Driver | EN | IN1 | IN2 |
|---|---|---:|---:|---:|
| M1 | L298N #1 A | D2 | D22 | D23 |
| M2 | L298N #1 B | D3 | D24 | D25 |
| M3 | L298N #2 A | D4 | D26 | D27 |
| M4 | L298N #2 B | D5 | D28 | D29 |
| M5 | L298N #3 A | D6 | D30 | D31 |

## DYNAMIXEL

| 연결 | 방식 | 용도 |
|---|---|---|
| Raspberry Pi → U2D2 | USB | 통신 |
| U2D2 → Power Hub | 3핀 | DATA / VDD / GND |
| Power Hub → XL430 #1 | 3핀 | 전원 + 통신 |
| Power Hub → XL430 #2 | 3핀 | 전원 + 통신 |

---

# 16. 최종 핀맵 구조

```text
                         Raspberry Pi 3
                              │
             ┌────────────────┼─────────────────┐
             │                │                 │
          GPIO/I2C           USB               USB
             │                │                 │
       ┌─────┴─────┐          │                 │
       │           │          ▼                 ▼
  4×4 Keypad    I2C LCD   Arduino Mega         U2D2
                             │                  │
                             │                  │ 3핀
                             │                  ▼
                             │           U2D2 Power Hub
                             │              │      │
                             │             3핀    3핀
                             │              │      │
                             │              ▼      ▼
                             │           XL430   XL430
                             │             #1      #2
                             │
                    ┌────────┼────────┐
                    │        │        │
                    ▼        ▼        ▼
                 L298N #1 L298N #2 L298N #3
                    │        │        │
                   M1/M2    M3/M4      M5
```

---

* L298N의 `ENA/ENB`를 Arduino Mega에서 PWM으로 제어할 경우 해당 채널의 Enable 점퍼를 제거한다.
* 12V 전원은 리니어 액추에이터 구동용으로 사용한다.
* Raspberry Pi의 GPIO에 12V를 직접 연결하지 않는다.
* Arduino Mega와 L298N은 반드시 공통 GND로 연결한다.
* 리니어 액추에이터의 방향은 `IN1/IN2` 또는 `IN3/IN4`의 HIGH/LOW 조합으로 제어한다.
* Raspberry Pi와 Arduino Mega 간 제어 명령은 USB Serial을 통해 전달한다.
# 17. 주의사항

1. Raspberry Pi 3에는 12V를 직접 연결하지 않습니다.
2. Raspberry Pi 3는 5V 전원을 사용합니다.
3. Arduino Mega 2560은 Raspberry Pi USB를 통해 로직 전원을 공급받습니다.
4. 리니어 모터 구동 전원은 12V SMPS를 사용합니다.
5. L298N #1은 M1/M2를 제어합니다.
6. L298N #2는 M3/M4를 제어합니다.
7. L298N #3은 M5를 제어합니다.
8. U2D2는 Raspberry Pi 3와 USB로 연결합니다.
9. U2D2와 U2D2 Power Hub는 3핀 케이블로 연결합니다.
10. U2D2 Power Hub와 XL430-W250-T 2개는 각각 3핀 케이블로 연결합니다.
11. DYNAMIXEL XL430-W250-T의 구동 전원은 U2D2 Power Hub에서 공급합니다.
12. Raspberry Pi 제어 전원과 모터 구동 전원은 분리하여 구성합니다.
13. 전원 인가 전에 전압과 극성을 반드시 확인합니다.
U2D2는 Raspberry Pi 3와 USB로 연결합니다.
U2D2와 U2D2 Power Hub는 3핀 케이블로 연결합니다.
XL430-W250-T #1, #2는 Power Hub에 각각 3핀 케이블로 연결합니다.
DYNAMIXEL 전원은 U2D2 Power Hub를 통해 공급합니다.
Raspberry Pi 제어 전원과 모터 구동 전원은 분리하여 구성합니다.
전원 인가 전에 각 장치의 전압과 극성을 반드시 확인합니다.
