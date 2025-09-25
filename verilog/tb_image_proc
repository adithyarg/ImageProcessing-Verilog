`timescale 1ns/1ps

module tb_image_proc;
  parameter integer WIDTH  = 128;   // <-- update to match your image width
  parameter integer HEIGHT = 128;   // <-- update to match your image height
  localparam integer TOTAL = WIDTH * HEIGHT;

  reg [23:0] img_mem [0:TOTAL-1];
  reg [23:0] pix_in;
  reg [23:0] pix_out;
  reg [7:0] r, g, b, gray;
  reg [23:0] processed_mem [0:TOTAL-1];

  integer i, op;

  initial begin
    // Load the input image (already .mem from Python script)
    $readmemh("C:/Users/adith/OneDrive/code/ImageProc-Verilog/images/image.mem", img_mem);

    // Loop through all 8 operations
    for (op = 1; op <= 8; op = op + 1) begin
      for (i = 0; i < TOTAL; i = i + 1) begin
        pix_in = img_mem[i];
        r = pix_in[23:16];
        g = pix_in[15:8];
        b = pix_in[7:0];

        case (op)
          1: pix_out = ~pix_in & 24'hFFFFFF;    // invert

          2: begin                              // grayscale
               gray = (r + g + b) / 3;
               pix_out = {gray, gray, gray};
             end

          3: begin                              // brightness increase
               r = (r + 50 > 255) ? 255 : r + 50;
               g = (g + 50 > 255) ? 255 : g + 50;
               b = (b + 50 > 255) ? 255 : b + 50;
               pix_out = {r,g,b};
             end

          4: begin                              // brightness decrease
               r = (r < 50) ? 0 : r - 50;
               g = (g < 50) ? 0 : g - 50;
               b = (b < 50) ? 0 : b - 50;
               pix_out = {r,g,b};
             end

          5: pix_out = {r, 8'h00, 8'h00};       // red filter
          6: pix_out = {8'h00, g, 8'h00};       // green filter
          7: pix_out = {8'h00, 8'h00, b};       // blue filter
          8: pix_out = pix_in;                  // original (no change)

          default: pix_out = pix_in;
        endcase

        processed_mem[i] = pix_out;
      end

      // Save result of each operation with unique file
      case(op)
        1: $writememh("you_dir/1.Invert.mem", processed_mem);
        2: $writememh("you_dir/2.Grayscale.mem", processed_mem);
        3: $writememh("you_dir/3.BrightnessInc.mem", processed_mem);
        4: $writememh("you_dir/4.BrightnessDec.mem", processed_mem);
        5: $writememh("you_dir/5.RedFilter.mem", processed_mem);
        6: $writememh("you_dir/6.GreenFilter.mem", processed_mem);
        7: $writememh("you_dir/7.BlueFilter.mem", processed_mem);
        8: $writememh("you_dir/8.Original.mem", processed_mem);
      endcase

      $display("✅ Operation %0d complete", op);
    end

    $display("🎯 All operations complete. Check your images/ folder.");
    $finish;
  end
endmodule
