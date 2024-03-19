"""! @file encoder_reader.py

@author Nathaniel Davis
@author Sebastian Bessoudo
@date 02-12-2024
"""

import pyb
import time

class Encoder:
    """!
    This class implements an encoder for the motor for an ME405 kit.
    """

    def __init__(self, enA, enB, readch, enAch, enBch):
        """!
        Initializes the encoder. Also sets up a 
        @param enA encoder channel A pin
        @param enB encoder channel B pin
        @param timer timer used for both encoder pins
        @param enAch timer channel for encoder channel A
        @param enBch timer channel for encoder channel B
        """
        
        # sets up pin A and B of the encoder
        self.pinA = pyb.Pin(enA, pyb.Pin.OUT_PP)
        self.pinB = pyb.Pin(enB, pyb.Pin.OUT_PP)
        
        # sets up the timer channel to read the encoder pins and read out position
        self.reader = pyb.Timer(readch, period=3200, prescaler=0)
        self.chA = self.reader.channel(enAch, pyb.Timer.ENC_AB, pin=self.pinA)
        self.chB = self.reader.channel(enBch, pyb.Timer.ENC_AB, pin=self.pinB)
        
        self.pos = 0
        self.oldcounter = 0
        self.reader.counter(0)
        
        self.autoreload = 3200
        
        print("Initializing Encoder")

    def read(self):
        """!
        reads the current encoder position
        and checks for overflow or underflow
        when delta has exceeded positively or negatively half of the 65536 ticks
        """

        # new encoder position = read encoder position
        self.newcounter = self.reader.counter()
        # change in encoder = new encoder position - old encoder position
        delta = self.newcounter - self.oldcounter
        # update old encoder position to new encoder position
        self.oldcounter = self.newcounter
        
        # check for overflow or underflow, correct delta if needed
        # underflow occurs if the delta is greater than half the encoder max
        if delta >= 0.5*(self.autoreload):
            delta -= self.autoreload
        # overflow occurs if the delta is less than negative of half the encoder max
        elif delta <= -0.5*(self.autoreload):
            delta += self.autoreload

            
        # find new position using deltath
        self.pos += delta

#         print("Delta = " + str(delta))
#         print("Position = " + str(self.pos))
        return self.pos

    def zero(self):
        """!
        Resets position from the encoder back to 0
        """
        self.pos = 0

if __name__ == "__main__":
    enc1 = Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8, 1, 2)
    enc2 = Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4, 1, 2)
    
    # unecessary resetting; for testing purposes only
    enc1.zero()
    enc2.zero()
    
    # sets up the timer to read store the encoder data every specified amount of time
    while True:
        print(enc1.read())
        time.sleep(0.1)       