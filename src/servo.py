"""! @file servo.py
Servo controller class. Running as main will make servo rotate at specific speed.
@author Nathaniel Davis
@date 3-13-24
"""

import time
import pyb

class Servo:
    """!
    This class implements a servo controller to move to its designated setpoint and stop
    """
    def __init__(self, servpin, timer, ch):
        """
        Creates the servo controller using PWM
        @param servpin pin that the servo is connected to
        @param timer timer for the servo pin
        @param channel channel for the servo pin
        """
        servo_pin = pyb.Pin(servpin, pyb.Pin.OUT_PP)
        tim = pyb.Timer(timer, freq = 50) # period is 20 ms
        self.servo_channel = tim.channel(ch, pyb.Timer.PWM, pin = servo_pin)
    def cw(self):
        """
        Makes servo turn clockwise
        """
        self.servo_channel.pulse_width_percent(5)
    def ccw(self):
        """
        Makes servo turn counter-clockwise
        """
        self.servo_channel.pulse_width_percent(10)
    def off(self):
        """
        Turns servo off
        """
        self.servo_channel.pulse_width_percent(0)
        
    def stop(self):
        """
        Makes servo stop
        """
        self.servo_channel.pulse_width_percent(7.5)
    
if __name__ == "__main__":
    serv = Servo(pyb.Pin.board.PB6, 4, 1)
    firing = 220
    serv.ccw()
    time.sleep_ms(firing)
    serv.stop()
    time.sleep(0.5)
    serv.cw()
    time.sleep_ms(firing)
    serv.stop()
    time.sleep(0.5)
    serv.off()