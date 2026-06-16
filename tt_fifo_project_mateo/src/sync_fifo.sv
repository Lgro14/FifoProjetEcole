module sync_fifo #(
    
    //Constantes configurables
    parameter int DEPTH = 8,  
    parameter int WIDTH = 8

)(

    //Los puertos son una conexion entre el modulo y el exterior
    input  logic             clk, 
    input  logic             rst_n,
    input  logic             wr_en_i,
    input  logic [WIDTH-1:0] din_i, //Dato de 8 bits
    input  logic             rd_en_i,
    output logic [WIDTH-1:0] dout_o,
    output logic             full_o,
    output logic             empty_o

);  //Señales internas, el exterior no las ve

    localparam int AW = $clog2(DEPTH); //Cantidad de bits de direccion -> Como DEPTH=8, se necesitan 3 bits para direccionar las 8 posiciones
    logic [AW:0] wptr;
    logic [AW:0] rptr;

    logic        do_read;
    logic        do_write;

    logic [WIDTH-1:0] mem [0:DEPTH-1]; //Memoria tipo arreglo


    assign empty_o = (wptr==rptr); //Ya es un condicional perse 
    assign full_o = ((wptr[AW-1:0]==rptr[AW-1:0]) && (wptr[AW]!=rptr[AW]));
    
    //assign do_read = ((rd_en_i==1'b1)&&(empty_o==1'b0));
    assign do_read = (rd_en_i && !empty_o);
    assign do_write = (wr_en_i && !full_o); 

    always_ff @( posedge clk ) begin

        if (!rst_n)begin
            wptr   <= '0;  /// '0 -> Tod0s los bits a 
            rptr   <= '0;
            dout_o <= '0;
        
        end else begin
            if (do_read)begin
                dout_o <= mem[rptr[AW-1:0]];
                rptr   <= rptr + 1'b1;
                
            end 

            if (do_write)begin
                mem[wptr[AW-1:0]] <= din_i;
                wptr <= wptr + 1'b1;
            end

        end           
        
    end

endmodule

