# 스마트 시트 전체 결선도 (Wiring Diagram)

스마트 시트 시스템의 전체 하드웨어 결선 구조를 정리한 문서입니다.

본 시스템은 **Raspberry Pi 4를 메인 컨트롤러**로 사용하며, Arduino Mega 2560을 통해 5개의 리니어 모터를 제어하고, U2D2를 통해 2개의 DYNAMIXEL XL430-W250-T를 제어합니다.

---

## 1. 시스템 구성

| 장치                     | 수량 | 역할                   |
| ---------------------- | -: | -------------------- |
| Raspberry Pi 4         |  1 | 메인 컨트롤러 / ROS 2      |
| Arduino Mega 2560      |  1 | 리니어 모터 제어            |
| 4×4 Matrix Keypad      |  1 | 사용자 입력               |
| I2C LCD 16×2           |  1 | 사용자 출력               |
| L298N                  |  3 | 리니어 모터 구동            |
| Linear Motor           |  5 | 등받이 구동               |
| U2D2                   |  1 | DYNAMIXEL 통신 인터페이스   |
| U2D2 Power Hub         |  1 | DYNAMIXEL 전원 및 통신 분배 |
| DYNAMIXEL XL430-W250-T |  2 | 추가 구동부               |
| 12V SMPS               |  1 | 모터 구동 전원             |
| 12V / 5V 어댑터           |  1 | Raspberry Pi 전원      |

---

# 2. 전체 결선 구조

```text
                             ┌──────────────────────┐
                             │   12V / 5V 어댑터    │
                             │      5V 설정         │
                             └──────────┬───────────┘
                                        │
                                       5V
                                        │
                                        ▼
                             ┌──────────────────────┐
                             │    Raspberry Pi 4    │
                             │     Main Controller  │
                             └──────────┬───────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                  USB                 GPIO                  I2C
                    │                   │                   │
                    ▼                   ▼                   ▼
          ┌─────────────────┐   ┌──────────────┐   ┌──────────────┐
          │ Arduino Mega    │   │ 4×4 Keypad   │   │ I2C LCD 16×2 │
          │     2560        │   └──────────────┘   └──────────────┘
          └────────┬────────┘
                   │
              Motor Control
                   │
       ┌───────────┼───────────┐
       │           │           │
       ▼           ▼           ▼
 ┌───────────┐ ┌───────────┐ ┌───────────┐
 │ L298N #1  │ │ L298N #2  │ │ L298N #3  │
 │   M1/M2   │ │   M3/M4   │ │    M5     │
 └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
       │              │              │
     ┌─┴─┐          ┌─┴─┐            │
     ▼   ▼          ▼   ▼            ▼
    M1   M2         M3   M4           M5


                             Raspberry Pi 4
                                  │
                                  │ USB
                                  ▼
                                U2D2
                                  │
                                  │ 3핀 케이블
                                  ▼
                         ┌──────────────────┐
                         │ U2D2 Power Hub   │
                         └───────┬─────┬────┘
                                 │     │
                               3핀   3핀
                                 │     │
                                 ▼     ▼
                              XL430   XL430
                               #1      #2


                       ┌────────────────────┐
                       │      12V SMPS      │
                       │   Motor Power      │
                       └─────────┬──────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
               L298N ×3                U2D2 Power Hub
                    │                         │
                    ▼                         ▼
              Linear Motor ×5          XL430 ×2
```

---

# 3. 전원 계통

## 3.1 Raspberry Pi 전원

```text
12V / 5V 어댑터
       │
       │ 5V 설정
       ▼
Raspberry Pi 4
```

* Raspberry Pi 4 전용 전원
* 어댑터 출력은 **5V로 설정**
* Raspberry Pi에 12V를 직접 연결하지 않음
* 별도의 Buck Converter는 사용하지 않음

---

## 3.2 Arduino 로직 전원

```text
Raspberry Pi 4
      │
      │ USB
      ▼
Arduino Mega 2560
      │
      └── Arduino 로직 전원
```

