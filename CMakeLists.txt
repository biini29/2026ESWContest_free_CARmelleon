
cmake_minimum_required(VERSION 3.8)
project(smart_seat)

# 컴파일러 경고 옵션 (기본값)
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 필요한 패키지들 찾기
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# 커스텀 메시지 생성 (우리 .msg 파일 등록)
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/TargetSeatProfile.msg"
  DEPENDENCIES std_msgs geometry_msgs)

# 파이썬 스크립트를 설치 (ros2 run 으로 실행 가능하게)
install(PROGRAMS
  scripts/keypad_node.py
  scripts/profile_inference_node.py
  scripts/seat_controller_node.py
  scripts/sensor_bridge_node.py
  scripts/arduino_bridge_node.py
  scripts/belt_controller_node.py
  DESTINATION lib/${PROJECT_NAME}
)
 install(DIRECTORY
        launch
        DESTINATION share/${PROJECT_NAME}
        )

# launch 폴더를 설치 (ros2 launch 로 찾을 수 있게)
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
