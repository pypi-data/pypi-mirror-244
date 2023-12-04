""" module:: tests.test_scenarios
    :platform: Any
    :synopsis: Tests for typical communication scenarios listed in XCP Spec part 5 example communication sequences.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import pytest
from socketcan_xcp.protocol import ConnectMode, DaqProperty, \
    DaqKeyByteAddrExtention, DaqKeyByteIdentificaitonType, DaqKeyByteOptimisation
from socketcan_xcp.server import XcpServerState


class TestScenarioSettingUpASession:

    def test_getting_basic_information(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair

        result = mock_client.connect(mode=ConnectMode.Normal)
        assert result.get("raw") == bytearray.fromhex("FF 15 C0 08 08 00 10 10")
        result = mock_client.get_comm_mode_info()
        assert result.get("raw") == bytearray.fromhex("FF 00 01 00 02 00 00 64")
        result = mock_client.get_status()
        assert result.get("raw") == bytearray.fromhex("FF 00 15 00 00 00")


    @pytest.mark.skip("Incomplete test")
    def test_unlocking_protected_resources_through_seed_and_key_mechanism(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair

        result = mock_client.get_seed(mode=0, resource=1)  # F8 00 01
        assert result.get("raw") == bytearray.fromhex("FF 06 00 01 02 03 04 05")  # length of seed 6, seed 0,1,2,3,4,5

        result = mock_client.unlock(keylen=6, key=bytes.fromhex("69 AB A6 00 00 00")) # FF 06 00 01 02 030 04 05

        assert result.get("raw") == bytearray.fromhex("FF 14")  # protection status 0x14, cal/pag unlocked, daq / PGM protected

        result = mock_client.get_seed(mode=0, resource=4)  # F8 00 04
        assert result.get("raw") == bytearray.fromhex("FF 06 06 07 08 09 0A 0B")  # length of seed 6, seed 6,7,8,9,A,B

        result = mock_client.unlock(keylen=6, key=bytes.fromhex("69 AB A6 00 00 00"))

        assert result.get("raw") == bytearray.fromhex("FF 10")  # protection status 0x10, cal/pag/daq unlocked, PGM protected

        result = mock_client.get_seed(mode=0, resource=0x10)  # F8 00 10
        assert result.get("raw") == bytearray.fromhex("FF 06 05 04 03 02 01 00")  # length of seed 6, seed 5,4,3,2,1,0

        result = mock_client.unlock(keylen=6, key=bytes.fromhex("11 22 33 22 11 00"))

        assert result.get("raw") == bytearray.fromhex("FF 00")  # protection status 0x10, cal/pag/daq/PGM unlocked



    def test_getting_info_about_daq_processor(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        daq_proc = mock_server._daq_processor
        daq_proc._daq_properties = DaqProperty.DynamicDaqListSuported | DaqProperty.TimestampSupported
        daq_proc._max_daq = 0
        daq_proc._max_event_chan = 1
        daq_proc._min_daq = 0
        daq_proc._daq_key_byte_id_type = DaqKeyByteAddrExtention.Free
        daq_proc._daq_key_byte_id_type = DaqKeyByteIdentificaitonType.RelativeOdtAbsoluteDaqByte
        daq_proc._daq_key_byte_opt = DaqKeyByteOptimisation.Default
        result = mock_client.get_daq_processor_info()
        assert result.get("raw") == bytearray.fromhex("FF 11 00 00 01 00 00 40")

        daq_proc._daq_granularity = 2
        daq_proc._daq_max_elem_size = 0xFD
        daq_proc._timestamp_resolution = 6
        daq_proc._timestamp_size = 2
        daq_proc._timestamp_ticks = 0xA
        daq_proc._stim_granularity = 0
        daq_proc._stim_max_elem_size = 0
        result = mock_client.get_daq_resolution_info()
        assert result.get("raw") == bytearray.fromhex("FF 02 FD 00 00 62 0A 00")

        # for idx in range(daq_proc.max_event_chan):
        #     result = mock_client.get_daq_event_info()
