# 스마트 시트 전체 결선도 (Wiring Diagram)

스마트 시트 시스템의 Raspberry Pi, Arduino Mega, 4×4 Matrix Keypad, I2C LCD, L298N 모터 드라이버 및 5개의 리니어 모터의 전체 결선 구조를 정리한 문서입니다.

---

## 1. 전체 시스템 구성

```text
                         ┌─────────────────────────┐
                         │     12V / 5V 어댑터      │
                         │       (5V 설정)          │
                         └────────────┬────────────┘
                                      │ 5V
                                      ▼
                         ┌─────────────────────────┐
                         │     Raspberry Pi 4      │
                         │       Main Controller   │
                         └──────┬───────────┬──────┘
                                │           │
                         USB Serial         │ GPIO / I2C
                                │           │
                                ▼           ▼
                    ┌────────────────┐   ┌───────────────┐
                    │ Arduino Mega   │   │ 4×4 Keypad    │
                    │    2560        │   └───────────────┘
                    │ Motor Control  │
                    └───────┬────────┘   ┌───────────────┐
                            │             │ I2C LCD 16×2  │
                            │             │ PCF8574 0x27  │
                            │             └───────────────┘
                            │
                  ┌─────────┴─────────┐
                  │                   │
                  ▼                   ▼
          ┌──────────────┐     ┌──────────────┐
          │  L298N #1    │     │  L298N #2    │
          │ M1 + M2      │     │ M3 + M4      │
          └──────┬───────┘     └──────┬───────┘
                 │                    │
              ┌──┴──┐              ┌──┴──┐
              ▼     ▼              ▼     ▼
             M1     M2             M3     M4

                    ┌──────────────┐
                    │  L298N #3    │
                    │     M5       │
                    └──────┬───────┘
                           │
                           ▼
                          M5


     ┌─────────────────────────────────────────────┐
     │                 12V SMPS                     │
     │          모터 구동 전용 전원                  │
     └─────────────────────┬───────────────────────┘
                           │ 12V
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
         L298N #1      L298N #2      L298N #3
```

---

## 2. 전원 계통

### 2.1 Raspberry Pi 전원

```text
12V / 5V 겸용 어댑터
        │
        │ 5V 설정
        ▼
Raspberry Pi 4
```

* Raspberry Pi는 **5V 전용 전원**으로 공급
* 12V/5V 겸용 어댑터를 **5V로 설정**
* Raspberry Pi 전원 계통에는 **Buck Converter를 사용하지 않음**

---

### 2.2 Arduino Mega 로직 전원

```text
Raspberry Pi 4
      │
      │ USB
      ├──────────────► Arduino Mega 2560
      │                 (Arduino 로직 전원)
      │
      └──── USB Serial 통신
```

* Raspberry Pi USB를 통해 Arduino Mega에 연결
* USB를 통해 Arduino **로직 전원 및 통신** 수행
* Arduino의 모터 구동 전원과는 분리

> **주의:** Arduino의 로직 전원(5V)과 리니어 모터의 구동 전원(12V)은 별도의 전원 계통입니다.

---

### 2.3 모터 전원

```text
12V SMPS
   │
   ├────────────► L298N #1 ───► M1 / M2
   │
   ├────────────► L298N #2 ───► M3 / M4
   │
   └────────────► L298N #3 ───► M5
```

* 12V SMPS는 **모터 구동 전용**
* L298N 3개에 12V 공급
* Raspberry Pi 전원과 모터 전원은 독립
* **Buck Converter 없음**

---

## 3. Raspberry Pi ↔ LCD 결선

사용 LCD:

* 16×2 I2C LCD
* PCF8574 I2C Backpack
* I2C 주소: `0x27`

### LCD Pin Mapping

| LCD | Raspberry Pi | Physical Pin | 설명      |
| --- | ------------ | -----------: | ------- |
| VCC | 5V           |            2 | LCD 전원  |
| GND | GND          |            6 | 공통 접지   |
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

## 4. Raspberry Pi ↔ 4×4 Matrix Keypad 결선

### GPIO Mapping

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

> Keypad는 별도의 전원선을 사용하지 않고 GPIO를 이용하여 Matrix 방식으로 입력을 처리합니다.

---

## 5. Raspberry Pi ↔ Arduino Mega 통신

```text
Raspberry Pi 4
      │
      │ USB
      ▼
Arduino Mega 2560
      │
      │ Motor Control GPIO
      ▼
    L298N
```

