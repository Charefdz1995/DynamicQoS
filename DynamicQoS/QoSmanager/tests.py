# Create your tests here.
import napalm

driver = napalm.get_network_driver('ios')
device = driver(hostname='192.168.5.1', username='admin',
                password='admin')

print('Opening ...')

device.open()
print(device.get_interfaces())