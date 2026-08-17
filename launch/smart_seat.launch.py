
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable


def generate_launch_description():
    return LaunchDescription([
        SetEnvironmentVariable('RCUTILS_COLORIZED_OUTPUT', '1'),
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
