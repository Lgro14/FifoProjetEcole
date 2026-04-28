module cocotb_iverilog_dump();
initial begin
    string dumpfile_path;    if ($value$plusargs("dumpfile_path=%s", dumpfile_path)) begin
        $dumpfile(dumpfile_path);
    end else begin
        $dumpfile("/home/lgro/fifo/sim_build/sync_fifo.fst");
    end
    $dumpvars(0, sync_fifo);
end
endmodule
