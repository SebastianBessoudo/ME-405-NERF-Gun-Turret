"""! @file motor_driver.py
This is the file that main.py imports the motor driver from. This files establishes the
MotorDriver class to be used. 
@author Nathaniel Davis
@author Sebastian Bessoudo
@date 02-05-2024
"""

import pyb
import time

class MotorDriver:
    """!
    This class implements a motor driver for an ME405 kit.
    """

    def __init__(self, en_pin, in1pin, pin1ch, in2pin, pin2ch, timer):
        """!
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety.
        @param en_pin 
        @param in1pin Pin for use in positive direction
        @param pin1ch Channel for pin 1
        @param in2pin Pin for use in negative direction
        @param pin2ch Channel for pin 2
        @param timer Timer channel used
        """
        self.pinENA = pyb.Pin(en_pin, pyb.Pin.OUT_PP)
        self.pinIN1 = pyb.Pin(in1pin, pyb.Pin.OUT_PP)
        self.pinIN2 = pyb.Pin(in2pin, pyb.Pin.OUT_PP)
        tim = pyb.Timer(timer, freq=20000)
        self.chIN1 = tim.channel(pin1ch, pyb.Timer.PWM, pin=self.pinIN1)
        self.chIN2 = tim.channel(pin2ch, pyb.Timer.PWM, pin=self.pinIN2)
        self.pinENA.low()
        
        print("Creating a Motor Driver")
        self.PWM = 0
    def set_duty_cycle(self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor
        """
#         print(f"Setting duty cycle to {level}")
        self.PWM = level
        if self.PWM > 0:
#             print("Forward Motion")
            self.pinENA.high()
            self.chIN1.pulse_width_percent(self.PWM)
            self.chIN2.pulse_width_percent(0)
        elif self.PWM == 0:
#             print("Stopping Motion")
            self.pinENA.low()
        elif self.PWM < 0:
#             print("Backward Motion")
            self.pinENA.high()
            self.chIN2.pulse_width_percent(abs(self.PWM))
            self.chIN1.pulse_width_percent(0)
    def print(self):
        print(self.PWM)
if __name__ == "__main__":
    moe = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, 1,  pyb.Pin.board.PB5, 2, 3)
    moe.set_duty_cycle(50)