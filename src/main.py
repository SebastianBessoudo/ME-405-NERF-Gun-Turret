"""! @file main.py
Term Project of Nathaniel Davis and Sebastian Bessoudo.
When the blue button on the Nucleo is pressed, start the firing process
of turning around and firing
@author Nathaniel Davis
@author Sebastian Bessoudo
@date 3-12-24
"""

import pyb
import gc
import pyb
import cotask
import task_share
from motor_driver_updated import MotorDriver
from encoder_reader_updated import Encoder 
from motorwithencoder_updated import MotoEncodo
from servo import Servo
from mlx_cam import MLX_Cam
import math
import time
from machine import Pin, I2C
from mlx90640 import MLX90640
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern


def task1_mm(shares):
    """!
    mastermind of main.py
    """
    S0_INIT = 0
    S1_BUTTON = 1 
    S2_TURN = 2
    S3_CAM = 3
    S4_MOTOR = 4
    S5_FIRE = 5
    S6_RESET = 6

    state = S0_INIT
    
    while True:
        ir_angle, motor_setpoint = shares
        if(state == S0_INIT): # initializes system            
            # set up servo
            servpin = pyb.Pin.board.PB6
            servtimer = 4
            servchannel = 1
            serv = Servo(servpin, servtimer, servchannel)

            
            # set up flywheel output
            flypin = pyb.Pin.board.PC3
            flywheel = pyb.Pin(flypin, pyb.Pin.OUT_PP)
            flywheel.low()
            
            #set up button pin
            buttonpin = pyb.Pin.board.PC13
            button = pyb.Pin(buttonpin, pyb.Pin.IN)
            
            state = S1_BUTTON
            yield
            
        elif(state == S1_BUTTON): # waits for button press
            if button.value():
                state = S2_TURN
            yield
        elif(state == S2_TURN): # turns 180 degrees and waits 6 seconds
            print("turning")
            motor_setpoint.put(1600)
            time.sleep(6)
            
#             for _ in range(600):
#                 time.sleep_us(1000)
#                 yield
            state = S3_CAM
            yield
        elif(state == S3_CAM): # takes the currently stored camera info
            print("checking camera")
            if ir_angle.any():
                angle = ir_angle.get()
                state = S4_MOTOR
                yield
        elif(state == S4_MOTOR): # moves motor
            print("adjusting")
            if ir_angle.any():
                setpoint = motor_setpoint.get()
                setpoint -= angle*16
                motor_setpoint.put(setpoint)
                state = S5_FIRE
            yield
        elif(state == S5_FIRE): # fire away!
            print("firing!")
#             flywheel.high() # start flywheel motors
#             for _ in range(2000):
#                 time.sleep_us(1000)
#             servo.set_angle(142)
#             for _ in range(1000):
#                 time.sleep_us(1000)
#             flywheel.low()
#             servo.set_angle(100)
#             time.sleep_ms(500)
#             servo.off()
            state = S6_RESET
            yield
        elif(state == S6_RESET): # resets system
            motor_setpoint.put(0)
            yield
        
def task2_motorcontrol(shares):
    """!
    motor controller that constantly attempts to
    reach the setpoint set in the intertask variable "motor_setpoint."
    """
    S0_INIT = 0
    S1_UPDATE_MOTOR = 1
     
    state = S0_INIT
    while True:
        ir_angle, motor_setpoint = shares
        if(state == S0_INIT):
            # motor pins
            mtrAplus = pyb.Pin.board.PB4
            Aplusch = 1
            mtrAminus = pyb.Pin.board.PB5
            Aminusch = 2
            mtrEN = pyb.Pin.board.PA10
            mtrtimer = 3

            # encoder pins
            encA = pyb.Pin.board.PC6
            encAch = 1
            encB = pyb.Pin.board.PC7
            encBch = 2
            readch = 8
            
            # set up motor driver
            moe = MotorDriver(mtrEN, mtrAplus, Aplusch,  mtrAminus, Aminusch, mtrtimer)
            # set up encoder
            enc = Encoder(encA, encB, readch, encAch, encBch)
            # set up motor control
            motorctrl = MotoEncodo(moe, enc)
            motorctrl.set_Kp(1)
            
            state = S1_UPDATE_MOTOR
            yield
            
        elif(state == S1_UPDATE_MOTOR):
            if motor_setpoint.any():
                setpoint = motor_setpoint.get()
                motorctrl.set_setpoint(setpoint)
                motor_setpoint.put(setpoint)
                print(f'setpoint: {setpoint}, current location: {enc.read()}')
            yield
        
def task3_camera(shares):
    """!
    constantly updates the intertask variable "ir_angle"
    with an angle of greatest heat signature.
    """
    S0_INIT = 0
    S1_UPDATE_CAMERA = 1
    
    state = S0_INIT
    while True:
        ir_angle, motor_setpoint = shares
        if(state == S0_INIT):
            import gc
            # The following import is only used to check if we have an STM32 board such
            # as a Pyboard or Nucleo; if not, use a different library
            try:
                from pyb import info

            # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
            except ImportError:
                # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
                i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))

            # OK, we do have an STM32, so just use the default pin assignments for I2C1
            else:
                i2c_bus = I2C(1)

            # Select MLX90640 camera I2C address, normally 0x33, and check the bus
            i2c_address = 0x33
            scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]

            # Create the camera object and set it up in default mode
            camera = MLX_Cam(i2c_bus)
            camera._camera.refresh_rate = 1.0
            state = S1_UPDATE_CAMERA
            yield
        elif(state == S1_UPDATE_CAMERA):
            # Get an image and see how long it takes to grab that image
            # Keep trying to get an image; this could be done in a task, with
            # the task yielding repeatedly until an image is available
            image = None
            while not image:
                image = camera.get_image_nonblocking()
                yield
            # Can show image.v_ir, image.alpha, or image.buf; image.v_ir best?
            # Display pixellated grayscale or numbers in CSV format; the CSV
            # could also be written to a file. Spreadsheets, Matlab(tm), or
            # CPython can read CSV and make a decent false-color heat plot.
            csv = []
            for line in camera.get_csv(image, limits=(0, 99)):
                csv.append(sum([eval(i) for i in line.split(',')]))
                yield
            cam_row = csv.index(max(csv))
            angle = cam_row - 12.5
            ir_angle.put(angle) 
            gc.collect()
            yield
            
if __name__ == "__main__":
    
    # create intertask data here
    ir_angle = task_share.Queue('h', 1, thread_protect=True, overwrite=True, name="IR Angle")
    motor_setpoint = task_share.Queue('l', 1, thread_protect=True, overwrite=True, name="Motor Setpoint")
    
    # create tasks
    task1 = cotask.Task(task1_mm, name="Mastermind", priority=2, period=20, profile=True, trace=False, shares=(ir_angle, motor_setpoint))
    task2 = cotask.Task(task2_motorcontrol, name="Motor Control", priority=3, period=10, profile=True, trace=False, shares=(ir_angle, motor_setpoint))
    task3 = cotask.Task(task3_camera, name="Camera", priority=2, period=50,profile=True, trace=False, shares=(ir_angle, motor_setpoint))
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    
    # clean up memory
    gc.collect()
    
    # create scheduler
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break
    
    
    