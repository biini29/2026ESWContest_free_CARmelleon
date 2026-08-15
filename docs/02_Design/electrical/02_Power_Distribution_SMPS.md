# 전원 계통도

## 1. 전체 전원 구성

스마트 시트 시스템은 **12V DC 전원공급기**를 메인 전원으로 사용하며, 모터 구동 계통과 제어 계통을 분리하여 구성한다.

```text
                         AC 220V
                            │
                            ▼
                  ┌─────────────────┐
                  │  DC 12V Power   │
                  │    Supply       │
                  └────────┬────────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
           DC 12V                      DC 12V
             │                           │
             ▼                           ▼
    ┌─────────────────┐        ┌─────────────────┐
    │   Motor Power   │        │  Buck Converter │
    │      Bus        │        │     12V → 5V    │
    └────────┬────────┘        └────────┬────────┘
             │                          │
       ┌─────┼─────┐                    │ 5V
       │     │     │              ┌─────┴─────┐
       ▼     ▼     ▼              │           │
    L298N  L298N  L298N           ▼           ▼
      #1     #2     #3       Raspberry Pi  Arduino Mega
       │     │     │              │           │
      12V   12V   12V             │ USB       │
       │     │     │              └─────┬─────┘
       │     │     │                    │
       ▼     ▼     ▼                    │
     M1 M2  M3 M4  M5                    │
                                        │
                              LCD / Keypad / Control
```

## 2. 모터 전원 계통

리니어 모터 5개는 L298N 모터 드라이버 3개를 통해 구동한다.

```text
                    DC 12V Power Supply
                           │
                           ├───────────────┐
                           │               │
                           ▼               ▼
                       L298N #1         L298N #2
                       (12V/GND)        (12V/GND)
                        │    │           │    │
                        ▼    ▼           ▼    ▼
                       M1    M2          M3    M4

                           │
                           ▼
                       L298N #3
                       (12V/GND)
                           │
                           ▼
                           M5
```

### 모터 배치

| Motor Driver | Linear Motor     |
| ------------ | ---------------- |
| L298N #1     | Motor 1, Motor 2 |
| L298N #2     | Motor 3, Motor 4 |
| L298N #3     | Motor 5          |

## 3. 제어부 전원 계통

라즈베리파이는 Buck Converter를 이용하여 12V를 5V로 변환한 후 공급한다.

```text
DC 12V
  │
  ▼
┌─────────────────┐
│ Buck Converter  │
│    12V → 5V     │
└────────┬────────┘
         │ 5V
         ▼
┌─────────────────┐
│  Raspberry Pi   │
└────────┬────────┘
         │ USB
         ▼
┌─────────────────┐
│  Arduino Mega   │
└─────────────────┘
```

## 4. GND 공통 연결

모터 제어 신호가 정상적으로 전달되도록 각 제어 장치와 모터 드라이버의 GND를 공통으로 연결한다.

```text
                  12V Power Supply (-)
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
          L298N #1     L298N #2    L298N #3
             │           │           │
             └───────────┼───────────┘
                         │
                         ▼
                    Common GND
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
        Arduino Mega           Buck Converter
                                     │
                                     ▼
                                Raspberry Pi
```

## 5. 전원 계통 요약

| 구분              |     전압 | 공급원              | 대상                            |
| --------------- | -----: | ---------------- | ----------------------------- |
| 모터 전원           | 12V DC | 12V Power Supply | L298N #1~#3 → Linear Motor 5개 |
| Raspberry Pi 전원 |  5V DC | Buck Converter   | Raspberry Pi                  |
| Arduino 전원      |     5V | Raspberry Pi USB | Arduino Mega                  |
| LCD/Keypad      |     5V | 제어부 전원           | LCD 및 Keypad                  |
| GND             |     0V | 공통 GND           | 전체 제어 시스템                     |

> **주의:** 리니어 모터의 전원은 Raspberry Pi 또는 Arduino에서 직접 공급하지 않는다. 모터 구동 전원은 12V 전원공급기에서 L298N으로 공급한다.

> **주의:** 실제 제작 시에는 전원공급기의 정격 전류, Buck Converter의 출력 전류, 리니어 모터의 정격 전류를 확인하여 전원 용량을 결정한다.
