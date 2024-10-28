import RPi.GPIO as GPIO
import time

# Setup
motor_pin = 20  # Set the motor pin to GPIO 20

GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(motor_pin, GPIO.OUT)  # Set GPIO 27 as an output

try:
    # Start motor
    print("Motor running...")
    GPIO.output(motor_pin, GPIO.HIGH)
    time.sleep(5)  # Run the motor for 5 seconds

    # Stop motor
    print("Motor stopping...")
    GPIO.output(motor_pin, GPIO.LOW)

except KeyboardInterrupt:
    # Graceful exit on Ctrl+C
    pass
finally:
    # Cleanup
    GPIO.cleanup()
    print("GPIO cleaned up.")
