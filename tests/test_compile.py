import glob
import json

from pymint.mintdevice import MINTDevice


def test_full_flow():
    # Load each of the .mint files in in the tests/mint_files directory

    mint_files = glob.glob('tests/mint_files/*.mint')
    for mint_file in mint_files:
        # Load the mint file
        mint_device = MINTDevice.from_mint_file(mint_file)
        # Convert it to Parchmint
        parchmint_device = mint_device.to_parchmint_json()
        # Write the Parchmint to a file
        with open(mint_file.replace('.mint', '.json'), 'w') as f:
            json.dump(parchmint_device, f)

        # TODO - Now check if two json objects are equal
        pass
    

        