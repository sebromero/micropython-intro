from machine import Pin, ADC, UART, SoftI2C
from my9221 import MY9221
from DFPlayer import DFPlayer
from rotary_irq_rp2 import RotaryIRQ
import ssd1306_1315 as ssd

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

class MusicPlayer:
    def __init__(self, uart):
        self.player = DFPlayer(uart=uart)
        self.volume = 10
        self.player.set_volume(10)
        self.current_track = 1
    
    def is_paused(self):
        return self.player.get_status() == self.player.STATUS_PAUSED
    
    def is_busy(self):
        return self.player.get_status() == self.player.STATUS_BUSY

    def max_track(self):
        return self.player.num_files()

    def next_track(self):
        self.current_track += 1
        if self.current_track > self.max_track():
            self.current_track = 1
        self.player.play(track=self.current_track)

    def prev_track(self):
        self.current_track -= 1
        if self.current_track < 1:
            self.current_track = self.max_track()
        self.player.play(track=self.current_track)

    def play(self):
        if self.is_busy():
            return
        self.player.play()
    
    def pause(self):
        if self.is_paused():
            return
        self.player.pause()

    def toggle(self):
        if self.is_paused() or not self.is_busy():
            self.play()
        elif self.is_busy():
            self.pause()

    def set_volume(self, volume):
        if volume != self.volume:
            self.volume = volume
            self.player.set_volume(volume)

def map_range(value, in_min, in_max, out_min, out_max):
    return round(out_min + (((value - in_min) / (in_max - in_min)) * (out_max - out_min)))

def on_button_release(pin):
    if pin.value() == 0: # button is released
        player.toggle()

def update_display():
    oled.fill(0)
    oled.text("Current Track:", 10, 20)
    oled.text(str(player.current_track), 10, 35)
    oled.show()

i2c_bus = SoftI2C(scl = Pin(13), sda = Pin(12), freq = 100000) # I2C0 on Nano RP2040 Connect
oled = ssd.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c_bus)
player = MusicPlayer(uart=UART(0, tx=Pin("A2"), rx=Pin("A3"), baudrate=9600))
ledbar = MY9221(Pin(19), Pin(20)) # D7, D8 on Nano RP2040 Connect
ledbar.reverse(True)
potentiometer = ADC(Pin(26)) # GPIO26 = A0 on Nano RP2040 Connect
button = Pin(25, Pin.IN) # GPIO25 = D2 on Nano RP2040 Connect
button.irq(handler=on_button_release) # trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING) is default
encoder = RotaryIRQ("D10", "D11", min_val = 0, max_val = 10, range_mode = RotaryIRQ.RANGE_UNBOUNDED)
encoder_value = 0
update_display()

while True:
    level = map_range(potentiometer.read_u16(), 176, 65359, 10, 0)
    ledbar.level(level)
    player.set_volume(level * 10)
    new_encoder_value = encoder.value()

    if new_encoder_value != encoder_value:

        if new_encoder_value > encoder_value:
            player.next_track()
            update_display()
        
        elif new_encoder_value < encoder_value:
            player.prev_track()
            update_display()
        
        encoder_value = new_encoder_value