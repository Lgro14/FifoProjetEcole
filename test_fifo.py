import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly


@cocotb.test()
async def test_reset(dut):
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())
    
    dut.rst_n.value = 0
    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    dut.din_i.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.empty_o.value) == 1
    assert int(dut.full_o.value) == 0
    assert int(dut.dout_o.value) == 0
 
@cocotb.test()
async def test_write(dut):
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())
    
    dut.rst_n.value = 0
    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    dut.din_i.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.rst_n.value = 1
    for i in range(8):
        await FallingEdge(dut.clk)
        dut.wr_en_i.value = 1
        dut.rd_en_i.value = 0
        dut.din_i.value = i + 1
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 0
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.empty_o.value) == 0
    assert int(dut.full_o.value) == 1

@cocotb.test()
async def test_read(dut):
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())
    
    dut.rst_n.value = 0
    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    dut.din_i.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.rst_n.value = 1
    for i in range(8):
        await FallingEdge(dut.clk)
        dut.wr_en_i.value = 1
        dut.rd_en_i.value = 0
        dut.din_i.value = i + 1
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 1
    for i in range(8):
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert int(dut.dout_o.value) == i + 1, f"Expected {i + 1}, got {int(dut.dout_o.value)}"
    await FallingEdge(dut.clk)

    dut.rd_en_i.value = 0
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.empty_o.value) == 1
    assert int(dut.full_o.value) == 0

@cocotb.test()
async def test_wraparound(dut):
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())

    dut.rst_n.value = 0
    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    dut.din_i.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.rst_n.value = 1
    for i in range(8):
        await FallingEdge(dut.clk)
        dut.wr_en_i.value = 1
        dut.rd_en_i.value = 0
        dut.din_i.value = i + 1
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.full_o.value) == 1
    assert int(dut.empty_o.value) == 0
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 1
    for expected in [1, 2, 3, 4]:
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert int(dut.dout_o.value) == expected, f"Expected {expected}, got {int(dut.dout_o.value)}"
    for i in range(4):
        await FallingEdge(dut.clk)
        dut.wr_en_i.value = 1
        dut.rd_en_i.value = 0
        dut.din_i.value = i + 9
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.full_o.value) == 1
    assert int(dut.empty_o.value) == 0
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 1
    for expected in [5, 6, 7, 8, 9, 10, 11, 12]:
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert int(dut.dout_o.value) == expected, f"Expected {expected}, got {int(dut.dout_o.value)}"
    await FallingEdge(dut.clk)

    dut.rd_en_i.value = 0
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.empty_o.value) == 1
    assert int(dut.full_o.value) == 0

@cocotb.test()
async def test_rw_empty(dut):
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())

    dut.rst_n.value = 0
    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    dut.din_i.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.rst_n.value = 1
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 1
    dut.rd_en_i.value = 1
    dut.din_i.value = 6
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.empty_o.value) == 1
    assert int(dut.full_o.value) == 0
    assert int(dut.dout_o.value) == 6, f"Expected 6, got {int(dut.dout_o.value)}"

@cocotb.test()
async def test_rw_middle(dut):
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())

    dut.rst_n.value = 0
    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    dut.din_i.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.rst_n.value = 1
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 1
    dut.rd_en_i.value = 0
    dut.din_i.value = 6
    await FallingEdge(dut.clk)

    dut.din_i.value = 7
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 1
    dut.rd_en_i.value = 1
    dut.din_i.value = 67
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.dout_o.value) == 6, f"Expected 6, got {int(dut.dout_o.value)}"
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 1
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.dout_o.value) == 7, f"Expected 7, got {int(dut.dout_o.value)}"
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.dout_o.value) == 67, f"Expected 67, got {int(dut.dout_o.value)}"
    assert int(dut.empty_o.value) == 1
    assert int(dut.full_o.value) == 0

@cocotb.test()
async def test_rw_full(dut):
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())

    dut.rst_n.value = 0
    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    dut.din_i.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    await ReadOnly()

    for i in range(8):
        await FallingEdge(dut.clk)
        dut.wr_en_i.value = 1
        dut.rd_en_i.value = 0
        dut.din_i.value = i + 1
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.full_o.value) == 1
    assert int(dut.empty_o.value) == 0
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 1
    dut.rd_en_i.value = 1
    dut.din_i.value = 99
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.full_o.value) == 1
    assert int(dut.empty_o.value) == 0
    assert int(dut.dout_o.value) == 1, f"Expected 1, got {int(dut.dout_o.value)}"
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 1
    for expected in [2, 3, 4, 5, 6, 7, 8, 99]:
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert int(dut.dout_o.value) == expected, f"Expected {expected}, got {int(dut.dout_o.value)}"
    await FallingEdge(dut.clk)

    dut.rd_en_i.value = 0
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.empty_o.value) == 1
    assert int(dut.full_o.value) == 0

@cocotb.test()
async def test_write_full(dut):
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())

    dut.rst_n.value = 0
    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    dut.din_i.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.rst_n.value = 1
    for i in range(8):
        await FallingEdge(dut.clk)
        dut.wr_en_i.value = 1
        dut.rd_en_i.value = 0
        dut.din_i.value = i
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 1
    dut.rd_en_i.value = 0
    dut.din_i.value = 99
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.full_o.value) == 1
    assert int(dut.empty_o.value) == 0
    await FallingEdge(dut.clk)

    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 1
    for expected in range(8):
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert int(dut.dout_o.value) == expected, f"Expected {expected}, got {int(dut.dout_o.value)}"
    await FallingEdge(dut.clk)

    dut.rd_en_i.value = 0
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.empty_o.value) == 1
    assert int(dut.full_o.value) == 0

@cocotb.test()
async def test_read_empty(dut):
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())

    dut.rst_n.value = 0
    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    dut.din_i.value = 0
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.rst_n.value = 1
    await FallingEdge(dut.clk)

    dut.rd_en_i.value = 1
    await RisingEdge(dut.clk)
    await ReadOnly()
    
    assert int(dut.empty_o.value) == 1
    assert int(dut.full_o.value) == 0
    assert int(dut.dout_o.value) == 0
    