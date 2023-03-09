from machine import Pin, I2C

i2c_list = []
i2c_list.append(I2C(0))
i2c_list.append(I2C(1))

for bus in range(0, len(i2c_list)):
    print("\n👀 Scanning bus %d..." %(bus))
    for addr in i2c_list[bus].scan():
        print("🙌 Found device on bus %d at address 0x%x" %(bus, addr))
