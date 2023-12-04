""" module:: tests.test_protocol
    :platform: Any
    :synopsis: Tests for socketcan_xcp.protocol
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""

from socketcan_xcp.protocol import concat_connect_command, parse_connect_command, StdCmd, concat_connect_response, \
    ResourceFlag, ComModeBasicFlag, PacketIdFromServer, concat_disconnect_command, \
    concat_response_packet, parse_packet_from_server, concat_status_response, SessionStatus, \
    ProtectionStatus, parse_packet_from_client, concat_clear_daq_list, concat_set_daq_ptr, concat_write_daq, \
    concat_set_daq_list_mode, DaqListMode, concat_get_daq_list_mode, concat_get_daq_list_mode_response, \
    concat_start_stop_daq_list, DaqStartStopMode, \
    concat_start_stop_daq_list_response, concat_start_stop_daq_sync, concat_get_daq_clock_response, \
    concat_read_daq_response, concat_get_daq_resolution_info_response, \
    concat_get_server_id, concat_get_daq_id, concat_set_daq_id, concat_get_seed


class TestConcatAndParsers:

    def test_connect_command(self, connect_mode):
        data = concat_connect_command(mode=connect_mode)
        result = parse_connect_command(data)
        assert result.get("mode") == connect_mode
        assert result.get("pid") == StdCmd.Connect

    def test_connect_response(self, endianess):
        resource_flags = ResourceFlag(
            ResourceFlag.CalibrationAndPagingSupported | ResourceFlag.DaqSupported | ResourceFlag.StimSupported
            | ResourceFlag.ProgrammingSupported)
        com_mode_basic_flags = ComModeBasicFlag(
            ComModeBasicFlag.SlaveBlockModeAvailable | ComModeBasicFlag.MoreTypesAvailable
            | ComModeBasicFlag.AddressGranularity0 | ComModeBasicFlag.AddressGranularity1)
        if endianess == "big":
            com_mode_basic_flags |= ComModeBasicFlag.MSBFirst
        protocol_version = 1
        transport_version = 1
        max_cto = 1
        max_dto = 1
        granularity = (com_mode_basic_flags >> 1) & 0x3
        command_response_data = concat_connect_response(resource=resource_flags,
                                                        com_mode_basic=com_mode_basic_flags,
                                                        protocol_layer_version=protocol_version,
                                                        transport_layer_version=transport_version,
                                                        max_cto=max_cto,
                                                        max_dto=max_dto
                                                        )
        result = parse_packet_from_server(cmd=StdCmd.Connect,
                                          data=concat_response_packet(command_response_data=command_response_data),
                                          endianess=endianess)

        assert result.get("resource_flags") == resource_flags
        assert result.get("com_mode_basic_flags") == com_mode_basic_flags
        assert result.get("granularity") == granularity
        assert result.get("max_cto") == max_cto
        assert result.get("max_dto") == max_dto
        assert result.get("protocol_layer_version") == protocol_version
        assert result.get("transport_layer_version") == transport_version

    def test_disconnect(self):
        assert concat_disconnect_command() == bytes((StdCmd.Disconnect,))

    def test_response(self):
        assert concat_response_packet() == bytes((PacketIdFromServer.Response,))

    def test_parse_packet_from_server(self, packet_id_from_server, endianess):
        data = bytearray(8)
        data[0] = packet_id_from_server
        assert parse_packet_from_server(cmd=StdCmd.Connect, data=data, endianess=endianess)

        assert parse_packet_from_server(cmd=StdCmd.Connect, data=bytes(8), endianess=endianess) == {"raw": bytes(8)}

    def test_concat_status_response(self, endianess):
        data = concat_status_response(session_status=SessionStatus(0),
                                      resource_protection_status=ProtectionStatus(0),
                                      session_config_id=0,
                                      endianess=endianess)

    def test_parse_packet_from_client_DTO(self, endianess):
        result = parse_packet_from_client(bytes(8), endianess=endianess)
        assert result.get("packet_type") == "DTO"

    def test_parse_packet_from_client_CTO(self, endianess):
        result = parse_packet_from_client(concat_connect_command(), endianess=endianess)
        assert result.get("packet_type") == "CTO"

    def test_concat_clear_daq_list(self, endianess):
        daq_list = 0x42
        result = parse_packet_from_client(concat_clear_daq_list(daq_list=daq_list, endianess=endianess),
                                          endianess=endianess)
        assert result.get("daq_list") == daq_list

    def test_concat_set_daq_ptr(self, endianess):
        daq_list = 0xDEAD
        odt_list = 0x42
        odt_elem = 0x84
        result = parse_packet_from_client(concat_set_daq_ptr(daq_list=daq_list, odt_list=odt_list, odt_elem=odt_elem,
                                                             endianess=endianess),
                                          endianess=endianess)
        assert result.get("daq_list") == daq_list
        assert result.get("odt_list") == odt_list
        assert result.get("odt_elem") == odt_elem

    def test_concat_write_daq(self, endianess):
        addr = 0xDEADBEEF
        ext = 0
        size = 0x42
        bit_offset = 4
        result = parse_packet_from_client(concat_write_daq(bit_offset=bit_offset, size=size, ext=ext, addr=addr,
                                                           endianess=endianess),
                                          endianess=endianess)
        assert result.get("bit_offset") == bit_offset
        assert result.get("size") == size
        assert result.get("ext") == ext
        assert result.get("addr") == addr

    def test_set_daq_list_mode(self, endianess):
        daq_list = 0xDEAD
        chan = 0xBEEF
        mode = DaqListMode(0)
        prescaler = 1
        prio = 0xFF
        result = parse_packet_from_client(concat_set_daq_list_mode(daq_list=daq_list, mode=mode, chan=chan,
                                                                   prescaler=prescaler, prio=prio, endianess=endianess),
                                          endianess=endianess)
        assert result.get("daq_list") == daq_list
        assert result.get("chan") == chan
        assert result.get("mode") == mode
        assert result.get("prescaler") == prescaler
        assert result.get("prio") == prio

    def test_get_daq_list_mode(self, endianess):
        daq_list = 0xDEAD
        chan = 0xBEEF
        mode = DaqListMode(0)
        prescaler = 1
        prio = 0xFF
        result = parse_packet_from_client(concat_get_daq_list_mode(daq_list=daq_list, endianess=endianess),
                                          endianess=endianess)
        assert result.get("daq_list") == daq_list

        result = parse_packet_from_server(cmd=StdCmd.GetDaqListMode, data=concat_response_packet(
            command_response_data=concat_get_daq_list_mode_response(
                mode=mode,
                chan=chan,
                prescaler=prescaler,
                prio=prio,
                endianess=endianess
            )), endianess=endianess)
        assert result.get("chan") == chan
        assert result.get("mode") == mode
        assert result.get("prescaler") == prescaler
        assert result.get("prio") == prio

    def test_concat_start_stop_daq_list(self, endianess):
        daq_list = 0xDEAD
        mode = DaqStartStopMode(0)
        result = parse_packet_from_client(
            concat_start_stop_daq_list(mode=mode, daq_list=daq_list, endianess=endianess), endianess=endianess)
        assert result.get("daq_list") == daq_list
        assert result.get("mode") == mode

        first_pid = 0x42
        result = parse_packet_from_server(cmd=StdCmd.StartStopDaqList,
                                          data=concat_response_packet(
                                              command_response_data=concat_start_stop_daq_list_response(
                                                  first_pid=first_pid)),
                                          endianess=endianess)
        assert result.get("first_pid") == first_pid

    def test_concat_start_stop_daq_sync(self):
        mode = DaqStartStopMode(0)
        assert concat_start_stop_daq_sync(mode=mode) == bytes((StdCmd.StartStopSync, mode))

    def test_concat_get_daq_clock_response(self, endianess):
        timestamp = 0x12345678

        result = parse_packet_from_server(cmd=StdCmd.GetDaqClock,
                                          data=concat_response_packet(
                                              command_response_data=concat_get_daq_clock_response(timestamp=timestamp,
                                                                                                  endianess=endianess)),
                                          endianess=endianess)
        assert result.get("timestamp") == timestamp

    def test_concat_read_daq_response(self, endianess):
        addr = 0xDEADBEEF
        ext = 0
        size = 0x42
        bit_offset = 4
        result = parse_packet_from_server(cmd=StdCmd.ReadDaq,
                                          data=concat_response_packet(
                                              command_response_data=concat_read_daq_response(addr=addr, ext=ext,
                                                                                             endianess=endianess,
                                                                                             size=size,
                                                                                             bit_offset=bit_offset)),
                                          endianess=endianess)
        assert result.get("bit_offset") == bit_offset
        assert result.get("size") == size
        assert result.get("ext") == ext
        assert result.get("addr") == addr

    def test_parse_get_daq_resolution_info_response(self, endianess):
        daq_granularity = 4
        daq_max_elem_size = 4
        stim_granularity = 4
        stim_max_elem_size = 4
        timestamp_resolution = 9
        timestamp_size = 4
        timestamp_fixed = False
        timestamp_ticks = 0x42
        result = parse_packet_from_server(cmd=StdCmd.GetDaqResolutionInfo,
                                          data=concat_response_packet(
                                              command_response_data=concat_get_daq_resolution_info_response(
                                                  daq_granularity=daq_granularity,
                                                  daq_max_elem_size=daq_max_elem_size,
                                                  stim_granularity=stim_granularity,
                                                  stim_max_elem_size=stim_max_elem_size,
                                                  timestamp_resolution=timestamp_resolution,
                                                  timestamp_size=timestamp_size,
                                                  timestamp_fixed=timestamp_fixed,
                                                  timestamp_ticks=timestamp_ticks,
                                                  endianess=endianess)),
                                          endianess=endianess)
        assert result.get("daq_granularity") == daq_granularity
        assert result.get("daq_max_elem_size") == daq_max_elem_size
        assert result.get("stim_granularity") == stim_granularity
        assert result.get("stim_max_elem_size") == stim_max_elem_size
        assert result.get("timestamp_resolution") == timestamp_resolution
        assert result.get("timestamp_size") == timestamp_size
        assert result.get("timestamp_fixed") == timestamp_fixed
        assert result.get("timestamp_ticks") == timestamp_ticks

    def test_parse_parse_transport_layer(self, endianess):
        invert_echo = False
        result = parse_packet_from_client(concat_get_server_id(invert_echo=invert_echo),
                                          endianess=endianess)
        assert result.get("invert_echo") == invert_echo

    def test_parse_get_daq_id(self, endianess):
        daq_list = 0x1234
        result = parse_packet_from_client(concat_get_daq_id(daq_list=daq_list,
                                                            endianess=endianess),
                                          endianess=endianess)
        assert result.get("daq_list") == daq_list

    def test_parse_set_daq_id(self, endianess):
        daq_list = 0x1234
        can_id = 0x11223344
        result = parse_packet_from_client(concat_set_daq_id(daq_list=daq_list,
                                                            can_id=can_id,
                                                            endianess=endianess),
                                          endianess=endianess)
        assert result.get("daq_list") == daq_list
