from flask import Flask, request, render_template, Response
from adafruit_servokit import ServoKit
from picamera import PiCamera
import time

app = Flask(__name__)

# Initialize servo kit and set pulse width ranges
kit = ServoKit(channels=16)
servo_channel_1 = 0  # BASE
servo_channel_2 = 1  # WAIST
servo_channel_3 = 2  # ARM

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move_servo', methods=['POST'])
def move_servo_endpoint():
    data = request.get_json()
    if 'servo' in data and 'angle' in data:
        servo_id = int(data['servo'])
        angle = int(data['angle'])
        if servo_id == 0:  # BASE
            move_servo(kit.servo[servo_channel_1], angle, delay_between_steps)
        elif servo_id == 1:  # WAIST
            move_servo(kit.servo[servo_channel_2], angle, delay_between_steps)
        elif servo_id == 2:  # ARM
            move_servo(kit.servo[servo_channel_3], angle, delay_between_steps)
        return 'OK'
    else:
        return 'Invalid data', 400

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 20
    time.sleep(2)  # Give the camera some time to warm up

    while True:
        frame = bytearray()
        camera.capture(frame, 'jpeg', use_video_port=True)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    delay_between_steps = 0.005
    app.run(host='0.0.0.0', port=80)
