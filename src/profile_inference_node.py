
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from smart_seat.msg import TargetSeatProfile
import math


NUM_MOTORS = 5
MOTOR_HEIGHTS = [150.0, 320.0, 490.0, 660.0, 830.0]
MAX_STROKE_MM = 100.0

SIT_A, SIT_B, SIT_C = 4.2999, 0.2129, 171.2187

# 일반 허리(요추) 곡선
LUMBAR_RATIO = 0.18
LUMBAR_MAX_PUSH = 95.0
LUMBAR_WIDTH = 200.0

# 임산부 모드 허리 (부드럽게 + 정점 낮춤)
PREG_LUMBAR_RATIO = 0.12
PREG_LUMBAR_MAX_PUSH = 55.0
PREG_LUMBAR_WIDTH = 250.0

# 머리 지지
HEAD_CG_OFFSET = 90.0
HEAD_MAX_PUSH = 40.0
HEAD_WIDTH = 150.0

SCALE = 0.5

# 벨트 관련 상수
BELT_HOME_ABOVE_CUSHION = -45.0
BELT_TICKS_PER_MM = 37.3
BELT_SHOULDER_RATIO = 0.80
BELT_PREGNANT_TARGET_REAL = 125.0
BELT_CALIBRATION_OFFSET_MM = 25.0   # 실측 기반 보정값


class ProfileInferenceNode(Node):
    def __init__(self):
        super().__init__('profile_inference_node')
        self.pub = self.create_publisher(
            TargetSeatProfile, '/target_seat_profile', 10)
        self.sub = self.create_subscription(
            Point, '/body_data', self.callback, 10)
        self.get_logger().info(
            f'profile_inference_node 시작됨 (천+솜 곡선+임산부모드+벨트, 스케일 {SCALE})')

    def callback(self, msg):
        height = msg.x
        weight = msg.y
        is_pregnant = (msg.z == 1.0)

        if height <= 0:
            self.get_logger().info('=== 리셋 명령 수신 → 초기화 신호 발행 ===')
            profile = TargetSeatProfile()
            profile.belt_height_cm = -1.0
            profile.actuator_mm = [-1.0] * NUM_MOTORS
            self.pub.publish(profile)
            return

        mode = '임산부' if is_pregnant else '일반'
        self.get_logger().info(f'입력 -> 키: {height:.1f}cm, 몸무게: {weight:.1f}kg, 모드: {mode}')

        sitting_height = SIT_A * height + SIT_B * weight + SIT_C

        # 허리 곡선 파라미터 선택
        if is_pregnant:
            lumbar_ratio = PREG_LUMBAR_RATIO
            lumbar_max = PREG_LUMBAR_MAX_PUSH
            lumbar_width = PREG_LUMBAR_WIDTH
        else:
            lumbar_ratio = LUMBAR_RATIO
            lumbar_max = LUMBAR_MAX_PUSH
            lumbar_width = LUMBAR_WIDTH

        lumbar_apex = sitting_height * lumbar_ratio
        head_support = sitting_height - HEAD_CG_OFFSET

        self.get_logger().info(
            f'  앉은키: {sitting_height:.0f}mm, 요추정점: {lumbar_apex:.0f}mm '
            f'(밀기최대 {lumbar_max:.0f}mm)')

        pushes = []
        for i in range(NUM_MOTORS):
            motor_h = MOTOR_HEIGHTS[i]

            d_lumbar = motor_h - lumbar_apex
            push_lumbar = lumbar_max * math.exp(-((d_lumbar / lumbar_width) ** 2))

            if head_support <= MOTOR_HEIGHTS[-1] + HEAD_WIDTH:
                d_head = motor_h - head_support
                push_head = HEAD_MAX_PUSH * math.exp(-((d_head / HEAD_WIDTH) ** 2))
            else:
                push_head = 0.0

            push = max(push_lumbar, push_head)
            pushes.append(min(push, MAX_STROKE_MM))

        scaled = [p * SCALE for p in pushes]

        # 벨트 목표 계산
        if is_pregnant:
            belt_target_real = BELT_PREGNANT_TARGET_REAL
        else:
            belt_target_real = sitting_height * BELT_SHOULDER_RATIO

        belt_target_model = belt_target_real * SCALE
        belt_target_model += BELT_CALIBRATION_OFFSET_MM  # 실측 보정 적용

        belt_ticks_needed = (belt_target_model - BELT_HOME_ABOVE_CUSHION) * BELT_TICKS_PER_MM

        self.get_logger().info(
            f'  벨트 목표(방석위,모형,보정후): {belt_target_model:.0f}mm -> 필요틱수: {belt_ticks_needed:.0f}')

        profile = TargetSeatProfile()
        profile.belt_height_cm = belt_ticks_needed  # 필드명은 그대로, 실제로는 '필요 틱수'
        profile.actuator_mm = scaled
        self.pub.publish(profile)

        detail = [f'M{i+1}:{pushes[i]:.0f}->{scaled[i]:.0f}' for i in range(NUM_MOTORS)]
        self.get_logger().info('  밀기(실물->모형): ' + ', '.join(detail))


def main(args=None):
    rclpy.init(args=args)
    node = ProfileInferenceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
