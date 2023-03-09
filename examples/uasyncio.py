# Cooperative multitasking scheduler for MicroPython

from machine import Pin
import uasyncio

async def blink(led, period_ms):
    while True:
        led.on()
        await uasyncio.sleep_ms(100)
        led.off()
        await uasyncio.sleep_ms(period_ms)

async def main():
    uasyncio.create_task(blink(Pin("LED"), 700))
    uasyncio.create_task(blink(Pin("D12"), 400))
    await uasyncio.sleep_ms(10000)

uasyncio.run(main())