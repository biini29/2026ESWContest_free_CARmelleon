
## 1. 전체 구조 개요

본 프로젝트는 실제 차량용 컴포트 시트 메커니즘을 검증하기 위해 제작된 **2:1 축소 스케일 프로토타입**입니다. 실물 시트의 기하학적 형상과 기계적 동작 원리를 유지하면서, 부스 전시 규격 제약과 3D 프린터 출력 가능 범위를 고려하여 외형 및 동작 스트로크 비율을 50% 축소 적용하였습니다.

이 축소 모형을 통해 5개의 리니어 액추에이터를 활용한 등받이 요추(Lumber) 제어 및 다이나믹셀 기반의 능동형 안전벨트 장력 조절 메커니즘을 소형 공간 내에서 직관적으로 검증할 수 있습니다.

![전체 조립도](3D_model/screenshot/render%20image.png)

---

## 2. 등받이(백레스트) 구조

등받이 내부에는 총 5개의 리니어 액추에이터가 일정 간격으로 수직 배치되어 등받이 형상을 능동적으로 변형시킵니다. 액추에이터는 전용 고정 마운트 플레이트(`linear_motor_mount_plate`)에 구멍을 뚫어 렌치 볼트로 직접 결합·고정하였으며, 백레스트 메인 외각 프레임(`backrest_outer_frame`)에 안정적으로 장착됩니다.

- **액추에이터 결합 방식:** `linear_motor_mount_plate` 부품에 가공된 홀을 통해 리니어 액추에이터를 나사 체결로 직접 고정
- **액추에이터 간격 구현:** 방석 면 기준 하단부터 150mm, 320mm, 490mm, 660mm, 830mm 위치에 각각 고정되어 구동부 쉘(`backrest_shell`)을 밀어내는 방식으로 요추 지지 곡면 형성
- **연결 폴더:** [`Linear Moter Lumber Structure/`](./Linear%20Moter%20Lumber%20Structure/) 내부 자료 참고

| 항목 | 값 |
|---|---|
| 프레임 재질 | 3D 프린팅 (PLA/PETG) 및 프레임 구조물 |
| 액추에이터 고정 방식 | 마운트 플레이트(`linear_motor_mount_plate`) 타공 결합 |
| 등받이 곡면 재질 | 커스텀 프린팅 쉘 패널 (`backrest_shell`) |

---

## 3. 안전벨트 릴/가이드레일 구조

탑승자의 체형 및 시트 상태 변형에 반응하여 벨트 장력을 능동적으로 제어하기 위해 2개의 ROBOTIS DYNAMIXEL XL430 모터가 적용되었습니다.

- **릴 메커니즘:** 다이나믹셀 모터 축과 연결 커넥터(`motor-shaft connecter`)로 연결된 릴(`belt_drive_reel`)이 회전하며 벨트(`belt`)를 감거나 풀어 장력을 조절합니다.
- **주요 부품 구성:**
  - 모터 고정: `belt_motor_bracket`
  - 동력 전달: `belt_drive_shaft`, `motor-shaft connecter`
  - 벨트 가이드: `belt_guide` (벨트의 꼬임 방지 및 이송 경로 유지)
  - 외각 프레임: `seatbelt_outer_frame`

---

## 4. 헤드레스트 자리 — 초음파센서 ㄱ자 브라켓

탑승자의 앉은키(신장)를 실시간으로 측정하여 최적의 헤드레스트 위치 및 시트 제어 알고리즘을 수행하기 위해 초음파 센서(HC-SR04)가 설치됩니다.

- **설계 의도:** 센서를 상단에 안정적으로 지지하고 탑승자 머리 상단과의 거리를 수직 방향으로 정밀 측정하기 위한 ㄱ자 형상 브라켓 (`ultrasonic_sensor_bracket`) 활용
- **정확한 치수 연산:**
  - 센서 설치 높이: 바닥면 기준 585mm + 브라켓 오프셋 60mm = **645mm**
  - 방석 기준 오차 보정 높이: **방석 면 기준 570mm** 고정 (상세 내용은 [`Seat_Control_Algorithm.md`](../../04_Software/Seat_Control_Algorithm.md) 4절 참고)
- **부품 위치:**
  - 센서 고정 프레임: [`ultrasonic_sensor_holder_frame.step`](3D_model/partial_component/custom/custom_stp/ultrasonic_sensor_holder_frame.step)
  - 센서 브라켓: [`ultrasonic_sensor_bracket.step`](3D_model/partial_component/third_party/third_party_stp/ultrasonic_sensor_bracket.step)

---

## 5. 파일 목록

| 파일/폴더 경로 | 설명 | 주요 포함 파일 형식 |
|---|---|---|
| [`3D_model/assemble/`](3D_model/assemble/) | 전체 조립 3D 모델 파일 | `.step`, `.stl` |
| [`3D_model/partial_component/custom/`](3D_model/partial_component/custom/) | 자체 설계 커스텀 파트 모음 | `custom_stp/` (`.step`), `custom_stl/` (`.stl`) |
| [`3D_model/partial_component/third_party/`](3D_model/partial_component/third_party/) | 외부 제조사 및 오픈소스 CAD 데이터 | `third_party_stp/` (`.step`), `third_party_stl/` (`.stl`) |
| [`3D_model/screenshot/`](3D_model/screenshot/) | 모델링 설계 및 렌더링 이미지 | `.png` |
| [`Linear Moter Lumber Structure/`](Linear%20Moter%20Lumber%20Structure/) | 등받이 액추에이터 배치 상세 구조 | - |

---

## 6. 설계 시 고려한 제약사항

- **2:1 스케일로 인한 제약 및 해결:**
  - 모터 및 액추에이터 등 기성 상용 부품은 50% 축소가 불가능하므로, 전용 마운트 플레이트(`linear_motor_mount_plate`) 및 모터 커넥터를 별도 설계하여 내부 간섭을 해결하고 메커니즘을 소형 프레임 안에 매립.
- **전시 부스 규격 (2m × 2m):**
  - 2:1 축소 설계를 통해 제어 박스(`control_box`) 포함 전체 모형이 소형화되어 2m × 2m 전시 공간 내에 여유 있게 배치 가능.
- **운반 및 조립 편의성:**
  - 시트 하단(`seat_bottom`), 백레스트 외각 프레임(`backrest_outer_frame`), 제어 박스(`control_box`)가 모듈화되어 있어 분해 및 이동/재조립이 용이함.
