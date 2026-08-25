# 스마트 시트 전체 핀맵 (Pinout)

## 1. 시스템 구성

| 장치 | 수량 | 역할 |
|---|---:|---|
| Raspberry Pi 3 | 1 | 메인 컨트롤러 |
| 4×4 Matrix Keypad | 1 | 사용자 입력 |
| I2C LCD 16×2 | 1 | 사용자 정보 표시 |
| Arduino Mega 2560 | 1 | Linear Motor 제어 |
| L298N | 3 | Linear Motor 구동 |
| Linear Motor | 5 | 등받이 형상 조절 |
| U2D2 | 1 | DYNAMIXEL 통신 |
| U2D2 Power Hub | 1 | DYNAMIXEL 전원 및 통신 분배 |
| DYNAMIXEL XL430-W250-T | 2 | 시트 구동 |
| 12V SMPS | 1 | 모터 구동 전원 |
| 12V / 5V 어댑터 | 1 | Raspberry Pi 전원 |

---

## 2. Raspberry Pi 3 핀맵

### 2.1 I2C LCD

| LCD 핀 | Raspberry Pi 3 | Physical Pin | 기능 |
|---|---|---:|---|
| VCC | 5V | 2 | 전원 |
| GND | GND | 6 | 접지 |
| SDA | GPIO 2 | 3 | I2C SDA |
| SCL | GPIO 3 | 5 | I2C SCL |

**LCD I2C 주소:** `0x27`

### 2.2 4×4 Matrix Keypad

| Keypad 핀 | Raspberry Pi GPIO | Physical Pin | 기능 |
|---|---:|---:|---|
| R1 | GPIO 5 | 29 | Row 1 |
| R2 | GPIO 6 | 31 | Row 2 |
| R3 | GPIO 13 | 33 | Row 3 |
| R4 | GPIO 19 | 35 | Row 4 |
| C1 | GPIO 26 | 37 | Column 1 |
| C2 | GPIO 12 | 32 | Column 2 |
| C3 | GPIO 16 | 36 | Column 3 |
| C4 | GPIO 20 | 38 | Column 4 |

---

## 3. Raspberry Pi 3 ↔ Arduino Mega 2560

| 연결 | 방식 | 기능 |
|---|---|---|
| Raspberry Pi 3 → Arduino Mega 2560 | USB | Serial 통신 |
| Raspberry Pi 3 → Arduino Mega 2560 | USB 5V | Arduino 로직 전원 |

```text
Raspberry Pi 3
      │
      │ USB
      ▼
Arduino Mega 2560
```

---

## 4. Arduino Mega 2560 ↔ L298N 전체 핀맵

| Motor | L298N | EN | IN1 | IN2 | 출력 |
|---|---|---|---|---|---|
| M1 | L298N #1 | D2 | D22 | D23 | OUT1 / OUT2 |
| M2 | L298N #1 | D3 | D24 | D25 | OUT3 / OUT4 |
| M3 | L298N #2 | D4 | D26 | D27 | OUT1 / OUT2 |
| M4 | L298N #2 | D5 | D28 | D29 | OUT3 / OUT4 |
| M5 | L298N #3 | D6 | D30 | D31 | OUT1 / OUT2 |

---

## 5. L298N #1

| Arduino Mega | L298N #1 | 기능 |
|---|---|---|
| D2 | ENA | M1 속도 제어 |
| D22 | IN1 | M1 방향 제어 |
| D23 | IN2 | M1 방향 제어 |
| D3 | ENB | M2 속도 제어 |
| D24 | IN3 | M2 방향 제어 |
| D25 | IN4 | M2 방향 제어 |

**출력 연결:**
- OUT1 / OUT2 → Linear Motor #1  
- OUT3 / OUT4 → Linear Motor #2  

---

## 6. L298N #2

| Arduino Mega | L298N #2 | 기능 |
|---|---|---|
| D4 | ENA | M3 속도 제어 |
| D26 | IN1 | M3 방향 제어 |
| D27 | IN2 | M3 방향 제어 |
| D5 | ENB | M4 속도 제어 |
| D28 | IN3 | M4 방향 제어 |
| D29 | IN4 | M4 방향 제어 |

