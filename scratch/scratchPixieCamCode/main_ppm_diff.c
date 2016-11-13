#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <errno.h>
#include "cc3.h"

// Program written by Yanfei and Carlos 

void capture_ppm(FILE *fp);
void subtract2_ppm(FILE *fp, FILE *fp1, FILE *fp2);

int main(void) {
  int i;
  int result;
  FILE *f, *f_background, *f_diff;
  bool light_on = true;
  char filename[16];
  char file_diff_name[16];

  cc3_uart_init (0,
		 CC3_UART_RATE_115200,
		 CC3_UART_MODE_8N1,
		 CC3_UART_BINMODE_TEXT);

  cc3_camera_init ();

  // use MMC
  cc3_filesystem_init ();

  cc3_camera_set_resolution(CC3_CAMERA_RESOLUTION_HIGH);
  cc3_timer_wait_ms(1000);
  

  // Capture the background image
  
  f_background = fopen("c:/background.ppm", "w");
  capture_ppm(f_background);
  fclose(f_background);

  printf( "A new background image has been created and saved \n");
  
  
  cc3_timer_wait_ms(3000);
  

  while(true){ 
   
    snprintf(filename, 16, "c:/img%.5d.ppm", i);
    // print file of the capture image to stderr 
    fprintf(stderr,"%s ", filename);
    fflush(stderr);
    f = fopen(filename, "w");
	
	// open the difference file
	snprintf(file_diff_name, 16, "c:/dif%.5d.ppm", i);
    f_diff = fopen(file_diff_name, "w");
	
	// open the background file
	f_background = fopen("c:/background.ppm", "r");
	
    subtract2_ppm(f, f_background, f_diff);

	// close all of the ppm files
    result = fclose(f);
    if (result) {
      perror("second fclose failed");
    }
    fprintf(stderr, "\r\n");
	
	result = fclose(f_background);
    if (result) {
      perror("background fclose failed");
    }
    fprintf(stderr, "\r\n");

	result = fclose(f_diff);
    if (result) {
      perror("diff fclose failed");
    }
    fprintf(stderr, "\r\n");

    i++;
  }
  return 0;
}

void capture_ppm(FILE *f)
{
  uint32_t x, y;
  uint32_t size_x, size_y;

  cc3_pixbuf_load ();
  uint8_t *row = cc3_malloc_rows(1);

  size_x = cc3_g_pixbuf_frame.width;
  size_y = cc3_g_pixbuf_frame.height;

  fprintf(f,"P6\n%d %d\n255\n",size_x,size_y );

  for (y = 0; y < size_y; y++) {
    cc3_pixbuf_read_rows(row, 1);
    for (x = 0; x < size_x * 3U; x++) {
      uint8_t p = row[x];
      if (fputc(p, f) == EOF) {
	  perror("fputc failed");
      }
    }
    
  }
  free(row);
}


void subtract2_ppm(FILE *f, FILE *f_background, FILE *f_diff)
{
  uint32_t x, y;
  uint32_t size_x, size_y;
  uint8_t p, p_background, p_diff;
  cc3_pixbuf_load ();
  uint8_t *row = cc3_malloc_rows(1);
  

  size_x = cc3_g_pixbuf_frame.width;
  size_y = cc3_g_pixbuf_frame.height;

  // Write header files
  fprintf(f,"P6\n%d %d\n255\n",size_x,size_y );
  fprintf(f_diff,"P6\n%d %d\n255\n",size_x,size_y );
  
  // Skip the header of the background file
  while (fgetc(f_background)!='\n');
  while (fgetc(f_background)!='\n');
  while (fgetc(f_background)!='\n');
  
  
  for (y = 0; y < size_y; y++) {
    cc3_pixbuf_read_rows(row, 1);
    for (x = 0; x < size_x * 3U; x++) {    
	  // Read background and live pixel
	  p_background=fgetc(f_background);
	  p = row[x];
	  if (p_background < p)
		p_diff = p - p_background;
		else
		p_diff = p_background - p;
      if (fputc(p, f) == EOF) {
	  perror("fputc failed in substract2_ppm");
	  
	  
	  if (fputc(p_diff, f_diff) == EOF) {
	  perror("fputc diff failed");
      }
	}
	
  }
  free(row);
}
