
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy
from rclpy.node import Node
from smart_seat.msg import TargetSeatProfile
from dynamixel_sdk import *
import json
import os
import threading
import time


DEVICENAME = '/dev/belt_u2d2'
BAUDRATE = 1000000
PROTOCOL_VERSION = 2.0

ADDR_TORQUE_ENABLE = 64
ADDR_OPERATING_MODE = 11
ADDR_PROFILE_VELOCITY = 112
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132

EXTENDED_POSITION_MODE = 4
VELOCITY = 80
DXL_IDS = [2, 12]
HOME_PATH = os.path.expanduser('~/belt_home.json')

# 안전 클램프 (홈 기준 상대 틱)
TICK_MIN = 0
TICK_MAX = 20000


class BeltControllerNode(Node):
    def __init__(self):
        super().__init__('belt_controller_node')

        self.portHandler = PortHandler(DEVICENAME)
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)
        self.move_lock = threading.Lock()

        if not self.portHandler.openPort():
            self.get_logger().error('U2D2 포트 열기 실패')
        if not self.portHandler.setBaudRate(BAUDRATE):
            self.get_logger().error('보드레이트 설정 실패')

        with open(HOME_PATH) as f:
            self.home = json.load(f)
        self.get_logger().info(f'홈 포지션 로드: {self.home}')

        for dxl_id in DXL_IDS:
            self.packetHandler.write1ByteTxRx(self.portHandler, dxl_id, ADDR_TORQUE_ENABLE, 0)
            self.packetHandler.write1ByteTxRx(
                self.portHandler, dxl_id, ADDR_OPERATING_MODE, EXTENDED_POSITION_MODE)
            self.packetHandler.write4ByteTxRx(
                self.portHandler, dxl_id, ADDR_PROFILE_VELOCITY, VELOCITY)
            self.packetHandler.write1ByteTxRx(self.portHandler, dxl_id, ADDR_TORQUE_ENABLE, 1)

        self.sub = self.create_subscription(
            TargetSeatProfile, '/target_seat_profile', self.on_profile, 10)

        self.get_logger().info('belt_controller_node 시작됨. 목표 대기 중...')

        # 시작 시 한 번만 홈으로 이동 (별도 스레드)
        threading.Thread(target=self.go_home_on_startup).start()

    def get_pos(self, dxl_id):
        v, _, _ = self.packetHandler.read4ByteTxRx(
            self.portHandler, dxl_id, ADDR_PRESENT_POSITION)
        if v > 2**31:
            v -= 2**32
        return v

    def go_home_on_startup(self):
        with self.move_lock:
            self.get_logger().info('=== 시작 시 홈 복귀 시작 ===')
            for dxl_id in DXL_IDS:
                cur = self.get_pos(dxl_id)
                target = self.home[str(dxl_id)]
                self.get_logger().info(f'ID {dxl_id}: 현재={cur} -> 목표(홈)={target}')
                self.packetHandler.write4ByteTxRx(
                    self.portHandler, dxl_id, ADDR_GOAL_POSITION, target & 0xFFFFFFFF)

            targets = {dxl_id: self.home[str(dxl_id)] for dxl_id in DXL_IDS}
            self._wait_arrival(targets)
            self.get_logger().info('=== 홈 복귀 완료 ===')

    def on_profile(self, msg):
        # 리셋 신호는 무시 (허리만 리셋되고 벨트는 반응하지 않음 — 홈 복귀는 느려서)
        if all(t < 0 for t in msg.actuator_mm):
            self.get_logger().info('리셋 신호 수신 - 벨트는 반응 안 함 (허리만 리셋)')
            return

        ticks_needed = msg.belt_height_cm
        ticks_needed = max(TICK_MIN, min(TICK_MAX, int(ticks_needed)))
        self.get_logger().info(f'벨트 목표 수신: {ticks_needed}틱 (홈 기준, 클램프 적용)')
        threading.Thread(target=self.move_to, args=(ticks_needed,)).start()

    def move_to(self, ticks_needed):
        with self.move_lock:
            targets = {}
            for dxl_id in DXL_IDS:
                home_pos = self.home[str(dxl_id)]
                pos = home_pos - int(ticks_needed)
                targets[dxl_id] = pos
                self.packetHandler.write4ByteTxRx(
                    self.portHandler, dxl_id, ADDR_GOAL_POSITION, pos & 0xFFFFFFFF)
            self._wait_arrival(targets)

    def _wait_arrival(self, targets):
        t0 = time.time()
        last = {d: self.get_pos(d) for d in DXL_IDS}
        stall = {d: 0 for d in DXL_IDS}
        while time.time() - t0 < 60:
            time.sleep(0.5)
            done = True
            for dxl_id in DXL_IDS:
                pos = self.get_pos(dxl_id)
                remain = abs(targets[dxl_id] - pos)
                if remain > 20:
                    done = False
                stall[dxl_id] = stall[dxl_id] + 1 if abs(pos - last[dxl_id]) < 2 else 0
                last[dxl_id] = pos
            if done or all(s > 6 for s in stall.values()):
                break
        self.get_logger().info('이동 완료')

    def destroy_node(self):
        for dxl_id in DXL_IDS:
            self.packetHandler.write1ByteTxRx(self.portHandler, dxl_id, ADDR_TORQUE_ENABLE, 0)
        self.portHandler.closePort()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = BeltControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
