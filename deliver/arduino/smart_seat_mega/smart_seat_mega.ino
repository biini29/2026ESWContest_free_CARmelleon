/*
 * Smart Seat - Arduino Mega 2560
 * 역할: 라즈베리파이(ROS 2)의 명령을 받아
 *       (1) 리니어 액추에이터 5개(L298N x3) 구동
 *       (2) HC-SR04 초음파 센서로 거리 측정 후 회신
 *
 * 통신: USB Serial 115200bps
 *   - 모터 명령 : "M,<번호>,<방향>,<속도>"   예) M,1,1,200
 *       방향 1=전진(늘림) / -1=후진(줄임) / 0=정지,  속도 0~255
 *       응답 : "OK M1 dir=1 spd=200"
 *   - 거리 요청 : "U"
 *       응답 : "DIST,<거리_mm>"   (측정 실패 시 "DIST,-1")
 *
 * 초음파 이설 배경:
 *   HC-SR04 ECHO는 5V 출력이라 3.3V인 라즈베리파이 GPIO에 직결하면 위험하다.
 *   5V 로직인 아두이노에서 직접 읽으면 레벨시프트(저항분배) 회로가 불필요하고
 *   펄스 타이밍도 안정적으로 처리된다.
 *   ※ TRIG/ECHO 핀 번호는 배선에 맞춰 자유롭게 변경 가능(아래 상수만 수정).
 */

// ── 리니어 액추에이터 (L298N x3) ──
const int NUM_MOTORS = 5;
const int MOTOR_EN[NUM_MOTORS] = { 2, 3, 4, 5, 6 };      // EN(PWM)
const int MOTOR_IN[NUM_MOTORS][2] = {
  {22, 23},   // 모터1 (L298N#1 A)
  {24, 25},   // 모터2 (L298N#1 B)
  {26, 27},   // 모터3 (L298N#2 A)
  {28, 29},   // 모터4 (L298N#2 B)
  {30, 31},   // 모터5 (L298N#3 A)
};

// ── HC-SR04 초음파 센서 (아두이노 5V 로직에서 직접 읽음) ──
// 리니어용 D2~D6, D22~D31 과 겹치지 않는 여유 핀 사용. 배선에 맞게 변경 가능.
const int TRIG_PIN = 32;
const int ECHO_PIN = 33;
const unsigned long ECHO_TIMEOUT_US = 30000UL;  // 약 5m 왕복 타임아웃

void setup() {
  Serial.begin(115200);

  for (int i = 0; i < NUM_MOTORS; i++) {
    pinMode(MOTOR_EN[i], OUTPUT);
    pinMode(MOTOR_IN[i][0], OUTPUT);
    pinMode(MOTOR_IN[i][1], OUTPUT);
    stopMotor(i);   // 시작 시 전부 정지 (안전)
  }

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  digitalWrite(TRIG_PIN, LOW);

  Serial.println("READY");
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    handleCommand(cmd);
  }
}

void handleCommand(String cmd) {
  if (cmd.length() == 0) return;

  char type = cmd.charAt(0);

  // ── 거리 요청: "U" ──
  if (type == 'U') {
    long mm = readUltrasonicMM();
    Serial.print("DIST,");
    Serial.println(mm);   // 실패 시 -1
    return;
  }

  // ── 모터 명령: "M,번호,방향,속도" ──
  if (type == 'M') {
    int c1 = cmd.indexOf(',');
    int c2 = cmd.indexOf(',', c1 + 1);
    int c3 = cmd.indexOf(',', c2 + 1);
    if (c1 < 0 || c2 < 0 || c3 < 0) return;

    int motorNum = cmd.substring(c1 + 1, c2).toInt();  // 1~5
    int dir      = cmd.substring(c2 + 1, c3).toInt();  // 1/0/-1
    int speed    = cmd.substring(c3 + 1).toInt();      // 0~255

    int idx = motorNum - 1;
    if (idx < 0 || idx >= NUM_MOTORS) return;

    driveMotor(idx, dir, speed);

    Serial.print("OK M"); Serial.print(motorNum);
    Serial.print(" dir="); Serial.print(dir);
    Serial.print(" spd="); Serial.println(speed);
  }
}

// HC-SR04 왕복 시간 → 거리(mm). 실패 시 -1 반환.
long readUltrasonicMM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  unsigned long duration = pulseIn(ECHO_PIN, HIGH, ECHO_TIMEOUT_US);
  if (duration == 0) return -1;              // 타임아웃(측정 실패)

  // 음속 343m/s → 편도거리(mm) = duration(us) * 0.343 / 2
  long distance_mm = (long)(duration * 0.343 / 2.0);
  return distance_mm;
}

void driveMotor(int idx, int dir, int speed) {
  speed = constrain(speed, 0, 255);
  if (dir > 0) {          // 전진(늘림)
    digitalWrite(MOTOR_IN[idx][0], HIGH);
    digitalWrite(MOTOR_IN[idx][1], LOW);
    analogWrite(MOTOR_EN[idx], speed);
  } else if (dir < 0) {   // 후진(줄임)
    digitalWrite(MOTOR_IN[idx][0], LOW);
    digitalWrite(MOTOR_IN[idx][1], HIGH);
    analogWrite(MOTOR_EN[idx], speed);
  } else {                // 정지
    stopMotor(idx);
  }
}

void stopMotor(int idx) {
  digitalWrite(MOTOR_IN[idx][0], LOW);
  digitalWrite(MOTOR_IN[idx][1], LOW);
  analogWrite(MOTOR_EN[idx], 0);
}
