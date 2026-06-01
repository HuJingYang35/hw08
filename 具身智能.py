import pybullet as p
import pybullet_data
import time

physics_client = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

plane_id = p.loadURDF("plane.urdf")
robot_id = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)

p.resetDebugVisualizerCamera(1.5, 45, -30, [0, 0, 0.5])
target_pos = [0.5, 0.2, 0.3]
end_effector_link = 11

joint_positions = p.calculateInverseKinematics(robot_id, end_effector_link, target_pos, 100, 0.001)

print("机械臂开始移动...")
for _ in range(240):
    for joint_idx in range(7):
        p.setJointMotorControl2(
            robot_id, joint_idx, p.POSITION_CONTROL,
            targetPosition=joint_positions[joint_idx], force=500
        )
    p.stepSimulation()
    time.sleep(1/240)

print("到达目标位置！仿真结束")
p.disconnect()



import pybullet as p
import pybullet_data
import time

physics_client = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

plane_id = p.loadURDF("plane.urdf")
robot_id = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)

cube_pos = [0.5, 0, 0.05]
cube_ori = p.getQuaternionFromEuler([0,0,0])
cube_id = p.loadURDF("cube.urdf", cube_pos, cube_ori, globalScaling=0.05)

p.resetDebugVisualizerCamera(1.8, 45, -30, [0,0,0.5])
end_effector_link = 11
arm_joints = [0,1,2,3,4,5,6]
gripper_joints = [9, 10]

def move_to(robot_id, target_pos, steps=240):
    joint_positions = p.calculateInverseKinematics(robot_id, end_effector_link, target_pos, 100, 0.001)
    for _ in range(steps):
        for j, idx in enumerate(arm_joints):
            p.setJointMotorControl2(robot_id, idx, p.POSITION_CONTROL, targetPosition=joint_positions[j], force=500)
        p.stepSimulation()
        time.sleep(1/240)

def control_gripper(robot_id, open=True):
    target = 0.04 if open else 0.0
    for idx in gripper_joints:
        p.setJointMotorControl2(robot_id, idx, p.POSITION_CONTROL, targetPosition=target, force=100)
    for _ in range(50):
        p.stepSimulation()
        time.sleep(1/240)

print("开始抓取...")
control_gripper(robot_id, open=True)
move_to(robot_id, [0.5, 0, 0.15])
move_to(robot_id, [0.5, 0, 0.07], 120)
control_gripper(robot_id, open=False)
move_to(robot_id, [0.5, 0, 0.3], 120)
move_to(robot_id, [0.3, -0.3, 0.3])
move_to(robot_id, [0.3, -0.3, 0.07], 120)
control_gripper(robot_id, open=True)
move_to(robot_id, [0.3, -0.3, 0.3], 120)

print("抓取流程完成！")
time.sleep(2)
p.disconnect()