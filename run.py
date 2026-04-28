from cocotb_tools.runner import get_runner

runner = get_runner("icarus")

runner.build(
    sources=["sync_fifo.sv"],
    hdl_toplevel="sync_fifo"
)

runner.test(
    hdl_toplevel="sync_fifo",
    test_module="test_fifo",
)