Raspberry Pi와 Arduino Mega는 USB로 연결하며 USB를 통해 통신과 Arduino 로직 전원을 공급합니다.

> Arduino의 로직 전원과 모터 구동 전원은 분리되어 있습니다.

---

## 3.3 리니어 모터 전원

```text
12V SMPS
   │
   ├────────────► L298N #1 ─────► Linear Motor #1
   │                           └─► Linear Motor #2
   │
   ├────────────► L298N #2 ─────► Linear Motor #3
   │                           └─► Linear Motor #4
   │
   └────────────► L298N #3 ─────► Linear Motor #5
```

* 리니어 모터 구동 전원: **12V**
* 12V SMPS에서 L298N 3개로 전원 공급
* L298N이 Arduino의 제어 신호를 받아 리니어 모터를 구동

---

## 3.4 DYNAMIXEL 전원

```text
12V SMPS
    │
    │ 12V DC
    ▼
U2D2 Power Hub
    │
    ├────────────► XL430-W250-T #1
    │                 3핀 케이블
    │
    └────────────► XL430-W250-T #2
                      3핀 케이블
```

DYNAMIXEL XL430-W250-T는 U2D2 Power Hub에서 전원과 통신을 공급받습니다.

두 DYNAMIXEL은 **Power Hub에서 각각 별도의 3핀 케이블로 직접 연결**합니다.

---

# 4. Raspberry Pi ↔ Arduino Mega

```text
Raspberry Pi 4
      │
      │ USB
      │
      ▼
Arduino Mega 2560
```

### 연결 기능

| 연결     | 기능            |
| ------ | ------------- |
| USB    | Serial 통신     |
| USB 5V | Arduino 로직 전원 |

Arduino는 Raspberry Pi에서 전달되는 모터 명령을 받아 L298N을 제어합니다.

---

# 5. Raspberry Pi ↔ I2C LCD

사용 LCD:

* 16×2 I2C LCD
* PCF8574 I2C Backpack
* I2C Address: `0x27`

| LCD | Raspberry Pi | Physical Pin | 기능      |
| --- | ------------ | -----------: | ------- |
| VCC | 5V           |            2 | 전원      |
| GND | GND          |            6 | 접지      |
| SDA | GPIO 2       |            3 | I2C SDA |
| SCL | GPIO 3       |            5 | I2C SCL |

### 결선

```text
Raspberry Pi 4              I2C LCD
────────────────────────────────────
Pin 2  (5V)       ────────► VCC
Pin 6  (GND)      ────────► GND
Pin 3  (GPIO 2)   ────────► SDA
Pin 5  (GPIO 3)   ────────► SCL
```

---

# 6. Raspberry Pi ↔ 4×4 Matrix Keypad

| Keypad | Raspberry Pi BCM GPIO | Physical Pin |
| ------ | --------------------: | -----------: |
| R1     |                GPIO 5 |           29 |
| R2     |                GPIO 6 |           31 |
| R3     |               GPIO 13 |           33 |
| R4     |               GPIO 19 |           35 |
| C1     |               GPIO 26 |           37 |
| C2     |               GPIO 12 |           32 |
| C3     |               GPIO 16 |           36 |
| C4     |               GPIO 20 |           38 |

### 결선

```text
4×4 Matrix Keypad             Raspberry Pi 4
──────────────────────────────────────────────
R1 ─────────────────────────► GPIO 5
R2 ─────────────────────────► GPIO 6
R3 ─────────────────────────► GPIO 13
R4 ─────────────────────────► GPIO 19

C1 ─────────────────────────► GPIO 26
C2 ─────────────────────────► GPIO 12
C3 ─────────────────────────► GPIO 16
C4 ─────────────────────────► GPIO 20
```

---

# 7. Arduino Mega ↔ L298N

## Motor Pin Mapping

