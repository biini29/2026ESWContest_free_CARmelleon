
cmake_minimum_required(VERSION 3.8)
project(smart_seat)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/TargetSeatProfile.msg"
  DEPENDENCIES std_msgs
)

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
  msg
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
