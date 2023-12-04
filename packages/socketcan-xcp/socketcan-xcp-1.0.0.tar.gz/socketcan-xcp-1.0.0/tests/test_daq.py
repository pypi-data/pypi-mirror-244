""" module:: tests.test_daq
    :platform: Any
    :synopsis: Tests for socketcan_xcp.daq
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
from random import randint

from socketcan_xcp.daq import OdtList, OdtElem, DaqList, DaqTable
from socketcan_xcp.protocol import DaqListMode


def mock_odt_elem_factory():
    return OdtElem(addr=randint(1, 0xFFFFFFFF),
                   ext=randint(1, 0xFF),
                   size=randint(1, 0xFF),
                   bit_offset=randint(1, 0xFF),
                   )


def mock_odt_list_factory():
    odt_list = OdtList(odt_list_length=randint(1, 20))
    return odt_list


def mock_daq_list_factory():
    daq_list = DaqList(odt_list_length=randint(1, 20),
                       daq_list_length=randint(1, 20),
                       prescaler=1,
                       mode=DaqListMode(0),
                       chan=0,
                       prio=0xFF,
                       first_pid=0
                       )
    return daq_list


def mock_daq_table_factory():
    daq_table = DaqTable(daq_table_length=randint(1,20),
                         odt_list_length=randint(1, 20),
                         daq_list_length=randint(1, 20)
                         )
    return daq_table


class TestObjectGeneration:

    def test_odt_elem(self, addr=0, ext=0, bit_offset=0, size=0):
        elem = OdtElem(addr=addr, ext=ext, bit_offset=bit_offset, size=size)

        assert elem.addr == addr
        assert elem.ext == ext
        assert elem.bit_offset == bit_offset
        assert elem.size == size

    def test_odt_list(self):
        odt = mock_odt_list_factory()
        idx = randint(0, len(odt) - 1)

        this_elem = mock_odt_elem_factory()
        odt.idx = idx
        odt.write(this_elem)
        odt.idx = idx
        read_elem = odt.read()
        assert read_elem.addr == this_elem.addr
        assert read_elem.ext == this_elem.ext
        assert read_elem.size == this_elem.size
        assert read_elem.bit_offset == this_elem.bit_offset

    def test_daq_list(self):
        daq_list = mock_daq_list_factory()
        odt_list_idx = randint(0, len(daq_list) - 1)
        assert isinstance(daq_list.elems[odt_list_idx], OdtList)

        odt_elem_idx = randint(0, len(daq_list.elems[odt_list_idx]) - 1)

        daq_list.set_ptr(
            odt_list_idx=odt_list_idx,
            odt_elem_idx=odt_elem_idx
        )
        this_elem = mock_odt_elem_factory()
        daq_list.write(this_elem)
        daq_list.set_ptr(
            odt_list_idx=odt_list_idx,
            odt_elem_idx=odt_elem_idx
        )
        read_elem = daq_list.read()
        assert read_elem.addr == this_elem.addr
        assert read_elem.ext == this_elem.ext
        assert read_elem.size == this_elem.size
        assert read_elem.bit_offset == this_elem.bit_offset

    def test_daq_table(self):
        daq_table = mock_daq_table_factory()
        daq_table_idx = randint(0, len(daq_table) - 1)
        daq_list = daq_table.elems[daq_table_idx]
        odt_list_idx = randint(0, len(daq_list) - 1)
        odt_elem = daq_list.elems[odt_list_idx]
        odt_elem_idx = randint(0, len(odt_elem) - 1)

        daq_table.set_ptr(
            daq_list_idx=daq_table_idx,
            odt_list_idx=odt_list_idx,
            odt_elem_idx=odt_elem_idx
        )
        this_elem = mock_odt_elem_factory()
        daq_table.write(this_elem)
        daq_table.set_ptr(
            daq_list_idx=daq_table_idx,
            odt_list_idx=odt_list_idx,
            odt_elem_idx=odt_elem_idx
        )
        read_elem = daq_table.read()
        assert read_elem.addr == this_elem.addr
        assert read_elem.ext == this_elem.ext
        assert read_elem.size == this_elem.size
        assert read_elem.bit_offset == this_elem.bit_offset
