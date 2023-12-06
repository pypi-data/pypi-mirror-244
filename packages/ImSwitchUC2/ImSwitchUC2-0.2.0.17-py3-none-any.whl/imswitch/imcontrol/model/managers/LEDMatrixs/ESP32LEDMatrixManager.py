from imswitch.imcommon.model import initLogger
from .LEDMatrixManager import LEDMatrixManager
import numpy as np

import uc2rest

class ESP32LEDMatrixManager(LEDMatrixManager):
    """ LEDMatrixManager for controlling LEDs and LEDMatrixs connected to an
    ESP32 exposing a REST API
    Each LEDMatrixManager instance controls one LED.

    Manager properties:

    - ``rs232device`` -- name of the defined rs232 communication channel
      through which the communication should take place
    - ``channel_index`` -- LEDMatrix channel (A to H)
    """

    def __init__(self, LEDMatrixInfo, name, **lowLevelManagers):
        self.__logger = initLogger(self, instanceName=name)
        self.power = 0
        self.I_max = 255
        self.setEnabled = False
        self.intensity=0

        try:
            self.Nx = LEDMatrixInfo.managerProperties['Nx']
            self.Ny = LEDMatrixInfo.managerProperties['Ny']
        except:
            self.Nx = 8
            self.Ny = 8
            
        # extract the special patterns from the user defined file
        try:
            self.SpecialPattern1 = LEDMatrixInfo.managerProperties['SpecialPattern1']
            self.SpecialPattern2 = LEDMatrixInfo.managerProperties['SpecialPattern2']
        except:
            self.SpecialPattern1 = 0
            self.SpecialPattern2 = 0
            
        self.NLeds = self.Nx*self.Ny

        self._rs232manager = lowLevelManagers['rs232sManager'][
            LEDMatrixInfo.managerProperties['rs232device']
        ]
       
        # initialize the LEDMatrix device that holds all necessary states^
        self.mLEDmatrix = self._rs232manager._esp32.led

        super().__init__(LEDMatrixInfo, name, isBinary=False, valueUnits='mW', valueDecimals=0)

    def setIndividualPattern(self, pattern, getReturn=False):
        r = self.mLEDmatrix.send_LEDMatrix_array(pattern, getReturn = getReturn)
        return r
                
    def setAll(self, state=(0,0,0), intensity=None):
        # dealing with on or off,
        # intensity is adjjusting the global value
        self.mLEDmatrix.setAll(state, intensity)

    def setPattern(self, pattern):
        self.mLEDmatrix.pattern(pattern)
    
    def getPattern(self):
        return self.mLEDmatrix.getPattern()

    def setEnabled(self, enabled):
        """Turn on (N) or off (F) LEDMatrix emission"""
        self.setEnabled = enabled
        
    def setLEDSingle(self, indexled=0, state=(0,0,0)):
        """Handles output power.
        Sends a RS232 command to the LEDMatrix specifying the new intensity.
        """
        self.mLEDmatrix.setSingle(indexled, state=state)

    def setLEDIntensity(self, intensity=(0,0,0)):
        self.mLEDmatrix.setIntensity(intensity)



# Copyright (C) 2020-2023 ImSwitch developers
# This file is part of ImSwitch.
#
# ImSwitch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ImSwitch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
