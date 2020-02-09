import serial

# Change this if the sensor lies somewhere else, but usually this works.
# you can search for it via "udevadm info -q property --export /dev/ttyUSB0"
# by trying various ttys
dev = serial.Serial('/dev/ttyUSB0', 9600)

if not dev.isOpen():
    dev.open()

msg = dev.read(10)
# check for correct byte order
assert msg[0] == ord(b'\xaa')
assert msg[1] == ord(b'\xc0')
assert msg[9] == ord(b'\xab')

# the interesting values lie here
pm25 = (msg[3] * 256 + msg[2]) / 10.0
pm10 = (msg[5] * 256 + msg[4]) / 10.0

# validate our reading
checksum = sum(v for v in msg[2:8]) % 256
assert checksum == msg[8]

# print
print(f"'PM10': {pm10}, 'PM2_5': {pm25}")
