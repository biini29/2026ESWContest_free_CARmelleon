
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from std_msgs.msg import String, Float32
import RPi.GPIO as GPIO
import time
import threading
import json
import os
from RPLCD.i2c import CharLCD


PROFILE_PATH = os.path.expanduser('~/ros2_ws/src/smart_seat/profiles.json')


class SmartSeatController(Node):
    def __init__(self):
        super().__init__('keypad_node')
        self.get_logger().info('keypad_node 시작됨 (복구본)')

        self.profiles = self.load_profiles()

        try:
            self.lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2, auto_linebreaks=False)
            self.lcd.clear()
            self.lcd.write_string("Family Seat\nReady...")
            self.get_logger().info('LCD Initialized Successfully (0x27)')
        except Exception as e:
            self.get_logger().error(f'LCD Init Failed: {e}')
            self.lcd = None

        self.pub = self.create_publisher(Point, '/body_data', 10)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.ROW_PINS = [5, 6, 13, 19]
        self.COL_PINS = [26, 12, 16, 20]
        self.KEY_MAP = [
            ['C', '.', '7', '3'],
            ['D', 'E', '8', '4'],
            ['B', '0', '6', '2'],
            ['A', '9', '5', '1'],
        ]
        for pin in self.ROW_PINS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        for pin in self.COL_PINS:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.guest_mode_active = False
        self.input_buffer = ""
        self.last_key = None
        self.d_press_time = None
        self.d_long_fired = False
        self.LONGPRESS_SEC = 3.0

        # 초음파 센서 (HC-SR04) — 아두이노 경유로 이설
        #   HC-SR04 ECHO(5V)를 3.3V인 라즈베리파이 GPIO에 직결하면 위험하므로,
        #   5V 로직인 아두이노가 직접 측정하고 그 값을 시리얼→arduino_bridge_node
        #   →/ultrasonic_distance 토픽으로 받는다. (레벨시프트 회로 불필요)
        self.measure_req_pub = self.create_publisher(String, '/measure_request', 10)
        self.create_subscription(Float32, '/ultrasonic_distance',
                                 self._on_ultrasonic, 10)
        self._latest_distance_mm = None
        self._distance_event = threading.Event()

        self.SENSOR_HEIGHT_ABOVE_CUSHION_MM = 570.0
        self.SIT_A, self.SIT_B, self.SIT_C = 4.2999, 0.2129, 171.2187
        self.GUEST_WEIGHT_KG = 65.0

        # 키패드 디바운스 / 유령신호 방지
        self._debounce_candidate = None
        self._debounce_count = 0
        self.DEBOUNCE_THRESHOLD = 2

        # 부팅 워밍업 (전원 노이즈로 인한 유령 D 입력 방지)
        self.BOOT_WARMUP_SEC = 1.5
        self.boot_time = time.time()

        self.timer = self.create_timer(0.05, self.scan_keypad)

        # 시작 시 자동 리셋 (벨트처럼 부팅할 때 한 번 확실히 정렬)
        threading.Timer(self.BOOT_WARMUP_SEC + 0.5, self.send_reset).start()

    def load_profiles(self):
        try:
            with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.get_logger().info(f'프로필 로드 성공: {list(data.keys())}')
            return data
        except Exception as e:
            self.get_logger().error(f'프로필 로드 실패, 기본값 사용: {e}')
            return {
                "A": {"name": "PAPA", "height": 178, "pregnant": False},
                "B": {"name": "MAMA", "height": 162, "pregnant": True},
                "C": {"name": "DAUGHTER", "height": 130, "pregnant": False},
            }

    def scan_keypad(self):
        # 부팅 직후 노이즈 구간 무시
        if time.time() - self.boot_time < self.BOOT_WARMUP_SEC:
            return

        pressed_keys = []
        for r_idx, r_pin in enumerate(self.ROW_PINS):
            GPIO.output(r_pin, GPIO.HIGH)
            for c_idx, c_pin in enumerate(self.COL_PINS):
                if GPIO.input(c_pin) == GPIO.HIGH:
                    pressed_keys.append(self.KEY_MAP[r_idx][c_idx])
            GPIO.output(r_pin, GPIO.LOW)

        if len(pressed_keys) > 1:
            # 여러 키 동시 감지 = 접점 불량 유령 신호로 판단, 무시
            self._debounce_candidate = None
            self._debounce_count = 0
            return

        pressed_key = pressed_keys[0] if pressed_keys else None

        if pressed_key == self._debounce_candidate:
            self._debounce_count += 1
        else:
            self._debounce_candidate = pressed_key
            self._debounce_count = 1

        if self._debounce_count < self.DEBOUNCE_THRESHOLD:
            return
        key = self._debounce_candidate

        if True:  # D 롱프레스/짧은클릭은 게스트모드 여부와 무관하게 항상 동작
            if key == 'D':
                if self.last_key != 'D':
                    self.d_press_time = time.time()
                    self.d_long_fired = False
                    self.get_logger().info('D 버튼 눌림 → 롱프레스 타이머 시작')
                elif not self.d_long_fired and self.d_press_time is not None and (time.time() - self.d_press_time) >= self.LONGPRESS_SEC:
                    self.d_long_fired = True
                    self.get_logger().info('D 3초 이상 입력 → 초음파 자동 측정 시작')
                    self.measure_height_ultrasonic()
                self.last_key = key
                self.d_last_seen_time = time.time()
                return
            elif self.last_key == 'D' and key != 'D':
                if self.d_press_time is not None and (time.time() - getattr(self, 'd_last_seen_time', 0)) < 0.3:
                    if not self.d_long_fired and (time.time() - self.d_press_time) >= self.LONGPRESS_SEC:
                        self.d_long_fired = True
                        self.measure_height_ultrasonic()
                    return
                if not self.d_long_fired:
                    self.process_key('D')
                self.d_press_time = None
                self.last_key = key
                return

        if key != self.last_key:
            self.last_key = key
            if key is not None:
                self.process_key(key)

    def process_key(self, key):
        self.get_logger().info(f'Key Pressed: {key}')

        if not self.guest_mode_active:
            if key in self.profiles:
                p = self.profiles[key]
                name = p['name']
                height = float(p['height'])
                pregnant = p.get('pregnant', False)
                tag = ' (Preg)' if pregnant else ''
                self.update_lcd(f"Mode: {name}{tag}", f"Target: {height:.0f}cm")
                self.send_height(height, pregnant)
            elif key == 'D':
                self.guest_mode_active = True
                self.input_buffer = ""
                self.update_lcd("Guest Mode", "Enter H: _")
            elif key == '.':
                self.update_lcd("Resetting...", "Please wait")
                self.send_reset()
        else:
            if key == 'E':
                if self.input_buffer:
                    try:
                        input_height = float(self.input_buffer)
                        if 130.0 <= input_height <= 185.0:
                            self.update_lcd("Setting Seat..", f"Height: {self.input_buffer}cm")
                            self.send_height(input_height, False)
                            time.sleep(4.0)
                            self.guest_mode_active = False
                            self.input_buffer = ""
                            self.update_lcd("Family Seat", "Ready...")
                        else:
                            self.get_logger().warn(f"Invalid range: {input_height}")
                            self.update_lcd("Error: Bad Range", "Limit: 130 - 185")
                            time.sleep(2.0)
                            self.input_buffer = ""
                            self.update_lcd("Guest Mode", "Enter H: _")
                    except ValueError:
                        self.update_lcd("Error: Invalid Num", "Try Again!")
                        time.sleep(2.0)
                        self.input_buffer = ""
                        self.update_lcd("Guest Mode", "Enter H: _")
            elif key == 'D':
                self.guest_mode_active = False
                self.input_buffer = ""
                self.update_lcd("Family Seat", "Ready...")
            elif key in self.profiles:
                # 게스트 모드 중 프로필 키가 눌리면 노이즈로 잘못 진입한 것으로 판단하여 자동 복구
                self.get_logger().warn('게스트 모드 중 프로필 키 감지 -> 게스트 모드 취소 후 적용')
                self.guest_mode_active = False
                self.input_buffer = ""
                p = self.profiles[key]
                name = p['name']
                height = float(p['height'])
                pregnant = p.get('pregnant', False)
                tag = ' (Preg)' if pregnant else ''
                self.update_lcd(f"Mode: {name}{tag}", f"Target: {height:.0f}cm")
                self.send_height(height, pregnant)
            elif key == '.':
                if not self.input_buffer:
                    # 입력 버퍼가 비어있으면 리셋 겸 게스트 모드 탈출
                    self.get_logger().info('게스트 모드 중 리셋 입력 -> 게스트 모드 탈출 및 리셋')
                    self.guest_mode_active = False
                    self.update_lcd("Resetting...", "Please wait")
                    self.send_reset()
                elif '.' not in self.input_buffer:
                    self.input_buffer += '.'
                    self.update_lcd("Guest Mode", f"Enter H: {self.input_buffer}")
            elif key in '0123456789':
                if len(self.input_buffer) < 6:
                    self.input_buffer += key
                    self.update_lcd("Guest Mode", f"Enter H: {self.input_buffer}")

    def measure_height_ultrasonic(self):
        self.guest_mode_active = False
        self.input_buffer = ""
        self.update_lcd("Measuring...", "Please sit")
        time.sleep(1.0)

        distance_mm = self._read_ultrasonic_distance_mm()
        if distance_mm is None:
            self.get_logger().error('초음파 측정 실패 (ECHO 타임아웃)')
            self.update_lcd("Sensor Error", "Try Again (D)")
            return

        model_sitting_height = self.SENSOR_HEIGHT_ABOVE_CUSHION_MM - distance_mm
        real_sitting_height = model_sitting_height * 2.0

        self.get_logger().info(
            f'초음파거리={distance_mm:.1f}mm 축소모델앉은키={model_sitting_height:.1f}mm '
            f'실제앉은키={real_sitting_height:.1f}mm')

        if model_sitting_height <= 0:
            self.update_lcd("Sensor Error", "Check Position")
            return

        estimated_height = (real_sitting_height - self.SIT_B * self.GUEST_WEIGHT_KG - self.SIT_C) / self.SIT_A
        self.get_logger().info(f'추정 키: {estimated_height:.1f} cm')

        self.update_lcd("Maybe your height", f"{estimated_height:.1f} cm")
        time.sleep(2.5)

        if 130.0 <= estimated_height <= 185.0:
            self.update_lcd("Setting Seat..", f"Height: {estimated_height:.1f}cm")
            self.send_height(estimated_height, False)
            time.sleep(2.5)
            self.guest_mode_active = False
            self.input_buffer = ""
            self.update_lcd("Family Seat", "Ready...")
        else:
            self.update_lcd("Applicable Range", "130 ~ 185 cm")
            time.sleep(2.5)
            self.update_lcd("Guest Mode", "Enter H: _")

    def _on_ultrasonic(self, msg):
        # arduino_bridge_node가 아두이노 "DIST,x" 응답을 받아 발행한 거리(mm)
        self._latest_distance_mm = msg.data
        self._distance_event.set()

    def _read_ultrasonic_distance_mm(self):
        # 아두이노에 거리 측정을 요청하고(/measure_request "U"),
        # /ultrasonic_distance 응답을 최대 1초 대기해서 받는다.
        self._distance_event.clear()
        self._latest_distance_mm = None
        self.measure_req_pub.publish(String(data='U'))

        if not self._distance_event.wait(timeout=1.0):
            return None                      # 응답 타임아웃
        d = self._latest_distance_mm
        if d is None or d < 0:
            return None                      # 아두이노 측정 실패(DIST,-1)
        return float(d)

    def update_lcd(self, line1, line2):
        if self.lcd:
            try:
                self.lcd.clear()
                time.sleep(0.02)
                self.lcd.cursor_pos = (0, 0)
                self.lcd.write_string(f"{line1[:16]:<16}")
                time.sleep(0.02)
                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(f"{line2[:16]:<16}")
                time.sleep(0.02)
            except Exception as e:
                self.get_logger().error(f"LCD Error: {e}")

    def send_height(self, height, pregnant=False):
        msg = Point()
        msg.x = float(height)
        msg.y = 65.0
        msg.z = 1.0 if pregnant else 0.0
        self.pub.publish(msg)
        self.get_logger().info(f'/body_data 발행: 키 {height}cm, 임산부={pregnant}')

    def send_reset(self):
        msg = Point()
        msg.x = 0.0
        msg.y = 0.0
        msg.z = 0.0
        self.pub.publish(msg)
        self.get_logger().info('/body_data 발행: 리셋 (x=0)')

    def destroy_node(self):
        if self.lcd:
            self.lcd.clear()
        GPIO.cleanup()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SmartSeatController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
