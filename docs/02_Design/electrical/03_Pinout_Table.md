# 스마트 시트 시스템 핀맵

## 1. 시스템 구성

본 핀맵은 실제 제작 회로와 Cirkit Designer 회로도를 기준으로 작성한다.

| 장치 | 수량 | 역할 |
|---|---:|---|
| Raspberry Pi 3 | 1 | 메인 컨트롤러 |
| Breadboard | 1 | Raspberry Pi 주변 장치 배선 |
| 4×4 Matrix Keypad | 1 | 사용자 입력 |
| I2C LCD 16×2 | 1 | 사용자 정보 및 상태 표시 |
| Arduino Mega 2560 | 1 | 센서 및 리니어 모터 제어 |
| Arduino 확장보드 | 1 | Arduino 핀 연결 및 배선 확장 |
| HC-SR04 | 1 | 거리 측정 |
| L298N Motor Driver | 3 | 리니어 모터 구동 |
| Linear Motor | 5 | 등받이 형상 조절 |
| U2D2 | 1 | Raspberry Pi ↔ DYNAMIXEL 통신 |
| U2D2 Power Hub | 1 | DYNAMIXEL 통신 및 전원 분배 |
| DYNAMIXEL XL430-W250-T | 2 | 벨트/시트 구동 |
| 12V SMPS | 1 | 리니어 모터 계통 전원 |

---

# 2. Raspberry Pi 3 핀맵

## 2-1. I2C LCD 16×2

| LCD 핀 | Raspberry Pi 3 | 물리 핀 | 역할 |
|---|---|---:|---|
| VCC | 5V | Pin 2 | LCD 전원 |
| GND | GND | Pin 6 | Ground |
| SDA | GPIO 2 | Pin 3 | I2C Data |
| SCL | GPIO 3 | Pin 5 | I2C Clock |

### I2C 설정

```text
LCD I2C Address : 0x27
```

---

## 2-2. 4×4 Matrix Keypad

| Keypad 핀 | Raspberry Pi GPIO | 물리 핀 |
|---|---:|---:|
| COL1 | GPIO 5 | Pin 29 |
| COL2 | GPIO 6 | Pin 31 |
| COL3 | GPIO 13 | Pin 33 |
| COL4 | GPIO 19 | Pin 35 |
| ROW1 | GPIO 26 | Pin 37 |
| ROW2 | GPIO 12 | Pin 32 |
| ROW3 | GPIO 16 | Pin 36 |
| ROW4 | GPIO 20 | Pin 38 |

### Keypad GPIO 정리

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

# 3. Raspberry Pi 3 ↔ Arduino Mega 2560

Raspberry Pi 3와 Arduino Mega 2560은 USB로 연결한다.

| Raspberry Pi 3 | Arduino Mega 2560 | 용도 |
|---|---|---|
| USB | USB | Serial 통신 |
| USB | USB | Arduino 로직 전원 공급 |

```text
Raspberry Pi 3
      │
      │ USB
      ▼
Arduino Mega 2560
```

Arduino의 센서 및 모터 제어 핀은 Arduino Mega의 논리 핀 번호를 기준으로 관리한다.

Arduino 확장보드를 사용하는 경우에도 프로그램에서는 동일한 Arduino 핀 번호를 사용한다.

---

# 4. HC-SR04 초음파 센서 핀맵

HC-SR04는 Arduino Mega 2560에 연결한다.

| HC-SR04 | Arduino Mega | 역할 |
|---|---:|---|
| VCC | 5V | 센서 전원 |
| GND | GND | Ground |
| TRIG | D7 | Trigger |
| ECHO | D8 | Echo |

```text
Arduino Mega
│
├── 5V  → HC-SR04 VCC
├── GND → HC-SR04 GND
├── D7  → HC-SR04 TRIG
└── D8  → HC-SR04 ECHO
```

---

# 5. Linear Motor PWM 핀맵

리니어 모터 5개는 L298N 3개를 이용해 제어한다.

| Arduino Mega | L298N | 채널 | Motor | 역할 |
|---:|---|---|---|---|
| D2 | L298N #3 | ENB | Motor 2 | PWM |
| D3 | L298N #1 | ENB | Motor 1 | PWM |
| D4 | L298N #2 | ENA | Motor 3 | PWM |
| D5 | L298N #2 | ENB | Motor 4 | PWM |
| D6 | L298N #3 | ENA | Motor 5 | PWM |

### PWM 핀 요약

```text
D2 → L298N #3 ENB → Motor 2
D3 → L298N #1 ENB → Motor 1
D4 → L298N #2 ENA → Motor 3
D5 → L298N #2 ENB → Motor 4
D6 → L298N #3 ENA → Motor 5
```

---