Arduino Mega는 Raspberry Pi와 USB Serial 통신을 수행하며, Raspberry Pi에서 전달된 모터 명령을 받아 L298N을 제어합니다.

---

## 6. Arduino Mega ↔ L298N Pin Mapping

### Arduino Mega Motor Pin Map

| Motor | L298N        | EN | IN1 | IN2 |
| ----- | ------------ | -: | --: | --: |
| M1    | L298N #1 A채널 | D2 | D22 | D23 |
| M2    | L298N #1 B채널 | D3 | D24 | D25 |
| M3    | L298N #2 A채널 | D4 | D26 | D27 |
| M4    | L298N #2 B채널 | D5 | D28 | D29 |
| M5    | L298N #3 A채널 | D6 | D30 | D31 |

---

## 7. L298N #1 결선

### M1

```text
Arduino Mega
────────────────────
D2  ───────────────► ENA
D22 ───────────────► IN1
D23 ───────────────► IN2
```

### M2

```text
Arduino Mega
────────────────────
D3  ───────────────► ENB
D24 ───────────────► IN3
D25 ───────────────► IN4
```

### 전원

```text
12V SMPS (+) ─────► L298N #1 +12V / VS
12V SMPS (-) ─────► L298N #1 GND
```

### 모터

```text
L298N #1 OUT1 / OUT2 ─────► M1
L298N #1 OUT3 / OUT4 ─────► M2
```

---

## 8. L298N #2 결선

### M3

```text
Arduino Mega
────────────────────
D4  ───────────────► ENA
D26 ───────────────► IN1
D27 ───────────────► IN2
```

### M4

```text
Arduino Mega
────────────────────
D5  ───────────────► ENB
D28 ───────────────► IN3
D29 ───────────────► IN4
```

### 전원

```text
12V SMPS (+) ─────► L298N #2 +12V / VS
12V SMPS (-) ─────► L298N #2 GND
```

### 모터

```text
L298N #2 OUT1 / OUT2 ─────► M3
L298N #2 OUT3 / OUT4 ─────► M4
```

---

## 9. L298N #3 결선

### M5

```text
Arduino Mega
────────────────────
D6  ───────────────► ENA
D30 ───────────────► IN1
D31 ───────────────► IN2
```

### 전원

```text
12V SMPS (+) ─────► L298N #3 +12V / VS
12V SMPS (-) ─────► L298N #3 GND
```

### 모터

```text
L298N #3 OUT1 / OUT2 ─────► M5
```

> L298N #3의 B채널은 사용하지 않습니다.

---

## 10. 전체 모터 배치

5개의 리니어 모터는 모두 등받이 부분에 배치됩니다.

```text
        등받이
          │
          │
          ▼

     M1      150 mm
     │
     │
     M2      320 mm
     │
     │
     M3      490 mm
     │
     │
     M4      660 mm
     │
     │
     M5      830 mm
     │
     ▼
```

| Motor |     위치 |
| ----- | -----: |
| M1    | 150 mm |
| M2    | 320 mm |
| M3    | 490 mm |
| M4    | 660 mm |
| M5    | 830 mm |

각 모터는 고정된 신체 부위 역할을 갖는 것이 아니라, 모터 위치를 기반으로 계산되는 Gaussian Curve에 따라 허리 및 머리 부분의 압력/돌출 정도를 제어합니다.

---

## 11. 공통 GND 구성

모터 구동계와 Arduino 사이에는 공통 기준 전위를 유지해야 합니다.

```text
                    ┌──► L298N #1 GND
                    │
12V SMPS (-) ───────┼──► L298N #2 GND
                    │
                    ├──► L298N #3 GND
                    │
                    └──► Arduino Mega GND
```

### 중요

* 12V SMPS `(-)`와 L298N GND는 연결
* 각 L298N의 GND는 공통으로 구성
* Arduino Mega GND도 모터 제어 신호 기준을 위해 공통 GND에 연결
* Raspberry Pi의 전원은 별도 전원 계통으로 유지

---

## 12. 최종 전원 구조

