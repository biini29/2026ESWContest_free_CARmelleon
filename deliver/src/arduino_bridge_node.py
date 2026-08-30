
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy
from rclpy.node import Node
import serial

from std_msgs.msg import String, Float32   # 모터 명령(문자열)·초음파 거리(실수)


SERIAL_PORT = '/dev/arduino_linear'
BAUD_RATE = 115200


class ArduinoBridgeNode(Node):
    def __init__(self):
        super().__init__('arduino_bridge_node')

        # 아두이노 시리얼 연결
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            self.get_logger().info(f'아두이노 연결 성공: {SERIAL_PORT} @ {BAUD_RATE}')
        except serial.SerialException as e:
            self.get_logger().error(f'아두이노 연결 실패: {e}')
            self.ser = None
            return

        # ★ 구독: /motor_cmd 로 오는 모터 명령을 아두이노로 전달 ★
        self.cmd_sub = self.create_subscription(
            String, '/motor_cmd', self.on_motor_cmd, 10)

        # ★ 구독: /measure_request → 아두이노에 초음파 측정 요청("U") 전달 ★
        self.meas_sub = self.create_subscription(
            String, '/measure_request', self.on_measure_request, 10)

        # ★ 발행: 아두이노가 회신한 거리(mm)를 /ultrasonic_distance 로 전달 ★
        self.dist_pub = self.create_publisher(Float32, '/ultrasonic_distance', 10)

        # 타이머: 아두이노에서 오는 데이터 읽기
        self.read_timer = self.create_timer(0.05, self.read_from_arduino)

        self.get_logger().info('arduino_bridge_node 시작됨. (/motor_cmd·/measure_request 구독 중)')

    # 아두이노 → 라즈베리파이: 읽기
    def read_from_arduino(self):
        if self.ser is None:
            return
        try:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith('DIST,'):
                    # 아두이노 초음파 응답 → /ultrasonic_distance 발행
                    try:
                        mm = float(line.split(',', 1)[1])
                    except (ValueError, IndexError):
                        mm = -1.0
                    self.dist_pub.publish(Float32(data=mm))
                # "OK M..." / "READY" 등 다른 응답은 로깅만(무시 가능)
        except Exception as e:
            self.get_logger().warn(f'시리얼 읽기 오류: {e}')

    # ★ /motor_cmd 콜백: 받은 명령을 아두이노로 전송 ★
    def on_motor_cmd(self, msg):
        self.send_command(msg.data)
        self.get_logger().info(f'모터 명령 전송: {msg.data}')

    # ★ /measure_request 콜백: 아두이노에 거리 측정 요청("U") 전송 ★
    def on_measure_request(self, msg):
        self.send_command('U')
        self.get_logger().info('초음파 측정 요청 전송: U')

    # 라즈베리파이 → 아두이노: 명령 보내기
    def send_command(self, command):
        if self.ser is None:
            return
        self.ser.write((command + '\n').encode('utf-8'))


def main(args=None):
    rclpy.init(args=args)
    node = ArduinoBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.ser is not None:
            node.ser.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
