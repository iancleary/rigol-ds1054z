import pyvisa


def test_pyvisa_resource_manager():
    rm = pyvisa.ResourceManager()

    assert rm is not None
    assert isinstance(rm, pyvisa.ResourceManager)