```text
                       ┌─────────────────────┐
                       │ 12V / 5V 어댑터     │
                       │      5V 설정        │
                       └──────────┬──────────┘
                                  │
                                  │ 5V
                                  ▼
                       ┌─────────────────────┐
                       │ Raspberry Pi 4      │
                       └──────────┬──────────┘
                                  │
                           USB 5V + Serial
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Arduino Mega 2560   │
                       │ Arduino 로직 전원   │
                       └──────────┬──────────┘
                                  │
                         Motor Control Signal
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
        ┌───────────┐       ┌───────────┐       ┌───────────┐
        │ L298N #1  │       │ L298N #2  │       │ L298N #3  │
        │ M1 / M2   │       │ M3 / M4   │       │ M5        │
        └─────┬─────┘       └─────┬─────┘       └─────┬─────┘
              │                   │                   │
              ▼                   ▼                   ▼
            M1/M2               M3/M4                 M5


                       ┌─────────────────────┐
                       │      12V SMPS       │
                       │   모터 구동 전원    │
                       └──────────┬──────────┘
                                  │
                     ┌────────────┼────────────┐
                     │            │            │
                     ▼            ▼            ▼
                  L298N #1     L298N #2     L298N #3
```

---

## 13. 전체 결선 요약

| 장치             | 연결 대상        | 전원        | 통신/제어          |
| -------------- | ------------ | --------- | -------------- |
| Raspberry Pi 4 | Arduino Mega | 5V 전용 어댑터 | USB Serial     |
| Raspberry Pi 4 | LCD          | 5V        | I2C            |
| Raspberry Pi 4 | 4×4 Keypad   | GPIO      | GPIO Matrix    |
| Arduino Mega   | L298N #1     | 로직 5V     | D2, D22~D25    |
| Arduino Mega   | L298N #2     | 로직 5V     | D4~D5, D26~D29 |
| Arduino Mega   | L298N #3     | 로직 5V     | D6, D30~D31    |
| 12V SMPS       | L298N #1~#3  | 12V       | 모터 구동          |
| L298N #1       | M1, M2       | 12V       | H-Bridge       |
| L298N #2       | M3, M4       | 12V       | H-Bridge       |
| L298N #3       | M5           | 12V       | H-Bridge       |

---

## 14. 주의사항

1. **Raspberry Pi에는 12V를 직접 연결하지 않습니다.**
2. Raspberry Pi는 12V/5V 어댑터를 **5V로 설정하여 사용합니다.**
3. **Buck Converter는 사용하지 않습니다.**
4. Arduino Mega는 Raspberry Pi USB를 통한 **Arduino 로직 전원**을 사용합니다.
5. 리니어 모터의 구동 전원은 **12V SMPS**를 사용합니다.
6. 12V SMPS는 L298N 모터 구동계 전용입니다.
7. Raspberry Pi 전원과 모터 전원은 분리합니다.
8. L298N과 Arduino Mega의 GND는 공통 기준을 구성합니다.
9. L298N #1은 M1/M2, L298N #2는 M3/M4, L298N #3은 M5를 제어합니다.
10. M1~M5는 모두 등받이에 배치되며 위치 기반 제어 알고리즘으로 구동됩니다.

---

## 15. 최종 연결 구조 한눈에 보기

```text
                         [ 5V POWER ]
                              │
                              ▼
                     ┌────────────────┐
                     │ Raspberry Pi 4 │
                     └───────┬────────┘
                             │
                 ┌───────────┼────────────┐
                 │           │            │
                 ▼           ▼            ▼
             4×4 Keypad   I2C LCD    USB Serial
                                          │
                                          ▼
                                ┌──────────────────┐
                                │ Arduino Mega 2560│
                                └────────┬─────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
       ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
       │  L298N #1   │            │  L298N #2   │            │  L298N #3   │
       │   M1 / M2   │            │   M3 / M4   │            │     M5      │
       └──────┬──────┘            └──────┬──────┘            └──────┬──────┘
              │                          │                          │
           ┌──┴──┐                    ┌──┴──┐                       │
           ▼     ▼                    ▼     ▼                       ▼
          M1     M2                   M3     M4                      M5

                  ▲                          ▲                         ▲
                  │                          │                         │
                  └────────────── 12V SMPS ─┴─────────────────────────┘
```

**전원 원칙:**
`5V → Raspberry Pi → Arduino 로직`
`12V → L298N → 리니어 모터`

**제어 원칙:**
`Raspberry Pi → USB Serial → Arduino Mega → L298N → M1~M5`
<img width="1536" height="1024" alt="ChatGPT Image 2026년 8월 25일 오후 02_04_47" src="https://github.com/user-attachments/assets/4791b4f0-a0f2-4ea5-901c-6a21599526c2" />