# 6. Linear Motor 방향 제어 핀맵

## 6-1. L298N #1

L298N #1은 Motor 1만 사용한다.

Motor 1은 B Channel의 OUT3 / OUT4를 사용한다.

| Arduino Mega | L298N #1 | Motor |
|---:|---|---|
| D22 | IN3 | Motor 1 |
| D23 | IN4 | Motor 1 |
| D3 | ENB | Motor 1 PWM |

### 출력

```text
L298N #1

D22 → IN3
D23 → IN4
D3  → ENB

OUT3 / OUT4
      │
      ▼
Linear Motor 1
```

L298N #1의 A Channel(ENA / IN1 / IN2 / OUT1 / OUT2)은 사용하지 않는다.

---

## 6-2. L298N #2

L298N #2는 Motor 3과 Motor 4를 제어한다.

### A Channel — Motor 3

| Arduino Mega | L298N #2 | Motor |
|---:|---|---|
| D24 | IN1 | Motor 3 |
| D25 | IN2 | Motor 3 |
| D4 | ENA | Motor 3 PWM |

```text
D24 → IN1
D25 → IN2
D4  → ENA

OUT1 / OUT2
      │
      ▼
Linear Motor 3
```

### B Channel — Motor 4

| Arduino Mega | L298N #2 | Motor |
|---:|---|---|
| D26 | IN3 | Motor 4 |
| D27 | IN4 | Motor 4 |
| D5 | ENB | Motor 4 PWM |

```text
D26 → IN3
D27 → IN4
D5  → ENB

OUT3 / OUT4
      │
      ▼
Linear Motor 4
```

---

## 6-3. L298N #3

L298N #3은 Motor 5와 Motor 2를 제어한다.

### A Channel — Motor 5

| Arduino Mega | L298N #3 | Motor |
|---:|---|---|
| D28 | IN1 | Motor 5 |
| D29 | IN2 | Motor 5 |
| D6 | ENA | Motor 5 PWM |

```text
D28 → IN1
D29 → IN2
D6  → ENA

OUT1 / OUT2
      │
      ▼
Linear Motor 5
```

### B Channel — Motor 2

| Arduino Mega | L298N #3 | Motor |
|---:|---|---|
| D30 | IN3 | Motor 2 |
| D31 | IN4 | Motor 2 |
| D2 | ENB | Motor 2 PWM |

```text
D30 → IN3
D31 → IN4
D2  → ENB

OUT3 / OUT4
      │
      ▼
Linear Motor 2
```

---

# 7. Arduino Mega 전체 Digital Pin 사용 현황

| Arduino Pin | 연결 대상 | 역할 |
|---:|---|---|
| D2 | L298N #3 ENB | Motor 2 PWM |
| D3 | L298N #1 ENB | Motor 1 PWM |
| D4 | L298N #2 ENA | Motor 3 PWM |
| D5 | L298N #2 ENB | Motor 4 PWM |
| D6 | L298N #3 ENA | Motor 5 PWM |
| D7 | HC-SR04 TRIG | 초음파 Trigger |
| D8 | HC-SR04 ECHO | 초음파 Echo |
| D22 | L298N #1 IN3 | Motor 1 방향 |
| D23 | L298N #1 IN4 | Motor 1 방향 |
| D24 | L298N #2 IN1 | Motor 3 방향 |
| D25 | L298N #2 IN2 | Motor 3 방향 |
| D26 | L298N #2 IN3 | Motor 4 방향 |
| D27 | L298N #2 IN4 | Motor 4 방향 |
| D28 | L298N #3 IN1 | Motor 5 방향 |
| D29 | L298N #3 IN2 | Motor 5 방향 |
| D30 | L298N #3 IN3 | Motor 2 방향 |
| D31 | L298N #3 IN4 | Motor 2 방향 |

---

# 8. 모터별 최종 핀맵

| Motor | Driver | Channel | PWM | 방향 제어 | 출력 |
|---|---|---|---:|---|---|
| Motor 1 | L298N #1 | B | D3 | D22 / D23 | OUT3 / OUT4 |
| Motor 2 | L298N #3 | B | D2 | D30 / D31 | OUT3 / OUT4 |
| Motor 3 | L298N #2 | A | D4 | D24 / D25 | OUT1 / OUT2 |
| Motor 4 | L298N #2 | B | D5 | D26 / D27 | OUT3 / OUT4 |
| Motor 5 | L298N #3 | A | D6 | D28 / D29 | OUT1 / OUT2 |

---

# 9. L298N별 최종 핀맵

## L298N #1

```text
Motor 1

Arduino D3  → ENB
Arduino D22 → IN3
Arduino D23 → IN4

OUT3 / OUT4 → Motor 1
```

---

