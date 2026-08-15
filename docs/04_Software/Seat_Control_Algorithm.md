
# Seat Control Algorithm

키(신장) 입력 하나로 등받이 곡선과 안전벨트 높이를 계산하는 알고리즘 전체를 정리한 문서입니다. 실물 대비 2:1 축소 모형이라는 전제 하에, 모든 계산식은 **실물 기준으로 유도한 뒤 마지막에 스케일(0.5)을 적용**하는 구조로 통일했습니다.

---

## 1. 앉은키 회귀식 (Size Korea 8차 인체치수조사)

유효 표본 5,092명 데이터를 선형 회귀 분석하여 도출했습니다.

```
앉은키(mm) = 4.2999 × 키(cm) + 0.2129 × 몸무게(kg) + 171.2187
결정계수 R² = 0.842
```

- 몸무게의 영향력은 키의 약 1/20 수준으로 미미하여, 키패드 프로필/게스트 입력 시 몸무게는 65kg 고정값을 사용합니다.
- 설계 적용 범위: 키 130~185cm (185cm = 한국 성인 남성 99백분위수 기준)

---

## 2. 등받이 곡선 — 가우시안 보간

리니어 액추에이터 5개가 각각 150 / 320 / 490 / 660 / 830mm(실물 기준) 높이에 배치되어 있습니다. 천+솜 구조의 좌석 표면을 5개의 독립된 점이 아니라 **연속된 곡면**으로 근사하기 위해, 각 액추에이터의 밀기량을 가우시안 함수로 계산합니다.

### 2-1. 요추(허리) 곡선

```python
lumbar_apex = 앉은키 × LUMBAR_RATIO
push_lumbar(motor_h) = LUMBAR_MAX_PUSH × exp( -((motor_h - lumbar_apex) / LUMBAR_WIDTH)² )
```

| 파라미터 | 일반 모드 | 임산부 모드 |
|---|---|---|
| `LUMBAR_RATIO` | 0.18 | 0.12 (정점을 낮춤) |
| `LUMBAR_MAX_PUSH` | 95.0mm | 55.0mm (약하게) |
| `LUMBAR_WIDTH` | 200.0mm | 250.0mm (넓게 분산) |

**임산부 모드를 별도로 두는 근거**: 일반적인 강한 요추 지지가 임신 중 요추 전만(lordosis)을 과도하게 만들거나 장골동맥을 압박할 위험이 있다는 인체공학 문헌에 근거하여, 정점을 낮추고 힘을 약하게, 대신 넓게 분산시켰습니다.

### 2-2. 머리 지지(헤드레스트) 곡선

```python
head_support = 앉은키 - HEAD_CG_OFFSET   # HEAD_CG_OFFSET = 90.0mm
push_head(motor_h) = HEAD_MAX_PUSH × exp( -((motor_h - head_support) / HEAD_WIDTH)² )
# HEAD_MAX_PUSH = 40.0mm, HEAD_WIDTH = 150.0mm
```

### 2-3. 최종 밀기량 결정

```python
push(motor_h) = max(push_lumbar(motor_h), push_head(motor_h))
push = min(push, MAX_STROKE_MM)   # 액추에이터 최대 스트로크로 제한
scaled_push = push × SCALE        # SCALE = 0.5 (2:1 축소 모형 반영)
```

하나의 물리 모터가 사용자 키에 따라 요추 지지 역할과 머리 지지 역할을 겸합니다. 예: 키가 작으면 상단 모터가 요추보다 머리 지지 값이 더 커져 자동으로 헤드레스트 역할로 전환됩니다.

---

## 3. 안전벨트 높이 계산

### 3-1. 목표 높이 (실물 기준)

| 모드 | 계산식 | 근거 |
|---|---|---|
| 일반 | `앉은키 × 0.80` (어깨 중앙) | 자동차 안전 매뉴얼 공통 기준: 벨트는 어깨 중앙을 지나야 함(목이면 위험, 팔 아래면 이탈 위험) |
| 임산부 | 고정값 125.0mm (골반) | 100~150mm 범위의 중간값, 복부 압박 방지 |

> "성인 평균 체형(AM50: 175cm·78kg)" 기준 설계의 한계를 데이터로 보정한다는 것이 이 프로젝트의 핵심 차별점입니다. AM50과 대비되는 5th percentile 여성 더미(152cm·50kg)는 최근에야 일부 도입되기 시작했다는 점도 이 설계 방향의 근거입니다.

