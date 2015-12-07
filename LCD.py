# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast			- Pentometer
# 4 : RS (Register Select)	- GPIO7 (26)
# 5 : R/W (Read Write)		- GROUND THIS PIN
# 6 : Enable or Strobe		- GPIO8 (24)
# 7 : Data Bit 0		- NOT USED
# 8 : Data Bit 1		- NOT USED
# 9 : Data Bit 2		- NOT USED
# 10: Data Bit 3		- NOT USED
# 11: Data Bit 4		- GPIO25 (22)
# 12: Data Bit 5		- GPIO24 (18)
# 13: Data Bit 6		- GPIO23 (16)
# 14: Data Bit 7		- GPIO18 (12)
# 15: 5V
# 16: GND
 
#import
import RPi.GPIO as GPIO
import time
import subprocess
 
# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
 
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
 
def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
 
  # Initialise display
  print "initialize display"
  lcd_init()

  cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
  
 
  while True:

    ipaddr = run_cmd(cmd)
 
    # Send text
    print "sending text"
    lcd_string("Zero Pi",LCD_LINE_1)
    lcd_string("IP %s" % (ipaddr),LCD_LINE_2) 
    time.sleep(3)
 
    # Send text
    lcd_string("IP %s" % (ipaddr),LCD_LINE_1)
    lcd_string(time.strftime("%m/%d/%Y %H:%M"),LCD_LINE_2) 
    time.sleep(3)
 
    lcd_string(time.strftime("%m/%d/%Y %H:%M"),LCD_LINE_1)
    lcd_string("Brian Spencer",LCD_LINE_2) 
    time.sleep(3)
 
    lcd_string("Brian Spencer",LCD_LINE_1)
    lcd_string("brianspencer.me",LCD_LINE_2) 
    time.sleep(3)

    lcd_string("brianspencer.me",LCD_LINE_1)
    lcd_string("Zero Pi",LCD_LINE_2)
    time.sleep(3)

def run_cmd(cmd):
  p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
  output = p.communicate()[0]
  return output
 
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