**출력 연결:**
- OUT1 / OUT2 → Linear Motor #3  
- OUT3 / OUT4 → Linear Motor #4  

---

## 7. L298N #3

| Arduino Mega | L298N #3 | 기능 |
|---|---|---|
| D6 | ENA | M5 속도 제어 |
| D30 | IN1 | M5 방향 제어 |
| D31 | IN2 | M5 방향 제어 |

**출력 연결:**
- OUT1 / OUT2 → Linear Motor #5  
- OUT3 / OUT4 → 사용하지 않음  

---

## 8. Linear Motor 배치

| Motor | 위치 |
|---|---|
| M1 | 150 mm |
| M2 | 320 mm |
| M3 | 490 mm |
| M4 | 660 mm |
| M5 | 830 mm |

---

## 9. Raspberry Pi 3 ↔ U2D2

| 연결 | 방식 | 기능 |
|---|---|---|
| Raspberry Pi 3 → U2D2 | USB | DYNAMIXEL 통신 |

---

## 10. U2D2 ↔ U2D2 Power Hub

| 연결 | 케이블 | 기능 |
|---|---|---|
| U2D2 → U2D2 Power Hub | 3핀 | DYNAMIXEL 통신 및 전원 버스 |

---

## 11. U2D2 Power Hub ↔ DYNAMIXEL

| DYNAMIXEL | Power Hub 연결 | 케이블 |
|---|---|---|
| XL430-W250-T #1 | Power Hub Port 1 | 3핀 |
| XL430-W250-T #2 | Power Hub Port 2 | 3핀 |

---

## 12. DYNAMIXEL 전체 연결

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

## 13. 전원 연결

### 13.1 Raspberry Pi 3
- 12V / 5V 어댑터 → 5V → Raspberry Pi 3  

### 13.2 Arduino Mega 2560
- Raspberry Pi 3 USB → 5V → Arduino Mega 2560 로직 전원  

### 13.3 L298N
- 12V SMPS → L298N #1  
- 12V SMPS → L298N #2  
- 12V SMPS → L298N #3  

### 13.4 U2D2 Power Hub
- 12V SMPS → U2D2 Power Hub  

---

## 14. 전체 전원 및 통신 구조

```text
12V / 5V 어댑터 (5V) ──► Raspberry Pi 3
Raspberry Pi 3 ──► USB ──► Arduino Mega
Raspberry Pi 3 ──► USB ──► U2D2 ──► U2D2 Power Hub ──► XL430 #1, XL430 #2
Arduino Mega ──► L298N #1, #2, #3 ──► Linear Motor M1~M5
12V SMPS ──► L298N ×3, U2D2 Power Hub
```

---

## 15. 전체 핀맵 요약

### Raspberry Pi 3

| 장치 | GPIO | Physical Pin | 기능 |
|---|---|---|---|
| LCD SDA | GPIO 2 | 3 | I2C SDA |
| LCD SCL | GPIO 3 | 5 | I2C SCL |
| LCD VCC | 5V | 2 | 전원 |
| LCD GND | GND | 6 | 접지 |
| Keypad R1 | GPIO 5 | 29 | Row 1 |
| Keypad R2 | GPIO 6 | 31 | Row 2 |
| Keypad R3 | GPIO 13 | 33 | Row 3 |
| Keypad R4 | GPIO 19 | 35 | Row 4 |
| Keypad C1 | GPIO
## 16. 주의사항

- Raspberry Pi 3에 12V를 직접 연결하지 않습니다.  
- Raspberry Pi 3는 5V 전원을 사용합니다.  
- Arduino Mega 2560은 Raspberry Pi 3 USB를 통해 로직 전원을 공급받습니다.  
- Linear Motor 구동 전원은 12V SMPS를 사용합니다.  
- L298N #1은 M1/M2를 제어합니다.  
- L298N #2는 M3/M4를 제어합니다.  
- L298N #3은 M5를 제어합니다.  
- U2D2는 Raspberry Pi 3와 USB로 연결합니다.  
- U2D2와 U2D2 Power Hub는 3핀 케이블로 연결합니다.  
- XL430-W250-T #1, #2는 Power Hub에 각각 3핀 케이블로 연결합니다.  
- DYNAMIXEL 전원은 U2D2 Power Hub를 통해 공급합니다.  
- Raspberry
