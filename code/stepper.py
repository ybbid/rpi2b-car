# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24
StepPins = [18,23,24,25]

# Set all pins as output
for pin in StepPins:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

# Define advanced sequence
# as shown in manufacturers datasheet
SeqSinglePhase = [[1,0,0,0],
		  [0,1,0,0],
		  [0,0,1,0],
		  [0,0,0,1]]

SeqFullDualPhase = [[1,1,0,0],
	            [0,1,1,0],
	            [0,0,1,1],
	            [1,0,0,1]]

SeqHalfStep = [[1,0,0,0],
	       [1,1,0,0],
	       [0,1,0,0],
	       [0,1,1,0],
	       [0,0,1,0],
	       [0,0,1,1],
	       [0,0,0,1],
	       [1,0,0,1]]
       
# Select Sequence Mode
Seq = SeqSinglePhase

# 1 clockwise, -1 anti-clockwise
StepDir = 1 

StepCount = len(Seq)

# Read wait time from command line
if len(sys.argv)>1:
  WaitTime = int(sys.argv[1])/float(1000)
else:
  WaitTime = 10/float(1000)

# Initialise variables
if (StepDir == 1):
  StepCounter = 0
else:
  StepCounter = StepCount - 1

# Start main loop
Count = 1
while True:
  # Quit after 1 rotation 360 degree
  if (Count > 512 * StepCount):
    break
  print "Count %i" % Count
  Count += 1

  print "Step: %i" %(StepCounter)
  for pin in range(0, 4):
    xpin = StepPins[pin]
#    print pin
    if Seq[StepCounter][pin]!=0:
      print " %i *" %(pin)
      GPIO.output(xpin, True)
    else:
      print " %i -" %(pin)
      GPIO.output(xpin, False)

  StepCounter += StepDir

  # If we reach the end of the sequence
  # start again
  if (StepCounter>=StepCount):
    StepCounter = 0
  if (StepCounter<0):
    StepCounter = StepCount - 1

  # Wait before moving on
  time.sleep(WaitTime)