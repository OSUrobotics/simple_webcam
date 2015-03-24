cmake_minimum_required(VERSION 2.8.3)
project(simple_webcam)

find_package(catkin REQUIRED COMPONENTS cv_bridge sensor_msgs camera_info_manager_py rospy)

catkin_package(
    CATKIN_DEPENDS cv_bridge sensor_msgs camera_info_manager_py rospy
)

catkin_python_setup()

install(PROGRAMS
    nodes/camera.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

install(DIRECTORY launch
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

include_directories( ${Boost_INCLUDE_DIR} ${catkin_INCLUDE_DIRS})