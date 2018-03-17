import hou

# our cam object
cam = hou.pwd()
# get 4x4 matrix representing  transformation of our camera
cam_xform = cam.worldTransform()
# get position of our camera
cam_pos = hou.Vector4(0, 0, 0, 1) * cam_xform
cam_pos = hou.Vector3(cam_pos)

# view axis of our camera
view_axis = hou.Vector4(0, 0, -1, 0) * cam_xform

# get target path
target_path = cam.evalParm("target")
# get target object
target_node = hou.node(target_path)
# get target's transformation
target_xform = target_node.worldTransform()
# get target's position
target_pos = hou.Vector4(0, 0, 0, 1) * target_xform

# cast from Vector4 to Vector3
view_axis = hou.Vector3(view_axis)
target_pos = hou.Vector3(target_pos)

# normalize our view axis
view_axis = view_axis.normalized()

# get a vector pointing from camera to target
cam_target = hou.Vector3( target_pos - cam_pos )

# project cam_target vector on view_axis, because view_axis is normalized, this results in length of our projected vector, what represents focus distance in our case
focus_dist = cam_target.dot(view_axis)

return focus_dist