| Motor | L298N        | EN | IN1 | IN2 |
| ----- | ------------ | -: | --: | --: |
| M1    | L298N #1 A채널 | D2 | D22 | D23 |
| M2    | L298N #1 B채널 | D3 | D24 | D25 |
| M3    | L298N #2 A채널 | D4 | D26 | D27 |
| M4    | L298N #2 B채널 | D5 | D28 | D29 |
| M5    | L298N #3 A채널 | D6 | D30 | D31 |

---

# 8. L298N #1 결선

### Arduino → L298N

```text
Arduino Mega          L298N #1
───────────────────────────────
D2  ─────────────────► ENA
D22 ─────────────────► IN1
D23 ─────────────────► IN2

D3  ─────────────────► ENB
D24 ─────────────────► IN3
D25 ─────────────────► IN4
```

### 전원 및 모터

```text
12V SMPS (+) ───────► L298N #1 +12V / VS
12V SMPS (-) ───────► L298N #1 GND

L298N #1 OUT1 / OUT2 ─────► Linear Motor #1
L298N #1 OUT3 / OUT4 ─────► Linear Motor #2
```

---

# 9. L298N #2 결선

### Arduino → L298N

```text
Arduino Mega          L298N #2
───────────────────────────────
D4  ─────────────────► ENA
D26 ─────────────────► IN1
D27 ─────────────────► IN2

D5  ─────────────────► ENB
D28 ─────────────────► IN3
D29 ─────────────────► IN4
```

### 전원 및 모터

```text
12V SMPS (+) ───────► L298N #2 +12V / VS
12V SMPS (-) ───────► L298N #2 GND

L298N #2 OUT1 / OUT2 ─────► Linear Motor #3
L298N #2 OUT3 / OUT4 ─────► Linear Motor #4
```

---

# 10. L298N #3 결선

### Arduino → L298N

```text
Arduino Mega          L298N #3
───────────────────────────────
D6  ─────────────────► ENA
D30 ─────────────────► IN1
D31 ─────────────────► IN2
```

### 전원 및 모터

```text
12V SMPS (+) ───────► L298N #3 +12V / VS
12V SMPS (-) ───────► L298N #3 GND

L298N #3 OUT1 / OUT2 ─────► Linear Motor #5
```

> L298N #3의 B채널은 사용하지 않습니다.

---

# 11. Raspberry Pi ↔ U2D2

```text
Raspberry Pi 4
      │
      │ USB
      ▼
    U2D2
      │
      │ 3핀 케이블
      ▼
U2D2 Power Hub
```

U2D2는 Raspberry Pi와 USB로 통신하며, DYNAMIXEL 제어 명령을 TTL Half-Duplex 방식으로 전달합니다.

---

# 12. U2D2 ↔ U2D2 Power Hub

```text
U2D2
 │
 │ 3핀 케이블
 │
 ▼
U2D2 Power Hub
```

### 3핀 신호

| 신호   | 기능           |
| ---- | ------------ |
| GND  | Ground       |
| VDD  | DYNAMIXEL 전원 |
| DATA | TTL 통신       |

> U2D2와 U2D2 Power Hub 사이에는 **3핀 케이블 1개**를 사용합니다.

---

# 13. U2D2 Power Hub ↔ DYNAMIXEL

DYNAMIXEL XL430-W250-T 2개는 Power Hub에 각각 독립적으로 연결합니다.

```text
                    U2D2 Power Hub
                         │
             ┌───────────┴───────────┐
             │                       │
          3핀 케이블               3핀 케이블
             │                       │
             ▼                       ▼
     XL430-W250-T #1         XL430-W250-T #2
```

### DYNAMIXEL 구성

| 장치       | 연결                 |
| -------- | ------------------ |
| XL430 #1 | Power Hub → 3핀 케이블 |
| XL430 #2 | Power Hub → 3핀 케이블 |

> XL430 #1과 XL430 #2를 서로 데이지체인으로 연결하는 방식이 아니라, **Power Hub에서 각각 직접 연결**합니다.

