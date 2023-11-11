from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

# Define servo channels
servo_channel_1 = 0 #BASE can rotate the arm side to side
servo_channel_2 = 1  # WAIST can rotate the arm up and down
servo_channel_3 = 2  # ARM has the tip at the front and can move up and down


kit.servo[servo_channel_1].set_pulse_width_range(750, 2750)
kit.servo[servo_channel_2].set_pulse_width_range(750, 2750)
kit.servo[servo_channel_3].set_pulse_width_range(750, 2800)



def move_servo(servo, target_angle, delay):
    current_angle = int(servo.angle) if servo.angle is not None else 0  
    target_angle = int(target_angle)  
    step = 1 if target_angle > current_angle else -1
    for angle in range(current_angle, target_angle, step):
        servo.angle = angle
        time.sleep(delay)

# Set the target angles and delay
target_angle_0 = 90  # BASE
target_angle_1 = 75 # WAIST
target_angle_2 = 13  # ARM
delay_between_steps = 0.005 

move_servo(kit.servo[servo_channel_1], target_angle_0, delay_between_steps)
move_servo(kit.servo[servo_channel_2], target_angle_1, delay_between_steps)
move_servo(kit.servo[servo_channel_3], target_angle_2, delay_between_steps)
