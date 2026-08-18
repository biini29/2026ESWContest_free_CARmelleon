# ROS 2 시스템 전체 실행

## 1. 개요

본 프로젝트의 ROS 2 시스템 전체를 한 번에 실행하기 위한 Launch 파일이다.

Launch 파일을 실행하면 스마트 시트 시스템에 필요한 5개의 ROS 2 노드가 동시에 실행된다.

### 실행되는 노드

| 노드 이름                    | 실행 파일                       | 주요 역할                                 |
| ------------------------ | --------------------------- | ------------------------------------- |
| `arduino_bridge_node`    | `arduino_bridge_node.py`    | Raspberry Pi와 Arduino 간 통신 및 모터 명령 전달 |
| `profile_inference_node` | `profile_inference_node.py` | 사용자 데이터를 기반으로 좌석 프로파일 추론              |
| `seat_controller_node`   | `seat_controller_node.py`   | 목표 좌석 프로파일에 따른 좌석 제어                  |
| `keypad_node`            | `keypad_node.py`            | 키패드 입력 및 사용자 프로필 제어                   |
| `belt_controller_node`   | `belt_controller_node.py`   | 안전벨트 제어                               |

---

## 2. 시스템 구성

Launch 파일은 다음과 같은 구조로 ROS 2 노드를 실행한다.

```text
                    ┌─────────────────────────┐
                    │       keypad_node        │
                    │     키패드 입력 처리      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ profile_inference_node  │
                    │   사용자 프로파일 추론   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  seat_controller_node   │
                    │      좌석 제어 처리       │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  arduino_bridge_node    │
                    │   Arduino 통신 / 모터제어 │
                    └────────────┬────────────┘
                                 │
                                 ▼
                         ┌──────────────┐
                         │   Arduino    │
                         │ 모터 드라이버 │
                         └──────────────┘

                    ┌─────────────────────────┐
                    │  belt_controller_node   │
                    │       안전벨트 제어       │
                    └─────────────────────────┘
```

> 실제 ROS 2 통신 구조는 각 노드의 Publisher / Subscriber 설정에 따라 달라질 수 있으며, 위 구조는 Launch 파일에서 실행되는 주요 노드의 역할을 나타낸다.

---

## 3. 실행 전 준비

### 3.1 ROS 2 환경 설정

터미널에서 ROS 2 Humble 환경을 불러온다.

```bash
source /opt/ros/humble/setup.bash
```

### 3.2 ROS 2 Workspace 설정

프로젝트의 Workspace를 빌드한 후 환경을 불러온다.

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

매번 `source` 명령을 입력하기 어려운 경우 `~/.bashrc`에 등록할 수 있다.

```bash
source ~/ros2_ws/install/setup.bash
```

---

## 4. Arduino 연결 확인

Arduino를 Raspberry Pi에 연결한 후 장치가 정상적으로 인식되는지 확인한다.

```bash
ls /dev/ttyUSB*
```

Arduino가 정상적으로 연결되어 있다면 다음과 같이 표시될 수 있다.

```text
/dev/ttyUSB0
```

Arduino Bridge Node에서 사용하는 포트와 실제 연결된 포트가 동일한지 확인한다.

---

## 5. 시스템 전체 실행

ROS 2 환경과 Workspace를 설정한 후 Launch 파일을 실행한다.

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

이후 다음 명령어를 실행한다.

```bash
ros2 launch smart_seat [launch파일명].py
```

예를 들어 Launch 파일 이름이 `smart_seat.launch.py`라면:

```bash
ros2 launch smart_seat smart_seat.launch.py
```

Launch 파일을 실행하면 다음 5개의 노드가 동시에 실행된다.

```text
arduino_bridge_node
profile_inference_node
seat_controller_node
keypad_node
belt_controller_node
```

---

## 6. 실행 확인

새로운 터미널을 열고 ROS 2 환경을 다시 설정한다.

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

### 실행 중인 노드 확인

```bash
ros2 node list
```