---

# 14. DYNAMIXEL 전원 및 통신 구조

```text
                           Raspberry Pi 4
                                │
                                │ USB
                                ▼
                              U2D2
                                │
                                │ 3핀
                                ▼
                       ┌─────────────────┐
                       │ U2D2 Power Hub  │
                       └───────┬─────────┘
                               │
                   ┌───────────┴───────────┐
                   │                       │
                 3핀                     3핀
                   │                       │
                   ▼                       ▼
             XL430 #1                 XL430 #2
             ID: 1                    ID: 2
```

DYNAMIXEL의 ID는 소프트웨어 설정에 따라 변경할 수 있으며, 두 모터를 독립적으로 제어하기 위해 서로 다른 ID를 사용합니다.

---

# 15. 전체 전원 및 제어 구조

```text
                         ┌──────────────────────┐
                         │   12V / 5V 어댑터    │
                         │       5V 설정        │
                         └──────────┬───────────┘
                                    │
                                   5V
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Raspberry Pi 4    │
                         │     Main Controller  │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 │ USB              │ USB              │ GPIO / I2C
                 │                  │                  │
                 ▼                  ▼                  ├────► 4×4 Keypad
       ┌─────────────────┐       ┌───────┐             │
       │ Arduino Mega    │       │ U2D2  │             └────► I2C LCD
       │     2560        │       └───┬───┘
       └────────┬────────┘           │
                │                    │ 3핀
                │                    ▼
                │           ┌──────────────────┐
                │           │ U2D2 Power Hub   │
                │           └───────┬─────┬────┘
                │                   │     │
                │                 3핀   3핀
                │                   │     │
                │                   ▼     ▼
                │                XL430  XL430
                │                  #1     #2
                │
                │ Motor Control
                │
        ┌───────┼────────┐
        │       │        │
        ▼       ▼        ▼
     L298N #1 L298N #2 L298N #3
       │       │        │
      M1/M2   M3/M4     M5


                    ┌────────────────────┐
                    │      12V SMPS      │
                    │   모터 구동 전원    │
                    └─────────┬──────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
                 L298N ×3        U2D2 Power Hub
                    │                   │
                    ▼                   ▼
              Linear Motor ×5      XL430 ×2
```

---

# 16. 모터 배치

5개의 리니어 모터는 모두 등받이에 배치됩니다.

| Motor |     위치 |
| ----- | -----: |
| M1    | 150 mm |
| M2    | 320 mm |
| M3    | 490 mm |
| M4    | 660 mm |
| M5    | 830 mm |

```text
                 등받이

                  ▲
                  │
             M5  830 mm
                  │
                  │
             M4  660 mm
                  │
                  │
             M3  490 mm
                  │
                  │
             M2  320 mm
                  │
                  │
             M1  150 mm
                  │
                  ▼
```

M1~M5는 특정 신체 부위에 고정된 역할을 갖는 것이 아니라, 각 모터의 위치를 기반으로 계산되는 제어 알고리즘을 통해 등받이의 형상을 조절합니다.

---

# 17. 전체 핀맵 요약

## Raspberry Pi

| 장치        |    GPIO | Physical Pin |
| --------- | ------: | -----------: |
| LCD SDA   |  GPIO 2 |            3 |
| LCD SCL   |  GPIO 3 |            5 |
| LCD VCC   |      5V |            2 |
| LCD GND   |     GND |            6 |
| Keypad R1 |  GPIO 5 |           29 |
| Keypad R2 |  GPIO 6 |           31 |
| Keypad R3 | GPIO 13 |           33 |
| Keypad R4 | GPIO 19 |           35 |
| Keypad C1 | GPIO 26 |           37 |
| Keypad C2 | GPIO 12 |           32 |
| Keypad C3 | GPIO 16 |           36 |
| Keypad C4 | GPIO 20 |           38 |

## Arduino Mega

