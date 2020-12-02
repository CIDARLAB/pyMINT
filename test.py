from pymint.mintdevice import MINTDevice
import pathlib
import json

filepath = "/home/krishna/CIDAR/pyfluigi/test/chthesis/net_mux.mint"

device = MINTDevice.from_mint_file(filepath)

print("# Components: {}".format(len(device.get_components())))
print("# Connections: {}".format(len(device.get_connections())))

print("Constraints:")
for constraint in device.get_constraints():
    print(constraint)

OUTPUT_DIR = pathlib.Path("~/Desktop/MINT").parent.parent.absolute()

tt = "{}.json".format(device.name)
dump = device.to_parchmint_v1()
with open(tt, "w") as f:
    json.dump(dump, f)
