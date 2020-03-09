# frequencyCounterReader
Python script to read and plot results from an HP/Agilent 53181a frequency counter using pyserial over RS-232.
Scrolling plot using Matplotlib.
Probably works with other models that communicate over RS-232
Tested with HP/Agilent 53181a

Note: This seems to work best with the Qt backend. Set this in an IPython console with
  %matplotlib qt