| Motor | EN | IN1 | IN2 |
| ----- | -: | --: | --: |
| M1    | D2 | D22 | D23 |
| M2    | D3 | D24 | D25 |
| M3    | D4 | D26 | D27 |
| M4    | D5 | D28 | D29 |
| M5    | D6 | D30 | D31 |

---

# 18. 전원 계통 요약

| 전원 공급원           | 공급 대상           |  전압 | 용도              |
| ---------------- | --------------- | --: | --------------- |
| 12V / 5V 어댑터     | Raspberry Pi 4  |  5V | Raspberry Pi 전원 |
| Raspberry Pi USB | Arduino Mega    |  5V | Arduino 로직 전원   |
| 12V SMPS         | L298N ×3        | 12V | 리니어 모터 구동       |
| 12V SMPS         | U2D2 Power Hub  | 12V | DYNAMIXEL 전원    |
| U2D2 Power Hub   | XL430-W250-T ×2 | 12V | DYNAMIXEL 구동    |

---

# 19. 결선 원칙

1. Raspberry Pi는 **5V 전원**을 사용합니다.
2. Raspberry Pi에 12V를 직접 공급하지 않습니다.
3. 별도의 Buck Converter는 사용하지 않습니다.
4. Arduino Mega는 Raspberry Pi USB를 통해 **로직 전원과 통신**을 공급받습니다.
5. 리니어 모터 5개는 **12V SMPS → L298N ×3** 구조로 구동합니다.
6. DYNAMIXEL 2개는 **12V SMPS → U2D2 Power Hub**를 통해 전원을 공급받습니다.
7. Raspberry Pi와 U2D2는 USB로 연결합니다.
8. U2D2와 U2D2 Power Hub는 **3핀 케이블**로 연결합니다.
9. XL430-W250-T #1과 #2는 Power Hub에서 **각각 별도의 3핀 케이블로 직접 연결**합니다.
10. L298N #1은 M1/M2, L298N #2는 M3/M4, L298N #3은 M5를 담당합니다.
11. Arduino Mega와 L298N의 제어 신호는 지정된 핀맵을 사용합니다.
12. Raspberry Pi의 LCD는 I2C를 사용합니다.
13. Raspberry Pi의 Keypad는 GPIO Matrix 방식으로 입력을 처리합니다.

---

# 20. 최종 연결 한눈에 보기

```text
                         ┌──────────────────┐
                         │  Raspberry Pi 4  │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼────────────────────┐
              │                   │                    │
             USB                 USB                 GPIO/I2C
              │                   │                    │
              ▼                   ▼                    ├── Keypad
       Arduino Mega             U2D2                   │
              │                   │                    └── LCD
              │                  3핀
              │                   │
              │                   ▼
              │           U2D2 Power Hub
              │              │       │
              │             3핀     3핀
              │              │       │
              │              ▼       ▼
              │           XL430    XL430
              │             #1       #2
              │
              │
        ┌─────┼─────┐
        │     │     │
        ▼     ▼     ▼
      L298N L298N  L298N
       #1    #2     #3
        │     │      │
       M1/   M3/     M5
       M2    M4


                    12V SMPS
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
          L298N ×3        U2D2 Power Hub
              │                 │
              ▼                 ▼
       Linear Motor ×5      XL430 ×2
```

---

## 주의

* **12V SMPS의 출력은 반드시 실제 12V인지 확인**합니다.
* XL430-W250-T의 허용 전원 범위를 초과하는 전압을 공급하지 않습니다.
* 모터 구동 전원과 Raspberry Pi 전원을 임의로 연결하지 않습니다.
* 배선 작업 및 전원 인가 전에는 극성(`+ / -`)과 GND를 반드시 확인합니다.
* L298N의 모터 출력에는 리니어 모터를 연결하고, DYNAMIXEL은 L298N에 연결하지 않습니다.
* DYNAMIXEL은 **U2D2 + U2D2 Power Hub를 통해 직접 연결**합니다.
