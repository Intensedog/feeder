import RPi.GPIO as GPIO
import time

# Set the GPIO pin connected to the servo
servo_pin = 18

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(servo_pin, GPIO.OUT)

# Set up PWM on the servo pin at 50Hz
servo = GPIO.PWM(servo_pin, 50)  # 50Hz frequency for standard servos
servo.start(0)  # Initialize PWM with 0% duty cycle (servo at neutral position)

def set_servo_angle(angle):
    # Function to set the servo angle (between 0 and 180 degrees)
    duty_cycle = 2 + (angle / 18)  # Convert angle to duty cycle (range 2 to 12)
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Allow time for the servo to reach the position

try:
    print("Setting servo to 0 degrees")
    set_servo_angle(0)  # Set to 0 degrees
    time.sleep(1)

    print("Setting servo to 90 degrees")
    set_servo_angle(90)  # Set to 90 degrees
    time.sleep(1)

    print("Setting servo to 180 degrees")
    set_servo_angle(180)  # Set to 180 degrees
    time.sleep(1)

    print("Returning servo to 0 degrees")
    set_servo_angle(0)  # Return to 0 degrees

finally:
    # Stop and clean up
    print("Stopping and cleaning up GPIO")
    servo.stop()
    GPIO.cleanup()
