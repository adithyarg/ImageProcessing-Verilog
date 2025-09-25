`timescale 1ns / 1ps

module tb_convolution();
  // Image size
  parameter IMG_WIDTH  = 128;
  parameter IMG_HEIGHT = 128;
  localparam integer IMG_SIZE = IMG_WIDTH * IMG_HEIGHT;

  // kernel_mem: 9 pixels packed per entry (9*24 = 216 bits)
  reg [215:0] kernel_mem [0:IMG_SIZE-1];
  reg [23:0] p [0:8];
  
  // declare all integers here
  integer i, op, j;
  integer r_acc, g_acc, b_acc;
  integer tmp;
  integer gx, gy, k;
  integer gray_p [0:8];   // grayscale 3×3 neighborhood

  reg [23:0] pix_out;

  // Files for output
  integer f_blur, f_motion_blur, f_sharpen, f_sobel_edge, f_emboss, f_outline;

  initial begin
    // load kernel neighborhood memory
    $readmemh("kernel_input.mem", kernel_mem);

    // open output files
    f_blur        = $fopen("blur.mem", "w");
    f_motion_blur = $fopen("motion_blur.mem", "w");
    f_sharpen     = $fopen("sharpen.mem", "w");
    f_sobel_edge  = $fopen("sobel_edge.mem", "w");
    f_emboss      = $fopen("emboss.mem", "w");
    f_outline     = $fopen("outline.mem", "w");

    // iterate over all pixels
    for (i = 0; i < IMG_SIZE; i = i + 1) begin
      // unpack neighborhood
      for (j = 0; j < 9; j = j + 1) begin
        p[j] = kernel_mem[i][j*24 +: 24];
      end

      // ----- 1. Blur -----
      r_acc = 0; g_acc = 0; b_acc = 0;
      for (j = 0; j < 9; j = j + 1) begin
        r_acc = r_acc + p[j][23:16];
        g_acc = g_acc + p[j][15:8];
        b_acc = b_acc + p[j][7:0];
      end
      pix_out = {r_acc/9, g_acc/9, b_acc/9};
      $fwrite(f_blur, "%06x\n", pix_out);

      // ----- 2. Motion Blur -----
      r_acc = (p[0][23:16] + p[4][23:16] + p[8][23:16]) / 3;
      g_acc = (p[0][15:8]  + p[4][15:8]  + p[8][15:8])  / 3;
      b_acc = (p[0][7:0]   + p[4][7:0]   + p[8][7:0])   / 3;
      pix_out = {r_acc, g_acc, b_acc};
      $fwrite(f_motion_blur, "%06x\n", pix_out);

      // ----- 3. Sharpen -----
      r_acc = -p[0][23:16] - p[1][23:16] - p[2][23:16]
              -p[3][23:16] + 9*p[4][23:16] - p[5][23:16]
              -p[6][23:16] - p[7][23:16] - p[8][23:16];
      g_acc = -p[0][15:8] - p[1][15:8] - p[2][15:8]
              -p[3][15:8] + 9*p[4][15:8] - p[5][15:8]
              -p[6][15:8] - p[7][15:8] - p[8][15:8];
      b_acc = -p[0][7:0] - p[1][7:0] - p[2][7:0]
              -p[3][7:0] + 9*p[4][7:0] - p[5][7:0]
              -p[6][7:0] - p[7][7:0] - p[8][7:0];
      pix_out = {clip(r_acc), clip(g_acc), clip(b_acc)};
      $fwrite(f_sharpen, "%06x\n", pix_out);

      // ----- 4. Sobel Edge Detection -----
      // grayscale neighborhood
      for (j=0; j<9; j=j+1) begin
        gray_p[j] = (p[j][23:16] + p[j][15:8] + p[j][7:0]) / 3;
      end

      gx = -gray_p[0] - 2*gray_p[3] - gray_p[6] +
             gray_p[2] + 2*gray_p[5] + gray_p[8];
      gy = -gray_p[0] - 2*gray_p[1] - gray_p[2] +
             gray_p[6] + 2*gray_p[7] + gray_p[8];
      tmp = (gx < 0 ? -gx : gx) + (gy < 0 ? -gy : gy);
      if (tmp > 255) tmp = 255;
      pix_out = {tmp[7:0], tmp[7:0], tmp[7:0]};
      $fwrite(f_sobel_edge, "%06x\n", pix_out);

      // ----- 5. Emboss -----
      r_acc = (-p[0][23:16] - p[1][23:16] - p[2][23:16]
               -p[3][23:16] + p[5][23:16]
               +p[6][23:16] + p[7][23:16] + p[8][23:16]) + 128;
      g_acc = (-p[0][15:8] - p[1][15:8] - p[2][15:8]
               -p[3][15:8] + p[5][15:8]
               +p[6][15:8] + p[7][15:8] + p[8][15:8]) + 128;
      b_acc = (-p[0][7:0] - p[1][7:0] - p[2][7:0]
               -p[3][7:0] + p[5][7:0]
               +p[6][7:0] + p[7][7:0] + p[8][7:0]) + 128;
      pix_out = {clip(r_acc), clip(g_acc), clip(b_acc)};
      $fwrite(f_emboss, "%06x\n", pix_out);

      // ----- 6. Outline -----
      r_acc = -p[0][23:16] - p[1][23:16] - p[2][23:16]
              -p[3][23:16] + 8*p[4][23:16] - p[5][23:16]
              -p[6][23:16] - p[7][23:16] - p[8][23:16];
      g_acc = -p[0][15:8] - p[1][15:8] - p[2][15:8]
              -p[3][15:8] + 8*p[4][15:8] - p[5][15:8]
              -p[6][15:8] - p[7][15:8] - p[8][15:8];
      b_acc = -p[0][7:0] - p[1][7:0] - p[2][7:0]
              -p[3][7:0] + 8*p[4][7:0] - p[5][7:0]
              -p[6][7:0] - p[7][7:0] - p[8][7:0];
      pix_out = {clip(r_acc), clip(g_acc), clip(b_acc)};
      $fwrite(f_outline, "%06x\n", pix_out);

    end // for (i)

    // close files
    $fclose(f_blur);
    $fclose(f_motion_blur);
    $fclose(f_sharpen);
    $fclose(f_sobel_edge);
    $fclose(f_emboss);
    $fclose(f_outline);

    $finish;
  end

  // helper function: clip to 0..255
  function [7:0] clip;
    input integer val;
    begin
      if (val < 0) clip = 0;
      else if (val > 255) clip = 255;
      else clip = val[7:0];
    end
  endfunction

endmodule