## L298N #2

```text
Motor 3

Arduino D4  → ENA
Arduino D24 → IN1
Arduino D25 → IN2

OUT1 / OUT2 → Motor 3


Motor 4

Arduino D5  → ENB
Arduino D26 → IN3
Arduino D27 → IN4

OUT3 / OUT4 → Motor 4
```

---

## L298N #3

```text
Motor 5

Arduino D6  → ENA
Arduino D28 → IN1
Arduino D29 → IN2

OUT1 / OUT2 → Motor 5


Motor 2

Arduino D2  → ENB
Arduino D30 → IN3
Arduino D31 → IN4

OUT3 / OUT4 → Motor 2
```

---

# 10. U2D2 / DYNAMIXEL 연결

Raspberry Pi 3와 DYNAMIXEL은 U2D2를 통해 통신한다.

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
      ├── 3핀 → DYNAMIXEL XL430-W250-T #1
      │
      └── 3핀 → DYNAMIXEL XL430-W250-T #2
```

| 시작 장치 | 연결 대상 | 연결 방식 |
|---|---|---|
| Raspberry Pi 3 | U2D2 | USB |
| U2D2 | U2D2 Power Hub | 3핀 |
| U2D2 Power Hub | DYNAMIXEL #1 | 3핀 |
| U2D2 Power Hub | DYNAMIXEL #2 | 3핀 |

U2D2 Power Hub에는 DYNAMIXEL 구동을 위한 별도 외부 전원을 사용한다.

> 외부 전원의 세부 전압 및 전원 공급 경로는 `전원 계통도.md`에서 관리한다.

---

# 11. Raspberry Pi 전체 GPIO 사용 현황

| BCM GPIO | 물리 핀 | 연결 대상 | 역할 |
|---:|---:|---|---|
| GPIO 2 | 3 | I2C LCD SDA | I2C Data |
| GPIO 3 | 5 | I2C LCD SCL | I2C Clock |
| GPIO 5 | 29 | Keypad COL1 | Keypad |
| GPIO 6 | 31 | Keypad COL2 | Keypad |
| GPIO 13 | 33 | Keypad COL3 | Keypad |
| GPIO 19 | 35 | Keypad COL4 | Keypad |
| GPIO 26 | 37 | Keypad ROW1 | Keypad |
| GPIO 12 | 32 | Keypad ROW2 | Keypad |
| GPIO 16 | 36 | Keypad ROW3 | Keypad |
| GPIO 20 | 38 | Keypad ROW4 | Keypad |

---

# 12. 핀맵 요약

```text
Raspberry Pi 3
│
├── GPIO 2  → LCD SDA
├── GPIO 3  → LCD SCL
│
├── GPIO 5  → Keypad COL1
├── GPIO 6  → Keypad COL2
├── GPIO 13 → Keypad COL3
├── GPIO 19 → Keypad COL4
├── GPIO 26 → Keypad ROW1
├── GPIO 12 → Keypad ROW2
├── GPIO 16 → Keypad ROW3
├── GPIO 20 → Keypad ROW4
│
├── USB → Arduino Mega 2560
│
└── USB → U2D2


Arduino Mega 2560
│
├── D2 → Motor 2 PWM
├── D3 → Motor 1 PWM
├── D4 → Motor 3 PWM
├── D5 → Motor 4 PWM
├── D6 → Motor 5 PWM
│
├── D7 → HC-SR04 TRIG
├── D8 → HC-SR04 ECHO
│
├── D22 / D23 → Motor 1 방향
├── D24 / D25 → Motor 3 방향
├── D26 / D27 → Motor 4 방향
├── D28 / D29 → Motor 5 방향
└── D30 / D31 → Motor 2 방향
```

---

# 13. 문서 관리 기준

본 문서에서는 실제 GPIO 및 제어 핀 번호만 관리한다.

```text
electric/
├── 핀맵.md
├── 결선도.md
└── 전원 계통도.md
```

- `핀맵.md`
  - Raspberry Pi GPIO
  - Arduino Digital Pin
  - HC-SR04 TRIG / ECHO
  - L298N ENA / ENB
  - L298N IN1 ~ IN4
  - 모터별 제어 핀

- `결선도.md`
  - Breadboard 및 확장보드 포함 실제 장치 연결 구조
  - Raspberry Pi ↔ 주변 장치
  - Arduino ↔ L298N ↔ Linear Motor
  - U2D2 ↔ Power Hub ↔ DYNAMIXEL

- `전원 계통도.md`
  - Raspberry Pi 전원
  - Arduino 전원
  - 12V SMPS
  - L298N 및 Linear Motor 전원
  - U2D2 Power Hub 외부 전원
  - DYNAMIXEL 구동 전원
