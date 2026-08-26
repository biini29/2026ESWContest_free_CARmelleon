
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rclpy
from rclpy.node import Node
from smart_seat.msg import TargetSeatProfile
from std_msgs.msg import String
import threading
import time
NUM_MOTORS_CTRL = 5
# 각 모터 방향별 속도 (mm/s) — 아두이노 모터 번호(M1~M5) 기준
MOTOR_SPEED_OUT = [6.9, 4.4, 6.9, 6.9, 6.8]
MOTOR_SPEED_IN  = [4.5, 6.9, 6.9, 6.9, 6.8]
# 코드상 자리 순서(0=150mm ... 4=830mm) → 실제 아두이노 모터 번호(1~5)
# 150mm자리=M2, 320mm자리=M1 (1,2번 물리 스왑됨)
MOTOR_MAP = [2, 1, 3, 4, 5]
PWM_SPEED = 200
class SeatControllerNode(Node):
    def __init__(self):
        super().__init__('seat_controller_node')
        self.sub = self.create_subscription(
            TargetSeatProfile, '/target_seat_profile', self.on_profile, 10)
        self.cmd_pub = self.create_publisher(String, '/motor_cmd', 10)
        # 현재 위치는 '자리 순서' 기준으로 추적
        self.current_mm = [0.0] * NUM_MOTORS_CTRL
        self.serial_lock = threading.Lock()
        self.get_logger().info('seat_controller_node 시작됨 (모터매핑 적용). 대기 중...')
    def on_profile(self, msg):
        targets = list(msg.actuator_mm)
        # 리셋 신호
        if all(t <= 0 for t in targets):
            self.get_logger().info('=== 리셋 신호 수신 → 모터 전부 집어넣기 ===')
            threading.Thread(target=self.reset_all).start()
            return
        self.get_logger().info(f'목표 수신: {[round(t,1) for t in targets]} mm')
        threading.Thread(target=self.move_all, args=(targets,)).start()
    def reset_all(self):
        # 현재 위치 기준 필요 시간 계산 (제일 오래 걸리는 모터 + 여유 3초)
        max_time = 0.0
        for idx in range(NUM_MOTORS_CTRL):
            motor_num = MOTOR_MAP[idx]
            need = self.current_mm[idx] / MOTOR_SPEED_IN[motor_num - 1]
            max_time = max(max_time, need)
        reset_time = max_time + 3.0
        self.get_logger().info(f'  모터 전부 후진 ({reset_time:.1f}초)...')
        for idx in range(NUM_MOTORS_CTRL):
            self.send(f'M,{MOTOR_MAP[idx]},-1,{PWM_SPEED}')
        time.sleep(reset_time)
        self.get_logger().info('  1~5번 모터 정지 (2번 모터만 3초 추가 후진)...')
        for idx in range(NUM_MOTORS_CTRL):
            motor_num = MOTOR_MAP[idx]
            if motor_num != 2:
                self.send(f'M,{motor_num},0,0')
        time.sleep(3.0)
        self.send(f'M,2,0,0')
        self.current_mm = [0.0] * NUM_MOTORS_CTRL
        self.get_logger().info('=== 리셋 완료. 모든 모터 0mm,(2번 모터 3초 추가 후진 완료) ===')
    def move_all(self, targets):
        threads = []
        for i in range(len(targets)):
            t = threading.Thread(target=self.move_one, args=(i, targets[i]))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        self.get_logger().info('─── 모든 모터 이동 완료 ───')
    def move_one(self, idx, target_mm):
        motor_num = MOTOR_MAP[idx]        # 실제 아두이노 모터 번호
        speed_idx = motor_num - 1         # 속도 배열 인덱스 (아두이노 번호 기준)
        current = self.current_mm[idx]
        diff = target_mm - current
        if abs(diff) < 1.0:
            self.get_logger().info(f'  [자리{idx+1}/모터{motor_num}] 이미 목표 근처, 생략')
            return
        if diff > 0:
            direction = 1
            speed = MOTOR_SPEED_OUT[speed_idx]
        else:
            direction = -1
            speed = MOTOR_SPEED_IN[speed_idx]
        move_time = abs(diff) / speed
        self.get_logger().info(
            f'  [자리{idx+1}/모터{motor_num}] {current:.0f}->{target_mm:.0f}mm '
            f'({"밀기" if direction>0 else "당기기"}, {move_time:.1f}초)')
        self.send(f'M,{motor_num},{direction},{PWM_SPEED}')
        time.sleep(move_time)
        self.send(f'M,{motor_num},0,0')
        self.current_mm[idx] = target_mm
    def send(self, command):
        with self.serial_lock:
            msg = String()
            msg.data = command
            self.cmd_pub.publish(msg)
            time.sleep(0.05)
def main(args=None):
    rclpy.init(args=args)
    node = SeatControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
if __name__ == '__main__':
    main()
