from gpiozero import AngularServo
from time import sleep

# Define the GPIO pin where the servo is connected
servo_pin = 18  # Only one servo on GPIO18

# Create a servo object using the default GPIO pin factory (software PWM)
servo = AngularServo(servo_pin, min_angle=-90, max_angle=90)

def open_servo():
    print("Opening servo...")
    servo.angle = 90  # Move the servo to fully open
    #sleep(1)

def close_servo():
    print("Closing servo...")
    servo.angle = -90  # Move the servo to fully closed
    #sleep(1)

# Example control without a loop
try:
    open_servo()
    sleep(1)  # Keep the servo open for 2 seconds
    close_servo()
    sleep(1)  # Keep the servo closed for 2 seconds
except KeyboardInterrupt:
    print("Program interrupted")