정상적으로 실행되었다면 다음 노드들이 표시되어야 한다.

```text
/arduino_bridge_node
/profile_inference_node
/seat_controller_node
/keypad_node
/belt_controller_node
```

### ROS 2 Topic 확인

```bash
ros2 topic list
```

현재 실행 중인 노드들이 사용하는 Topic이 정상적으로 생성되었는지 확인한다.

### 특정 Topic의 연결 상태 확인

예:

```bash
ros2 topic info /motor_cmd
```

Publisher와 Subscriber가 정상적으로 연결되어 있는지 확인한다.

---

## 7. Arduino Bridge Node 확인

Arduino와 Raspberry Pi의 통신이 정상적으로 연결되었는지 Launch 터미널의 로그를 확인한다.

정상적으로 연결되면 다음과 같은 형태의 메시지가 출력된다.

```text
아두이노 연결 성공: /dev/ttyUSB0 @ 115200
```

또한 모터 명령이 전달될 경우 다음과 같은 로그가 출력될 수 있다.

```text
모터 명령 전송: M,1,1,200
```

---

## 8. 시스템 종료

Launch로 실행된 전체 시스템을 종료하려면 Launch가 실행 중인 터미널에서 다음을 입력한다.

```text
Ctrl + C
```

Launch 파일에서 실행한 모든 ROS 2 노드가 함께 종료된다.

---

## 9. 문제 발생 시 확인

### 노드가 실행되지 않는 경우

```bash
ros2 node list
```

를 사용하여 필요한 노드가 실행되고 있는지 확인한다.

### Arduino가 인식되지 않는 경우

```bash
ls /dev/ttyUSB*
```

를 실행하여 Arduino 장치가 존재하는지 확인한다.

### `/motor_cmd` 연결 확인

```bash
ros2 topic info /motor_cmd
```

`Subscription count`가 0인 경우 모터 명령을 받을 Subscriber가 실행되지 않은 상태일 수 있으므로 `arduino_bridge_node`가 정상적으로 실행되었는지 확인한다.

### 패키지를 찾을 수 없는 경우

```text
Package 'smart_seat' not found
```

와 같은 오류가 발생하면 다음 명령어를 실행한다.

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

필요한 경우 Workspace를 다시 빌드한다.

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

---

## 10. Launch 파일 구성

현재 Launch 파일에서는 ROS 2 콘솔 출력 형식을 설정한 후 5개의 노드를 실행한다.

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable


def generate_launch_description():
    return LaunchDescription([
        SetEnvironmentVariable(
            'RCUTILS_COLORIZED_OUTPUT',
            '1'
        ),

        SetEnvironmentVariable(
            'RCUTILS_CONSOLE_OUTPUT_FORMAT',
            '[{name}] {message}'
        ),

        Node(
            package='smart_seat',
            executable='arduino_bridge_node.py',
            name='arduino_bridge_node',
            output='screen',
        ),

        Node(
            package='smart_seat',
            executable='profile_inference_node.py',
            name='profile_inference_node',
            output='screen',
        ),

        Node(
            package='smart_seat',
            executable='seat_controller_node.py',
            name='seat_controller_node',
            output='screen',
        ),

        Node(
            package='smart_seat',
            executable='keypad_node.py',
            name='keypad_node',
            output='screen',
        ),

        Node(
            package='smart_seat',
            executable='belt_controller_node.py',
            name='belt_controller_node',
            output='screen',
        ),
    ])
```

---

## 11. 전체 실행 순서

```text
① Raspberry Pi 전원 ON
        ↓
② Arduino 연결
        ↓
③ ROS 2 Humble 환경 설정
        ↓
④ smart_seat Workspace 환경 설정
        ↓
⑤ Arduino 연결 상태 확인
        ↓
⑥ Launch 파일 실행
        ↓
⑦ 5개 ROS 2 Node 실행
        ↓
⑧ Node / Topic 연결 상태 확인
        ↓
⑨ 스마트 시트 시스템 동작
```
