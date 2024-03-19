"""! @file closed_loop.py
Defines Servo class.
If this is the main.py file on the Nucleo,
it will run a motor response test.
@author Nathaniel Davis
@author Sebastian Bessoudo
@date 02-13-2024
"""

import micropython
import pyb
import time
import cqueue
from motor_driver_updated import MotorDriver
from encoder_reader_updated import Encoder

# Allow interrupts to display errors
micropython.alloc_emergency_exception_buf(100)

class MotoEncodo:
    """!
    This class uses motor control and encoder reading for the user to input a Kp value
    and its setpoint
    """
    def __init__(self, motor, encoder):
        """!
        Initializes the servo. Also sets up a 
        @param motor 
        @param encoder
        """
        self.motor = motor
        self.encoder = encoder
        self.Kp = 0.1
        self.Ki = 0
        self.error = 0
        self.sum = 0
        
    def run(self, level):
        """!
        sets the duty cycle for the motor to run based on
        @param level
        """
        self.motor.set_duty_cycle(level)
        
    def set_setpoint(self, setpoint):
        """!
        sets the setpoint of the motor
        @setpoint
        """
        self.encoder.read()
        self.error = setpoint - self.encoder.pos
        self.sum += self.error
        self.PWM = (self.Kp*self.error)+(self.Ki*self.sum*0.01)
        self.motor.set_duty_cycle(self.PWM)
        
    def set_Kp(self, Kp):
        """!
        sets the Kp value
        @param Kp Kp value desired
        """
        self.Kp = Kp
        
    def set_Ki(self, Ki):
        """!
        sets the Ki value
        @param Ki Ki value desired
        """
        self.Ki = Ki
    def plot_results():
        position = []
        time = [10*x for x in range(500)]
        for i in range(len(time)):
            positions.append(serv.encoder.read())
            print(time + ', ' + position)
        print('End')

    
if __name__ == "__main__":  
    # run motor response test
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
    input_kp = float(input('Please input a value for Kp: '))
    motorctrl.set_Kp(input_kp)
    input_ki = float(input('Please input a value for Ki: '))
    motorctrl.set_Ki(input_ki)
    input_setp = int(input('Please input a value for the setpoint: '))
    while True:
        time.sleep_ms(10)
        motorctrl.set_setpoint(input_setp)
        print(enc.read())
        
            
    