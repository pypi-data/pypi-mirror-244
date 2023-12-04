""" module:: tests.test_client
    :platform: Any
    :synopsis: Tests for socketcan_xcp.client
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""

import pytest

from socketcan_xcp.protocol import DaqListMode, DaqStartStopMode, XcpTrueTimeout, XcpErrorOutOfRange
from socketcan_xcp.server import XcpServerState

import logging

LOGGER = logging.getLogger(__name__)


class TestClient:

    def test_connect(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair

        mock_server.state = XcpServerState.NotConnected
        response = mock_client.connect()
        LOGGER.info(response)
        assert mock_client.endianess == mock_server.endianess
        assert mock_server.state == XcpServerState.Connected

    def test_disconnect(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        response = mock_client.disconnect()
        LOGGER.info(response)
        assert mock_server.state == XcpServerState.NotConnected

    def test_get_status(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        LOGGER.info(mock_client.state)
        response = mock_client.get_status()
        LOGGER.info(response)

    def test_get_comm_mode_info(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        response = mock_client.get_comm_mode_info()
        LOGGER.info(response)

    def test_clear_daq_list_config(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        response = mock_client.clear_daq_list(daq_list=0)
        LOGGER.info(response)

    def test_set_daq_ptr(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        response = mock_client.set_daq_ptr(daq_list=0, odt_list=0, odt_elem=0)
        LOGGER.info(response)
        with pytest.raises(XcpErrorOutOfRange):
            mock_client.set_daq_ptr(daq_list=0xCAFE, odt_list=0x11, odt_elem=0x22)

    def test_write_daq(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        response = mock_client.set_daq_ptr(daq_list=0, odt_list=0, odt_elem=0)
        response = mock_client.write_daq(bit_offset=0x4, size=0x32, ext=3, addr=0xDEADBEEF)
        LOGGER.info(response)

    def test_set_daq_list_mode(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        response = mock_client.set_daq_list_mode(daq_list=0, mode=DaqListMode(0), chan=0xBEEF,
                                                 prescaler=1, prio=0xFF)
        LOGGER.info(response)

    def test_get_daq_list_mode(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        response = mock_client.get_daq_list_mode(daq_list=0)
        LOGGER.info(response)

    def test_start_stop_daq_list(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        mode = DaqStartStopMode(0)
        response = mock_client.start_stop_daq_list(daq_list=0, mode=mode)
        LOGGER.info(response)

    def test_start_stop_daq_sync(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        mode = DaqStartStopMode(0)
        response = mock_client.start_stop_daq_sync(mode=mode)
        LOGGER.info(response)

    def test_get_daq_clock(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        response = mock_client.get_daq_clock()
        LOGGER.info(response)

    def test_read_daq(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess

        response = mock_client.set_daq_ptr(daq_list=0, odt_list=0, odt_elem=0)
        response = mock_client.read_daq()
        LOGGER.info(response)

    def test_timeout(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess

        mock_server.cause_timeout(cnt=1)
        mock_client.set_daq_ptr(daq_list=0, odt_list=0, odt_elem=0)

        mock_server.cause_timeout(cnt=2)
        mock_client.set_daq_ptr(daq_list=0, odt_list=0, odt_elem=0)

        mock_server.cause_timeout(cnt=3)
        with pytest.raises(XcpTrueTimeout):
            mock_client.set_daq_ptr(daq_list=0, odt_list=0, odt_elem=0)

    def test_get_daq_processor_info(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        response = mock_client.get_daq_processor_info()
        LOGGER.info(response)

    def test_get_daq_resolution_info(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        response = mock_client.get_daq_resolution_info()
        LOGGER.info(response)

    def test_get_server_id(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        response = mock_client.get_server_id(invert_echo=False)
        LOGGER.info(response)
        response = mock_client.get_server_id(invert_echo=True)
        LOGGER.info(response)

    def test_get_daq_id(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        daq_list = 0
        response = mock_client.get_daq_id(daq_list=daq_list)
        LOGGER.info(response)

    def test_set_daq_id(self, mock_client_server_pair):
        mock_client, mock_server = mock_client_server_pair
        mock_server.state = XcpServerState.Connected
        mock_client.endianess = mock_server.endianess
        daq_list = 0
        can_id = 0x500
        response = mock_client.set_daq_id(daq_list=daq_list,
                                          can_id=can_id)
        LOGGER.info(response)
