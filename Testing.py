
# 1: From Alexey Shkarin (BEFORE, check USB port location using terminal) https://github.com/AlexShkarin/pyLabLib/issues/28
print('importing packages...')
from pylablib.devices import Thorlabs
print('finished')

conn = {"port":"/dev/ttyUSB0","baudrate":115200,"rtscts":True}
x = Thorlabs.KinesisPiezoMotor(("serial",conn))


# 2: After 2022, he updated the library s.t this should work https://github.com/AlexShkarin/pyLabLib/issues/28
print('importing packages...')
from pylablib.devices import Thorlabs
print('finished')

x = Thorlabs.KinesisPiezoMotor("/dev/ttyUSB0")


# 3: Try different library - documentation states it should work with linux https://pypi.org/project/thorlabs-apt-device/
"""
In terminal:
sudo pip install --upgrade thorlabs-apt-device

If using this library, I will have to create KIM101 subclass myself
"""
from thorlabs_apt_device import devices
available_devices = devices.aptdevice.list_devices()
print(available_devices)

stage = devices.aptdevice_motor(serial_port="/dev/ttyUSB0")
stage.move_relative(distance=200)

