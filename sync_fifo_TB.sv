`timescale 1ns / 1ps

module tb_fifo();

    parameter WIDTH = 8;
    parameter DEPTH = 8;

    logic clk;
    logic rst_n;
    logic wr_en;
    logic rd_en;
    logic [WIDTH-1:0] d_in;

    logic [WIDTH-1:0] d_out;
    logic full;
    logic empty;

    integer idx;


    sync_fifo #(
        .WIDTH(WIDTH),
        .DEPTH(DEPTH)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .wr_en_i(wr_en),
        .rd_en_i(rd_en),
        .din_i(d_in),
        .dout_o(d_out),
        .full_o(full),
        .empty_o(empty)
    );


    initial begin
        clk = 1;
        forever #5 clk = ~clk; // (Periodo de 10ns -> 100MHz)
    end


    initial begin
        // Configuración para generar archivos de forma de onda (VCD)
        $dumpfile("fifo_TB.vcd");
        $dumpvars(0, tb_fifo);
        for(idx = 0; idx < DEPTH; idx = idx +1)  $dumpvars(0, tb_fifo.dut.mem[idx]);

        // 0. Inicialización de señales
        rst_n = 0;
        wr_en = 0;
        rd_en = 0;
        d_in = 0;

        // Esperar un par de ciclos y soltar el reset
        #20 rst_n = 1;
        #10;

        $display("--- Iniciando pruebas de la FIFO ---");

        // 1. Prueba de ESCRITURA hasta llenar la memoria
        $display("[%0t] TEST 1: Escribiendo datos en la FIFO...", $time);
        wr_en = 1;
        // Escribimos DEPTH veces para intentar llenarla
        repeat (DEPTH) begin
            d_in = $random; // Dato aleatorio
            #10;
        end
        wr_en = 0;
        #20;

        // 2. Prueba de LECTURA hasta vaciar la memoria
        $display("[%0t] TEST 2: Leyendo datos de la FIFO...", $time);
        rd_en = 1;
        repeat (DEPTH+3) begin
            #10;
        end
        rd_en = 0;
        #20;

  

        $display("[%0t] TEST 3: Escritura y Lectura simultánea...", $time);
        // Primero metemos un dato
        rd_en = 1; wr_en = 1; d_in = 8'hAA; #10;
        // Ahora leemos y escribimos al mismo tiempo
        rd_en = 1; wr_en = 1; d_in = 8'hBB; #10;
        rd_en = 1; wr_en = 1; d_in = 8'hCC; #10;
        
        // Dejamos de escribir, solo leemos el último
        wr_en = 0; #10;
        rd_en = 0; #20;

        $display("[%0t] --- Pruebas finalizadas ---", $time);
        $finish;
    end


    always @(posedge clk) begin
        if (wr_en && !full && !rst_n)
            $display("Write: d_in = %h | wr_ptr = %d", d_in, dut.wrptr_q);
        if (rd_en && !empty && !rst_n)
            $display("Read:   d_out = %h | rd_ptr = %d", dut.mem[dut.rdptr_q], dut.rdptr_q);
    end

endmodule
