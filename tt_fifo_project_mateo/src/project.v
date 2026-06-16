/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_mateo_fifo (
    //puertos wrapperpero q
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  //declaracion
  wire       wr_en_i; 
  wire       rd_en_i;
  wire [7:0] din_i;
  
  wire       full_o;
  wire       empty_o;
  wire [7:0] dout_o;

  //asignacion
  assign wr_en_i      = uio_in[0]; //lo que ordenen de fuera será la orden en la FIFO
  assign rd_en_i      = uio_in[1];
  assign din_i        = ui_in;
  
  //assign uio_oe = {4'b0000, 1'b1, 1'b1, 2'b00};
  assign uio_out[1:0] = 0; 
  assign uio_out[7:4] = 0;
  assign uio_out[2]   = full_o ; //la salida de la FIFO será lo que salga afuera
  assign uio_out[3]   = empty_o ;
  assign uo_out       = dout_o;


  assign uio_oe[0]    = 0; //la posición 0 en uio (wr) funciona como in
  assign uio_oe[1]    = 0;
  assign uio_oe[2]    = 1; //la posición 2 en uio (full) funciona como out
  assign uio_oe[3]    = 1;
  assign uio_oe[7:4]  = 0;
  
  
  
  sync_fifo fifo_inst (
    .clk(clk),
    .rst_n(rst_n),

    .wr_en_i(wr_en_i),
    .rd_en_i(rd_en_i),
    .din_i(din_i),

    .full_o(full_o),
    .empty_o(empty_o),
    .dout_o(dout_o)
  );

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in[7:2], 1'b0};

endmodule
