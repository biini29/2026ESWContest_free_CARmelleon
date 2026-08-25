# 시스템 제어 및 회로 구성 핀맵

## 1. 시스템 구성

| 장치                     | 수량 | 역할           |
| ---------------------- | -: | ------------ |
| Raspberry Pi 4         |  1 | 메인 컨트롤러      |
| 4×4 Matrix Keypad      |  1 | 사용자 입력       |
| I2C 16×2 Character LCD |  1 | 상태 및 안내 출력   |
| Arduino Mega 2560      |  1 | 모터 제어        |
| L298N                  |  3 | 리니어 액추에이터 구동 |
| 12V DC Linear Actuator |  5 | 실제 구동부       |
| 12V Power Supply       |  1 | 모터 전원        |

---

## 2. Raspberry Pi 4 핀맵

### 2-1. I2C LCD

| LCD 핀 | Raspberry Pi 물리 핀 |    BCM | 역할      |
| ----- | ----------------: | -----: | ------- |
| VCC   |                2번 |     5V | 전원      |
| GND   |                6번 |    GND | 접지      |
| SDA   |                3번 | GPIO 2 | I2C 데이터 |
| SCL   |                5번 | GPIO 3 | I2C 클럭  |

* I2C 주소: `0x27`
* LCD: `16×2 Character LCD`
* I2C 백팩: `PCF8574`
* Python 라이브러리: `RPLCD.i2c.CharLCD('PCF8574', 0x27, cols=16, rows=2)`

### 2-2. 4×4 Matrix Keypad

키패드의 핀은 왼쪽부터 1~8번 순서로 연결한다.

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

```python
ROW_PINS = [5, 6, 13, 19]      # BCM
COL_PINS = [26, 12, 16, 20]    # BCM
```

### 키패드 레이아웃

```text
[ 1 ][ 2 ][ 3 ][ A ]
[ 4 ][ 5 ][ 6 ][ B ]
[ 7 ][ 8 ][ 9 ][ C ]
[ . ][ 0 ][ E ][ D ]
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

Raspberry Pi 4와 Arduino Mega 2560은 USB Serial 통신으로 연결한다.

```text
Raspberry Pi 4
      │
      │ USB Serial
      ▼
Arduino Mega 2560
      │
      ├── L298N #1
      ├── L298N #2
      └── L298N #3
```

---

## 4. Arduino Mega 2560 ↔ L298N 핀맵

### L298N #1

| L298N 핀 | Arduino Mega | 기능         |
| ------- | -----------: | ---------- |
| ENA     |           D2 | PWM 속도 제어  |
| IN1     |          D22 | 모터 1 방향 제어 |
| IN2     |          D23 | 모터 1 방향 제어 |
| ENB     |           D3 | PWM 속도 제어  |
| IN3     |          D24 | 모터 2 방향 제어 |
| IN4     |          D25 | 모터 2 방향 제어 |

**모터 연결**

```text
OUT1, OUT2 → Linear Actuator 1
OUT3, OUT4 → Linear Actuator 2
```

### L298N #2

| L298N 핀 | Arduino Mega | 기능         |
| ------- | -----------: | ---------- |
| ENA     |           D4 | PWM 속도 제어  |
| IN1     |          D26 | 모터 3 방향 제어 |
| IN2     |          D27 | 모터 3 방향 제어 |
| ENB     |           D5 | PWM 속도 제어  |
| IN3     |          D28 | 모터 4 방향 제어 |
| IN4     |          D29 | 모터 4 방향 제어 |

**모터 연결**

```text
OUT1, OUT2 → Linear Actuator 3
OUT3, OUT4 → Linear Actuator 4
```

### L298N #3

| L298N 핀 | Arduino Mega | 기능         |
| ------- | -----------: | ---------- |
| ENA     |           D6 | PWM 속도 제어  |
| IN1     |          D30 | 모터 5 방향 제어 |
| IN2     |          D31 | 모터 5 방향 제어 |
| ENB     |      사용하지 않음 | 미사용        |
| IN3     |      사용하지 않음 | 미사용        |
| IN4     |      사용하지 않음 | 미사용        |

**모터 연결**

```text
OUT1, OUT2 → Linear Actuator 5
OUT3, OUT4 → 사용하지 않음
```

---

## 5. 전체 모터 핀맵

| 액추에이터   | L298N | OUT         | EN(PWM) | IN1 | IN2 |
| ------- | ----- | ----------- | ------: | --: | --: |
| Motor 1 | #1    | OUT1 / OUT2 |      D2 | D22 | D23 |
| Motor 2 | #1    | OUT3 / OUT4 |      D3 | D24 | D25 |
| Motor 3 | #2    | OUT1 / OUT2 |      D4 | D26 | D27 |
| Motor 4 | #2    | OUT3 / OUT4 |      D5 | D28 | D29 |
| Motor 5 | #3    | OUT1 / OUT2 |      D6 | D30 | D31 |

---

## 6. 리니어 액추에이터 연결

각 리니어 액추에이터는 2가닥 출력을 사용하며 L298N의 한 채널에 연결한다.

| 액추에이터             | L298N    | 출력          |
| ----------------- | -------- | ----------- |
| Linear Actuator 1 | L298N #1 | OUT1 / OUT2 |
| Linear Actuator 2 | L298N #1 | OUT3 / OUT4 |
| Linear Actuator 3 | L298N #2 | OUT1 / OUT2 |
| Linear Actuator 4 | L298N #2 | OUT3 / OUT4 |
| Linear Actuator 5 | L298N #3 | OUT1 / OUT2 |

---

## 7. 12V 전원 연결

12V 전원공급장치의 출력은 L298N 3개에 병렬로 연결한다.

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
```

### Common Ground

Arduino Mega와 L298N 3개는 반드시 공통 GND를 사용한다.

```text
                ┌── L298N #1 GND
                │
12V Power (-) ──┼── L298N #2 GND
                │
                ├── L298N #3 GND
                │
                └── Arduino Mega GND
```

---

## 8. 전체 시스템 연결 구조

```text
                         ┌─────────────────────┐
                         │    Raspberry Pi 4   │
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
```

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
```

## 10. 주의사항

* L298N의 `ENA/ENB`를 Arduino Mega에서 PWM으로 제어할 경우 해당 채널의 Enable 점퍼를 제거한다.
* 12V 전원은 리니어 액추에이터 구동용으로 사용한다.
* Raspberry Pi의 GPIO에 12V를 직접 연결하지 않는다.
* Arduino Mega와 L298N은 반드시 공통 GND로 연결한다.
* 리니어 액추에이터의 방향은 `IN1/IN2` 또는 `IN3/IN4`의 HIGH/LOW 조합으로 제어한다.
* Raspberry Pi와 Arduino Mega 간 제어 명령은 USB Serial을 통해 전달한다.
