`timescale 1ns/1ps

module sync_fifo #(
    parameter DEPTH = 8,
    parameter WIDTH = 8
)(
    input logic clk,
    input logic rst_n,
    input logic wr_en_i,
    input logic [WIDTH-1:0] din_i,
    input logic rd_en_i,
    output logic [WIDTH-1:0] dout_o,
    output logic full_o,
    output logic empty_o
);

logic [WIDTH-1:0] mem [0:DEPTH-1];

localparam int nbit = DEPTH <= 1 ? 1 : $clog2(DEPTH) - 1;
localparam int ncount = $clog2(DEPTH + 1) - 1;


logic [nbit:0] wrptr;
logic [nbit:0] rdptr;
logic [ncount:0] count;

assign empty_o = (count == 0);
assign full_o = (count == DEPTH);
assign dout_o = mem[rdptr];

always_ff @(posedge clk) begin
    if (!rst_n) begin
        wrptr <= '0;
        rdptr <= '0;
        count <= '0;
    end else begin
        if (wr_en_i && rd_en_i && !full_o && !empty_o) begin
            mem[wrptr] <= din_i;
            if (wrptr == DEPTH-1)
                wrptr <= '0;
            else
                wrptr <= wrptr + 1;

            if (rdptr == DEPTH-1)
                rdptr <= '0; 
            else
                rdptr <= rdptr + 1;
        end else if (wr_en_i && !full_o) begin
            mem[wrptr] <= din_i;
            if (wrptr == DEPTH-1)
                wrptr <= '0;
            else
                wrptr <= wrptr + 1;
            count <= count + 1;
        end else if (rd_en_i && !empty_o) begin
            if (rdptr == DEPTH-1)
                rdptr <= '0;
            else
                rdptr <= rdptr + 1;
            count <= count - 1;
        end
    end
end

endmodule