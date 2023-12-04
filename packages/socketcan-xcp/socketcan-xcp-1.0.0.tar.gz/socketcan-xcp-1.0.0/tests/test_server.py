""" module:: tests.test_server
    :synopsis: Tests for socketcan_xcp.server
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import time

import pytest

from socketcan_xcp.protocol import concat_connect_command, parse_packet_from_server, PacketIdFromServer, \
    concat_disconnect_command, concat_get_status_command, StdCmd, concat_get_comm_mode_info
from socketcan_xcp.server import XcpServer, XcpServerState
from tests.mocks import MockTransport


@pytest.fixture(scope="class")
def mock_transport() -> MockTransport:
    return MockTransport()


@pytest.fixture(scope="class")
def mock_server(mock_transport) -> XcpServer:
    # noinspection PyTypeChecker
    return XcpServer(transport=mock_transport)


class TestStdCommands:

    def test_connect(self, mock_server, mock_transport):
        """
        Test the server state machine switching
        :param mock_server: Fixture
        :param mock_transport: Fixture
        :return: Nothing
        """
        mock_server._state = XcpServerState.NotConnected
        command = concat_connect_command()
        mock_transport.rx_queue.put(command)
        response = parse_packet_from_server(cmd=StdCmd.Connect, data=mock_transport.tx_queue.get(timeout=.1), endianess=mock_server.endianess)
        time.sleep(.01)
        assert mock_server.state == XcpServerState.Connected
        assert response.get("packet_id") == PacketIdFromServer.Response

    def test_disconnect(self, mock_server, mock_transport):
        """
        Test the server state machine switching
        :param mock_server: Fixture
        :param mock_transport: Fixture
        :return: Nothing
        """
        mock_server._state = XcpServerState.Connected
        command = concat_disconnect_command()
        mock_transport.rx_queue.put(command)
        response = parse_packet_from_server(cmd=StdCmd.Disconnect, data=mock_transport.tx_queue.get(timeout=.1), endianess=mock_server.endianess)
        time.sleep(.01)
        assert mock_server.state == XcpServerState.NotConnected
        assert response.get("packet_id") == PacketIdFromServer.Response

    def test_get_status(self, mock_server, mock_transport):
        """
        Test the server state machine switching
        :param mock_server: Fixture
        :param mock_transport: Fixture
        :return: Nothing
        """
        mock_server._state = XcpServerState.Connected
        command = concat_get_status_command()
        mock_transport.rx_queue.put(command)

        result = parse_packet_from_server(cmd=StdCmd.GetStatus,data=mock_transport.tx_queue.get(timeout=1),
                                          endianess=mock_server.endianess
                                          )
        assert result.get("session_status") == mock_server.session_status
        assert result.get("protection_status") == mock_server.protection_status
        assert result.get("session_config_id") == mock_server.session_config_id

    def test_concat_get_comm_mode_info(self, mock_server, mock_transport):
        """
        Test the server state machine switching
        :param mock_server: Fixture
        :param mock_transport: Fixture
        :return: Nothing
        """
        mock_server._state = XcpServerState.Connected
        command = concat_get_comm_mode_info()
        mock_transport.rx_queue.put(command)
        result = parse_packet_from_server(cmd=StdCmd.GetCommModeInfo, data=mock_transport.tx_queue.get(timeout=1),
                                          endianess=mock_server.endianess
                                          )
        assert result.get("comm_mode_optional") == mock_server.com_mode_optional
        assert result.get("max_bs") == mock_server.max_bs
        assert result.get("min_st") == mock_server.min_st
        assert result.get("queue_size") == mock_server.queue_size
        assert result.get("xcp_driver_version") == mock_server.xcp_driver_version

    def test_unhandled_command(self, mock_server, mock_transport):
        """
        Test the server state machine switching
        :param mock_server: Fixture
        :param mock_transport: Fixture
        :return: Nothing
        """
        mock_server._state = XcpServerState.Connected
        command = bytearray(8)
        command[0] = StdCmd.CopyCalPage
        mock_transport.rx_queue.put(command)

