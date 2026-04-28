import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def test_reset(dut):
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())
    
    dut.rst_n.value = 0
    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    dut.din_i.value = 0

    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    assert dut.empty_o.value == 1
    assert dut.full_o.value == 0
    assert dut.dout_o.value == 0
 
@cocotb.test()
async def test_write(dut):
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())
    
    dut.rst_n.value = 0
    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    dut.din_i.value = 0

    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    dut.wr_en_i.value = 1
    for i in range(8):
        dut.din_i.value = i + 1
        await RisingEdge(dut.clk)
    dut.wr_en_i.value = 0
    await RisingEdge(dut.clk)

    assert dut.empty_o.value == 0
    assert dut.full_o.value == 1

@cocotb.test()
async def test_read(dut):
    cocotb.start_soon(Clock(dut.clk, 5, unit="ns").start())
    
    dut.rst_n.value = 0
    dut.wr_en_i.value = 0
    dut.rd_en_i.value = 0
    dut.din_i.value = 0

    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    
    dut.wr_en_i.value = 1
    for i in range(8):
        dut.din_i.value = i
        await RisingEdge(dut.clk)
    dut.wr_en_i.value = 0
    await RisingEdge(dut.clk)

    dut.rd_en_i.value = 1
    for i in range(8):
        await RisingEdge(dut.clk)
        assert int(dut.dout_o.value) == i
    dut.rd_en_i.value = 0
    await RisingEdge(dut.clk)

    assert dut.empty_o.value == 1
    assert dut.full_o.value == 0