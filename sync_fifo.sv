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

localparam int nbit = 
    DEPTH <= 1 ? 1 :
    $clog2(DEPTH) - 1;
localparam int ncount = $clog2(DEPTH + 1) - 1;


logic [nbit:0] wrptr_q;
logic [nbit:0] rdptr_q;
logic [ncount:0] count_q;

logic [nbit:0] wrptr_d;
logic [nbit:0] rdptr_d;
logic [ncount:0] count_d;

assign empty_o = (count_q == 0);
assign full_o = (count_q == DEPTH);

always_comb begin
    wrptr_d = wrptr_q;
    rdptr_d = rdptr_q;
    count_d = count_q;

    if (wr_en_i && rd_en_i) begin
        if (!empty_o) begin
            if (wrptr_q == DEPTH-1)
                wrptr_d = '0;
            else
                wrptr_d = wrptr_q + 1;

            if (rdptr_q == DEPTH-1)
                rdptr_d = '0;
            else
                rdptr_d = rdptr_q + 1;
        end
        count_d = count_q;
    end
    else if (wr_en_i && !full_o) begin
        if (wrptr_q == DEPTH-1)
            wrptr_d = '0;
        else
            wrptr_d = wrptr_q + 1;
        count_d = count_q + 1;

    end
    else if (rd_en_i && !empty_o) begin
        if (rdptr_q == DEPTH-1)
            rdptr_d = '0;
        else
            rdptr_d = rdptr_q + 1;
        count_d = count_q - 1;
    end
end

always_ff @(posedge clk) begin
    if (!rst_n) begin
        wrptr_q <= '0;
        rdptr_q <= '0;
        count_q <= '0;
    end
    else begin
        wrptr_q <= wrptr_d;
        rdptr_q <= rdptr_d;
        count_q <= count_d;
        if (wr_en_i && ((!rd_en_i && !full_o) || (rd_en_i && !empty_o))) begin
            mem[wrptr_q] <= din_i;
        end
        if(empty_o && wr_en_i && rd_en_i) begin
            dout_o <= din_i;
        end
        else if (rd_en_i) begin
            dout_o <= mem[wrptr_q];
        end
        else begin
            dout_o <= 0;
        end
    end
end


endmodule