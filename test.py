from pymint.mintdevice import MINTDevice
import pymint

filepath = "/home/krishna/CIDAR/pyfluigi/test/constraints/tree_constraint.mint"

device = MINTDevice.from_mint_file(filepath)

print("# Components: {}".format(len(device.get_components())))
print("# Connections: {}".format(len(device.get_connections())))

print("Constraints:")
for constraint in device.get_constraints():
    print(constraint)
