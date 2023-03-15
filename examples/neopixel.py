import machine, neopixel
from time import sleep_ms

pixels = neopixel.NeoPixel(machine.Pin("D3"), 1)

# Fades the leds in and out
def fade(cycles, delay_ms=16):
    # Count from 0 to 255 and back the given 
    # amount of times with a step size of 8
    for i in range(0, cycles * 2 * 256, 8):
         
        if (i // 256) % 2 == 0:
            # Fading in: Convert to value 0 - 255
            val = i & 0xff
        else:
            # Fading out: Convert to value 255 - 0
            val = 255 - (i & 0xff)
        pixels.fill((val, 0, 0))
        pixels.write()
        sleep_ms(delay_ms)
    
    # Clear leds
    pixels.fill((0, 0, 0))
    pixels.write()

# Fade in and out 4 times
print(f'\n🚨 Fading in {pixels.n} LEDs...')
fade(4)