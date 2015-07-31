#!/usr/bin/env python
import roslib; roslib.load_manifest('simple_webcam')
import rospy, cv2, cv_bridge
from sensor_msgs.msg import Image, CameraInfo
from camera_info_manager import CameraInfoManager

_bridge = cv_bridge.CvBridge()
_manager = None
if __name__ == '__main__':
	rospy.init_node('camera')
	cap = cv2.VideoCapture()
	cap.open(rospy.get_param('~camera_id', 0))

	manager = CameraInfoManager(rospy.get_name().strip('/'), url=rospy.get_param('~info_url', ''))
	manager.loadCameraInfo()

	image_pub = rospy.Publisher('~image_raw', Image, queue_size=1)
	info_pub  = rospy.Publisher('~camera_info', CameraInfo, queue_size=1)

	rate = rospy.Rate(rospy.get_param('~publish_rate', 15))
	header = rospy.Header()
	header.frame_id = rospy.get_name() + '_rgb_optical_frame'
	while not rospy.is_shutdown():
		cap.grab()
		frame = cap.retrieve()
		header.stamp = rospy.Time.now()
		if frame[0]:
			msg = _bridge.cv2_to_imgmsg(frame[1], "bgr8")
			msg.header = header

			if manager.isCalibrated():
				info = manager.getCameraInfo()
				info.header = header
				info_pub.publish(info)

			image_pub.publish(msg)

		rate.sleep()
	cap.release()
