# 스마트 시트 핀맵 (Pinout)

스마트 시트 시스템에서 사용되는 Raspberry Pi 4, Arduino Mega 2560, 4×4 Matrix Keypad, I2C LCD, L298N, Linear Motor, U2D2 및 DYNAMIXEL XL430-W250-T의 핀 연결 정보를 정리한 문서입니다.

---

## 1. 전체 시스템 구성

```text
Raspberry Pi 4
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

---

# 2. Raspberry Pi 4 핀맵

## 2.1 I2C LCD

| LCD | Raspberry Pi GPIO | Physical Pin | 기능 |
|---|---:|---:|---|
| VCC | 5V | 2 | 전원 |
| GND | GND | 6 | 접지 |
| SDA | GPIO 2 | 3 | I2C SDA |
| SCL | GPIO 3 | 5 | I2C SCL |

### 결선

```text
Raspberry Pi 4          I2C LCD
────────────────────────────────
Pin 2  (5V)      ─────► VCC
Pin 6  (GND)     ─────► GND
Pin 3  (GPIO 2)  ─────► SDA
Pin 5  (GPIO 3)  ─────► SCL
```

- LCD I2C 주소: `0x27`

---

# 3. Raspberry Pi 4 ↔ 4×4 Matrix Keypad

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
4×4 Matrix Keypad       Raspberry Pi 4
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

---

# 4. Raspberry Pi 4 ↔ Arduino Mega 2560

Raspberry Pi 4와 Arduino Mega 2560은 USB로 연결합니다.

```text
Raspberry Pi 4
      │
      │ USB
      ▼
Arduino Mega 2560
```

| 연결 | 방식 | 기능 |
|---|---|---|
| Raspberry Pi → Arduino Mega | USB | Serial 통신 |
| Raspberry Pi USB → Arduino | USB 5V | Arduino 로직 전원 |

---

# 5. Arduino Mega 2560 ↔ L298N 핀맵

Arduino Mega 2560은 총 5개의 Linear Motor를 제어합니다.

| Motor | L298N | EN | IN1 | IN2 |
|---|---|---:|---:|---:|
| M1 | L298N #1 A | D2 | D22 | D23 |
| M2 | L298N #1 B | D3 | D24 | D25 |
| M3 | L298N #2 A | D4 | D26 | D27 |
| M4 | L298N #2 B | D5 | D28 | D29 |
| M5 | L298N #3 A | D6 | D30 | D31 |

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
L298N #1 OUT3 / OUT4 ───► Linear Motor #2
```

---

# 7. L298N #2

L298N #2는 Linear Motor #3과 #4를 제어합니다.

## Motor #3

```text
Arduino Mega          L298N #2
───────────────────────────────
D4  ─────────────────► ENA
D26 ─────────────────► IN1
D27 ─────────────────► IN2
```

```text
L298N #2 OUT1 / OUT2 ───► Linear Motor #3
```

## Motor #4

```text
Arduino Mega          L298N #2
───────────────────────────────
D5  ─────────────────► ENB
D28 ─────────────────► IN3
D29 ─────────────────► IN4
```

```text
L298N #2 OUT3 / OUT4 ───► Linear Motor #4
```

---

# 8. L298N #3

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

# 9. Linear Motor 배치

5개의 Linear Motor는 모두 등받이에 배치됩니다.

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
              M5 830 mm
                   │
                   │
              M4 660 mm
                   │
                   │
              M3 490 mm
                   │
                   │
              M2 320 mm
                   │
                   │
              M1 150 mm
                   │
                   ▼
```

각 모터는 특정 신체 부위에 고정된 역할을 갖는 것이 아니라, 모터 위치를 기반으로 제어 알고리즘을 통해 등받이 형상을 조절합니다.

---

# 10. Raspberry Pi 4 ↔ U2D2

Raspberry Pi 4와 U2D2는 USB로 연결합니다.

```text
Raspberry Pi 4
      │
      │ USB
      ▼
    U2D2
```

| 연결 | 방식 | 기능 |
|---|---|---|
| Raspberry Pi 4 → U2D2 | USB | DYNAMIXEL 통신 |

---

# 11. U2D2 ↔ U2D2 Power Hub

U2D2와 U2D2 Power Hub는 3핀 케이블로 연결합니다.

```text
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

# 12. U2D2 Power Hub ↔ DYNAMIXEL

DYNAMIXEL XL430-W250-T 2개는 U2D2 Power Hub에 각각 3핀 케이블로 연결합니다.

```text
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
Raspberry Pi 4
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
Raspberry Pi 4
```

| 장치 | 공급 전원 |
|---|---:|
| Raspberry Pi 4 | 5V |

---

## Arduino Mega

```text
Raspberry Pi 4
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

## L298N

```text
12V SMPS
   │
   ├──► L298N #1
   ├──► L298N #2
   └──► L298N #3
```

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

## Raspberry Pi 4

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
                         Raspberry Pi 4
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

# 17. 주의사항

1. Raspberry Pi 4에는 12V를 직접 연결하지 않습니다.
2. Raspberry Pi 4는 5V 전원을 사용합니다.
3. Arduino Mega 2560은 Raspberry Pi USB를 통해 로직 전원을 공급받습니다.
4. 리니어 모터 구동 전원은 12V SMPS를 사용합니다.
5. L298N #1은 M1/M2를 제어합니다.
6. L298N #2는 M3/M4를 제어합니다.
7. L298N #3은 M5를 제어합니다.
8. U2D2는 Raspberry Pi 4와 USB로 연결합니다.
9. U2D2와 U2D2 Power Hub는 3핀 케이블로 연결합니다.
10. U2D2 Power Hub와 XL430-W250-T 2개는 각각 3핀 케이블로 연결합니다.
11. DYNAMIXEL XL430-W250-T의 구동 전원은 U2D2 Power Hub에서 공급합니다.
12. Raspberry Pi 제어 전원과 모터 구동 전원은 분리하여 구성합니다.
13. 전원 인가 전에 전압과 극성을 반드시 확인합니다.