### 3-2. 좌표계 — 방석 표면을 원점(0mm)으로 통일

```
바닥(0mm) → 방석 표면(75mm, 기준 원점) → 벨트 홈 포지션(실측) → 목표 높이
```

모든 벨트 관련 계산은 "방석 표면 = 0mm" 기준 하나로 통일하여 계산 오차를 방지합니다.

### 3-3. 모형 변환 및 틱 변환

```python
target_model_mm = target_real_mm × SCALE + BELT_CALIBRATION_OFFSET_MM
# SCALE = 0.5
# BELT_CALIBRATION_OFFSET_MM = 25.0  (실측 보정값, 아래 3-4 참고)

필요틱수 = (target_model_mm - BELT_HOME_ABOVE_CUSHION) × BELT_TICKS_PER_MM
# BELT_HOME_ABOVE_CUSHION = -45.0  (홈이 방석보다 45mm 아래)
# BELT_TICKS_PER_MM = 37.3         (실측 캘리브레이션 값)
```

### 3-4. 실측 캘리브레이션 근거

- 이론값(릴 지름 25mm 기준 원주 계산)이 아니라, 실제로 500mm를 이동시켜 측정한 값(약 18,449틱)으로 틱/mm 비율을 도출했습니다.
- A/B/C 세 프로필로 실측한 결과, 계산값이 실제 도달 높이보다 18~30mm씩 항상 부족하게 나와 평균 **+25mm 보정값**을 추가로 적용했습니다.

---

## 4. 초음파 자동 키 추정 (게스트 모드)

D키 3초 롱프레스 시, 방석 위 570mm(모형 기준)에 설치된 HC-SR04 초음파 센서로 앉은키를 자동 측정합니다.

```python
model_sitting_height = SENSOR_HEIGHT_ABOVE_CUSHION_MM - distance_mm   # 570.0 - 측정거리
real_sitting_height = model_sitting_height × 2.0                       # 모형 → 실물 환산 (2:1의 역)

# 1절의 회귀식을 키(h)에 대해 역산
h = (real_sitting_height - SIT_B × 65.0 - SIT_C) / SIT_A
```

- `130.0 ≤ h ≤ 185.0`이면 즉시 적용, 범위를 벗어나면 LCD에 `Applicable Range 130~185cm` 표시 후 미적용
- 센서 설치 높이(570mm) 산출 근거: 바닥에서 585mm 위치에 고정대, 60mm 브라켓으로 하향 장착 → 총 645mm(바닥 기준) − 75mm(방석 두께) = 570mm(방석 기준)

---

## 5. 핵심 상수 요약

```python
SIT_A, SIT_B, SIT_C = 4.2999, 0.2129, 171.2187   # 앉은키 회귀식
SCALE = 0.5                                       # 2:1 축소 모형

LUMBAR_RATIO, LUMBAR_MAX_PUSH, LUMBAR_WIDTH = 0.18, 95.0, 200.0
PREG_LUMBAR_RATIO, PREG_LUMBAR_MAX_PUSH, PREG_LUMBAR_WIDTH = 0.12, 55.0, 250.0
HEAD_CG_OFFSET, HEAD_MAX_PUSH, HEAD_WIDTH = 90.0, 40.0, 150.0
MOTOR_HEIGHTS = [150.0, 320.0, 490.0, 660.0, 830.0]
MAX_STROKE_MM = 100.0

BELT_SHOULDER_RATIO = 0.80
BELT_PREGNANT_TARGET_REAL = 125.0
BELT_HOME_ABOVE_CUSHION = -45.0
BELT_TICKS_PER_MM = 37.3
BELT_CALIBRATION_OFFSET_MM = 25.0

SENSOR_HEIGHT_ABOVE_CUSHION_MM = 570.0
GUEST_WEIGHT_KG = 65.0
```

## 6. 설계 범위와 한계

- 130~185cm 범위 밖(예: 초음파 자동측정에서 벗어난 경우)은 지원하지 않으며, 안내 메시지만 표시합니다.
- 몸무게를 항상 65kg 고정값으로 사용하므로, 실제 몸무게가 크게 다른 사용자는 앉은키 추정에 소폭 오차가 있을 수 있습니다(회귀식에서 몸무게 계수의 영향력 자체가 작아 오차 폭은 제한적입니다).
- 벨트 캘리브레이션(37.3틱/mm, +25mm 보정)은 현재 모형 개체에 대한 실측값으로, 하드웨어가 바뀌면(릴 교체, 재조립 등) 재실측이 필요합니다.
