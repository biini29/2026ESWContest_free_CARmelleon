
# Profile Manager

`keypad_node.py` 안의 가족 프로필 로딩/관리 로직입니다.

## 저장 위치

```
~/ros2_ws/src/smart_seat/profiles.json
```

## 데이터 구조

```json
{
  "A": {"name": "PAPA",     "height": 178, "pregnant": false},
  "B": {"name": "MAMA",     "height": 162, "pregnant": true},
  "C": {"name": "DAUGHTER", "height": 130, "pregnant": false}
}
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `name` | string | LCD에 표시될 이름 |
| `height` | number | 신장(cm) |
| `pregnant` | boolean | 임산부 모드 여부 — `true`면 요추 곡선/벨트 목표가 임산부용 계산식으로 전환 |

## 로딩 동작

- 노드 시작 시 `load_profiles()`가 파일을 읽어 딕셔너리로 로드
- **파일이 없거나 파싱 실패 시**: 하드코딩된 기본값(A=PAPA 178cm, B=MAMA 162cm 임산부, C=DAUGHTER 130cm)으로 자동 대체하여 최소한의 시연 가능 상태를 보장

## 프로필 키 눌렀을 때 동작

```
A/B/C 중 하나 눌림
  → profiles[key] 조회
  → LCD: "Mode: {name}{(Preg) 표시}" / "Target: {height}cm"
  → send_height(height, pregnant) 호출 → /body_data 발행
```

## 프로필 값 변경 방법

`profiles.json`을 직접 수정하면 됩니다(코드 재빌드 불필요, 노드만 재시작). 팀원 실측 키로 갱신하거나, 시연 대상자에 맞춰 조정할 때 이 파일만 바꾸면 됩니다.

## 딸(C) 프로필 기준 키 관련 참고

초기값은 실측 아동 키(121cm)였으나, 어린이 인체치수 데이터 부재로 Size Korea 성인 데이터의 신뢰 구간 하한(130cm)에 맞춰 130cm로 조정했습니다. 시스템 설계 범위(130~185cm) 전체와 일관성을 유지하기 위한 결정입니다.
