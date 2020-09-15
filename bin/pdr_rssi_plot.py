import os
import sys
import math
import matplotlib.pyplot as plot
import numpy as np

def main():


      rssi_pdr_table_two_dot_four = {
                  -97:    0.0000,  # this value is not from experiment
                  -96:    0.1494,
                  -95:    0.2340,
                  -94:    0.4071,
                  # <-- 50% PDR is here, at RSSI=-93.6
                  -93:    0.6359,
                  -92:    0.6866,
                  -91:    0.7476,
                  -90:    0.8603,
                  -89:    0.8702,
                  -88:    0.9324,
                  -87:    0.9427,
                  -86:    0.9562,
                  -85:    0.9611,
                  -84:    0.9739,
                  -83:    0.9745,
                  -82:    0.9844,
                  -81:    0.9854,
                  -80:    0.9903,
                  -79:    1.0000,  # this value is not from experiment
      }

      plot.grid(True, which="both")
      arr = list(rssi_pdr_table_two_dot_four.keys())
      rssi = arr[::-1]
      plot.semilogy(rssi, list(rssi_pdr_table_two_dot_four.values()) )

      plot.ylim([0,1.1])

      plot.xlim([-97,-80])

      plot.title('PDR x RSSI')

      plot.xlabel('RSSI')

      plot.ylabel('PDR')

      plot.show()


if __name__ == '__main__':

      main()