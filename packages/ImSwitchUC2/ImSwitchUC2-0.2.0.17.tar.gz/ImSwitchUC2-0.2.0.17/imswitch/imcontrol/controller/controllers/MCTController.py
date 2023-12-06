
import os
import threading
from datetime import datetime
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.ndimage as ndi
import scipy.signal as signal
import skimage.transform as transform
import tifffile as tif

from imswitch.imcommon.framework import Signal, Thread, Worker, Mutex, Timer
from imswitch.imcommon.model import dirtools, initLogger, APIExport
from skimage.registration import phase_cross_correlation
from ..basecontrollers import ImConWidgetController
import imswitch

class MCTController(ImConWidgetController):
    """Linked to MCTWidget."""

    sigImageReceived = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = initLogger(self)

        # mct parameters
        self.nImagesTaken = 0
        self.timePeriod = 60 # seconds
        self.zStackEnabled = False
        self.zStackMin = 0
        self.zStackMax = 0
        self.zStackStep = 0

        # xy
        self.xyScanEnabled = False
        self.xScanMin = 0
        self.xScanMax = 0
        self.xScanStep = 0
        self.yScanMin = 0
        self.yScanMax = 0
        self.yScanStep = 0

        # store old values
        self.Laser1ValueOld = 0
        self.Laser2ValueOld = 0
        self.LEDValueOld = 0

        self.Laser1Value = 0
        self.Laser2Value = 0
        self.LEDValue = 0
        self.MCTFilename = ""

        self.pixelsize=(10,1,1) # zxy


        # connect XY Stagescanning live update  https://github.com/napari/napari/issues/1110
        self.sigImageReceived.connect(self.displayImage)

        # autofocus related
        self.isAutofocusRunning = False
        self._commChannel.sigAutoFocusRunning.connect(self.setAutoFocusIsRunning)

        # select detectors
        allDetectorNames = self._master.detectorsManager.getAllDeviceNames()
        self.detector = self._master.detectorsManager[allDetectorNames[0]]

        # select lasers
        allLaserNames = self._master.lasersManager.getAllDeviceNames()
        self.lasers = []
        for iDevice in allLaserNames:
            if iDevice.lower().find("laser")>=0 or iDevice.lower().find("led"):
                self.lasers.append(self._master.lasersManager[iDevice])

        # TODO: misleading we have LEDs and LED Matrices here...
        self.leds = []
        for iDevice in allLaserNames:
            if iDevice.find("LED")>=0:
                self.leds.append(self._master.lasersManager[iDevice])

        '''
        if len(self._master.LEDMatrixsManager.getAllDeviceNames())>0:
            self.illu = self._master.LEDMatrixsManager[self._master.LEDMatrixsManager.getAllDeviceNames()[0]]
        else:
            self.illu = []
        '''
        # select stage
        self.stages = self._master.positionersManager[self._master.positionersManager.getAllDeviceNames()[0]]

        self.isMCTrunning = False

        # Connect MCTWidget signals
        if not imswitch.IS_HEADLESS:
            self._widget.mctStartButton.clicked.connect(self.startMCT)
            self._widget.mctStopButton.clicked.connect(self.stopMCT)
            self._widget.mctShowLastButton.clicked.connect(self.showLast)

            self._widget.sigSliderLaser1ValueChanged.connect(self.valueLaser1Changed)
            self._widget.sigSliderLaser2ValueChanged.connect(self.valueLaser2Changed)
            self._widget.sigSliderLEDValueChanged.connect(self.valueLEDChanged)

            self._widget.mctShowLastButton.setEnabled(False)

            # setup gui limits
            if len(self.lasers) >= 1: self._widget.sliderLaser1.setMaximum(self.lasers[0]._LaserManager__valueRangeMax)
            if len(self.lasers) >= 2: self._widget.sliderLaser2.setMaximum(self.lasers[1]._LaserManager__valueRangeMax)
            if len(self.leds) >= 1: self._widget.sliderLED.setMaximum(self.leds[0]._LaserManager__valueRangeMax)

            # setup gui text
            if len(self.lasers) >= 1: self._widget.sliderLaser1.setMaximum(self.lasers[0]._LaserManager__valueRangeMax)
            if len(self.lasers) >= 2: self._widget.sliderLaser2.setMaximum(self.lasers[1]._LaserManager__valueRangeMax)
            if len(self.leds) >= 1: self._widget.sliderLED.setMaximum(self.leds[0]._LaserManager__valueRangeMax)

            # suggest limits for tiled scan with 20% overlay
            try:
                self.pixelSize = self.detector.pixelSizeUm
                overlap = 0.8 # %20 overlap between ROIs
                self.Nx, self.Ny = self.detector._camera.SensorWidth, self.detector._camera.SensorHeight
                self.optDx = int(self.Nx* self.pixelSize[1]*overlap) # dx
                self.optDy = int(self.Ny* self.pixelSize[2]*overlap) # dy
                self._widget.mctValueXsteps.setText(str(self.optDx))
                self._widget.mctValueYsteps.setText(str(self.optDy))

            except Exception as e:
                self._logger.error(e)


    def startMCT(self):
        # initilaze setup
        # this is not a thread!
        self._widget.mctStartButton.setEnabled(False)

        # don't show any message
        #self._master.UC2ConfigManager.setDebug(False)

        # start the timelapse
        if not self.isMCTrunning and (self.Laser1Value>0 or self.Laser2Value>0 or self.LEDValue>0):
            self.nImagesTaken = 0
            self._widget.setnImagesTaken("Starting timelapse...")
            self.switchOffIllumination()

            # get parameters from GUI
            self.zStackMin, self.zStackMax, self.zStackStep, self.zStackEnabled = self._widget.getZStackValues()
            self.xScanMin, self.xScanMax, self.xScanStep, self.yScanMin, self.yScanMax, self.yScanStep, self.xyScanEnabled = self._widget.getXYScanValues()

            self.timePeriod, self.nImagesToCapture = self._widget.getTimelapseValues()
            self.MCTFilename = self._widget.getFilename()
            self.MCTDate = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")

            # store old values for later
            if len(self.lasers)>0:
                self.Laser1ValueOld = self.lasers[0].power
            if len(self.lasers)>1:
                self.Laser2ValueOld = self.lasers[1].power
            if len(self.leds)>0:
                self.LEDValueOld = self.leds[0].power

            # reserve space for the stack
            self._widget.mctShowLastButton.setEnabled(False)

            # start the timelapse - otherwise we have to wait for the first run after timePeriod to take place..
            self.takeTimelapse(self.timePeriod)

            '''
            self.timer = mTimer(self.timePeriod, self.takeTimelapse)
            self.timer.start()
            '''

        else:
            self.isMCTrunning = False
            self._widget.mctStartButton.setEnabled(True)


    def stopMCT(self):
        self.isMCTrunning = False

        self._widget.setnImagesTaken("Stopping timelapse...")

        self._widget.mctStartButton.setEnabled(True)

        # go back to initial position
        try:
            if self.xyScanEnabled:
                self.stages.move(value=(self.initialPosition[0], self.initialPosition[1]), axis="XY", is_absolute=True, is_blocking=True)
        except:
            pass

        # delete any existing timer
        try:
            del self.timer
        except:
            pass

        # delete any existing thread
        try:
            del self.MCTThread
        except:
            pass

        self._widget.setnImagesTaken("Done wit timelapse...")

        # store old values for later
        if len(self.lasers)>0:
            self.lasers[0].setValue(self.Laser1ValueOld)
        if len(self.lasers)>1:
            self.lasers[1].setValue(self.Laser2ValueOld)
        if len(self.leds)>0:
            self.leds[0].setValue(self.LEDValueOld)

    def showLast(self, isCleanStack=False):
        #  isCleanStack=False => subtract backgroudn or not
        if hasattr(self, "LastStackLaser1ArrayLast"):
            try:
                #subtract background and normalize stack
                if isCleanStack: LastStackLaser1ArrayLast = self.cleanStack(self.LastStackLaser1ArrayLast)
                else: LastStackLaser1ArrayLast = self.LastStackLaser1ArrayLast
                self._widget.setImage(LastStackLaser1ArrayLast, colormap="green", name="GFP",pixelsize=self.pixelsize)
            except  Exception as e:
                self._logger.error(e)

        if hasattr(self, "LastStackLaser2ArrayLast"):
            try:
                if isCleanStack: LastStackLaser2ArrayLast = self.cleanStack(self.LastStackLaser2ArrayLast)
                else: LastStackLaser2ArrayLast = self.LastStackLaser2ArrayLast
                self._widget.setImage(LastStackLaser2ArrayLast, colormap="red", name="SiR",pixelsize=self.pixelsize)
            except Exception as e:
                self._logger.error(e)

        if hasattr(self, "LastStackLEDArrayLast"):
            try:
                if isCleanStack: LastStackLEDArrayLast = self.cleanStack(self.LastStackLEDArrayLast)
                else: LastStackLEDArrayLast = self.LastStackLEDArrayLast
                self._widget.setImage(LastStackLEDArrayLast, colormap="gray", name="Brightfield",pixelsize=self.pixelsize)
            except  Exception as e:
                self._logger.error(e)

    def cleanStack(self, input):
        import NanoImagingPack as nip
        mBackground = nip.gaussf(np.mean(input,0),10)
        moutput = input/mBackground
        mFluctuations = np.mean(moutput, (1,2))
        moutput /= np.expand_dims(np.expand_dims(mFluctuations,-1),-1)
        return np.uint8(moutput)

    def displayStack(self, im):
        """ Displays the image in the view. """
        self._widget.setImage(im)

    def takeTimelapse(self, tperiod):
        # this is called periodically by the timer
        if not self.isMCTrunning:
            try:
                # make sure there is no exisiting thrad
                del self.MCTThread
            except:
                pass

            # this should decouple the hardware-related actions from the GUI
            self.isMCTrunning = True
            self.MCTThread = threading.Thread(target=self.takeTimelapseThread, args=(tperiod, ), daemon=True)
            self.MCTThread.start()

    def doAutofocus(self, params, timeout=10):
        self._logger.info("Autofocusing...")
        self._widget.setnImagesTaken("Autofocusing...")
        self._commChannel.sigAutoFocus.emit(int(params["valueRange"]), int(params["valueSteps"]))
        self.isAutofocusRunning = True

        while self.isAutofocusRunning:
            time.sleep(0.1)
            t0 = time.time()
            if not self.isAutofocusRunning or time.time()-t0>timeout:
                self._logger.info("Autofocusing done.")
                return


    def takeTimelapseThread(self, tperiod = 1):
        # this wil run i nthe background
        self.timeLast = 0
        image1 = None
        # get current position
        currentPositions = self.stages.getPosition()
        self.initialPosition = (currentPositions["X"], currentPositions["Y"])
        self.initialPositionZ = currentPositions["Z"]

        # run as long as the MCT is active
        while(self.isMCTrunning):

            # stop measurement once done
            if self.nImagesTaken >= self.nImagesToCapture:
                self.isMCTrunning = False
                self._logger.debug("Done with timelapse")
                self._widget.mctStartButton.setEnabled(True)
                break

            # initialize a run
            if time.time() - self.timeLast >= (tperiod):

                # run an event
                self.timeLast = time.time() # makes sure that the period is measured from launch to launch
                self._logger.debug("Take image")
                # reserve and free space for displayed stacks
                self.LastStackLaser1 = []
                self.LastStackLaser2 = []
                self.LastStackLED = []


                # set  speed
                self.stages.setSpeed(speed=10000, axis="X")
                self.stages.setSpeed(speed=10000, axis="Y")
                self.stages.setSpeed(speed=10000, axis="Z")

                # ensure motors are enabled
                #self.stages.enalbeMotors(enable=True)

                try:
                    # want to do autofocus?
                    autofocusParams = self._widget.getAutofocusValues()

                    if self._widget.isAutofocus() and np.mod(self.nImagesTaken, int(autofocusParams['valuePeriod'])) == 0:
                        self._widget.setnImagesTaken("Autofocusing...")
                        # turn on illuimination
                        if autofocusParams['illuMethod']=="Laser1":
                            self.lasers[0].setValue(self.Laser1Value)
                            self.lasers[0].setEnabled(True)
                            time.sleep(.05)
                        elif autofocusParams['illuMethod']=="Laser2":
                            self.lasers[1].setValue(self.Laser2Value)
                            self.lasers[1].setEnabled(True)
                            time.sleep(.05)
                        elif autofocusParams['illuMethod']=="LED":
                            self.leds[0].setValue(self.LEDValue)
                            self.leds[0].setEnabled(True)
                            time.sleep(.05)

                        self.doAutofocus(autofocusParams)
                        self.switchOffIllumination()
                    # acquire one xyzc scan
                    self.acquireScan(timestamp=self.nImagesTaken)

                    # update GUI
                    self._widget.setnImagesTaken(self.nImagesTaken)

                    # sneak images into arrays for displaying stack
                    if self.zStackEnabled and not self.xyScanEnabled:
                        self.LastStackLaser1ArrayLast = np.array(self.LastStackLaser1)
                        self.LastStackLaser2ArrayLast = np.array(self.LastStackLaser2)
                        self.LastStackLEDArrayLast = np.array(self.LastStackLED)

                        self._widget.mctShowLastButton.setEnabled(True)

                        ''' here we can try to compute the drift '''

                    if False and not self.xyScanEnabled:
                        # treat images
                        imageStack = self.LastStackLaser2 # FIXME: Hardcoded
                        imageStack = self.LastStackLED # FIXME: Hardcoded

                        driftCorrectionDownScaleFactor = 5
                        driftCorrectionCropSize = 800
                        iShift = [0,0]
                        imageList = []

                        # convert to list if necessary
                        if type(imageStack)!=list or len(imageStack)<2:
                            imageStack = list(imageStack)

                        # image processing
                        for iImage in imageStack:
                            if len(iImage.shape)>2:
                                # if RGB => make mono
                                iImage = np.mean(iImage, -1)
                            image = self.crop_center(iImage, driftCorrectionCropSize)
                            image = self.downscale_image(image, driftCorrectionDownScaleFactor)
                            imageList.append(image)

                        # remove background
                        imageList = np.array(imageList)
                        if len(imageList.shape)<3:
                            imageList = np.expand_dims(imageList,0)
                        imageList = imageList/ndi.filters.gaussian_filter(np.mean(imageList,0), 10)

                        # Find max focus
                        bestFocus = 0
                        bestFocusIndex = 0
                        for index, image in enumerate(imageList):
                            # remove high frequencies
                            imagearraygf = ndi.filters.gaussian_filter(image, 3)

                            # compute focus metric
                            focusValue = np.mean(ndi.filters.laplace(imagearraygf))
                            if focusValue > bestFocus:
                                bestFocus = focusValue
                                bestFocusIndex = index

                        # Align the images
                        image2 = np.std(imageList, (0))

                        #image2 = scipy.ndimage.gaussian_filter(image2, sigma=10)
                        if self.nImagesTaken > 0:
                            shift, error, diffphase = phase_cross_correlation(image1, image2)
                            iShift += (shift)

                            # Shift image2 to align with image1
                            image = imageList[bestFocusIndex]
                            #aligned_image = np.roll(image, int(iShift[1]), axis=1)
                            #aligned_image = np.roll(aligned_image,int(iShift[0]), axis=0)
                            self.stages.move(value=(self.initialPosition[0]+shift[1], self.initialPosition[1]+shift[0]), axis="XY", is_absolute=True, is_blocking=True)

                        image1 = image2.copy()

                    #save values
                    #make sure not to have too large travelrange after last (e.g. initial position + 2*shift))

                    #increase iterator
                    self.nImagesTaken += 1



                except Exception as e:
                    self._logger.error("Thread closes with Error: "+str(e))
                    # close the controller ina nice way
                    pass

            # pause to not overwhelm the CPU
            time.sleep(0.1)



    def acquireScan(self, timestamp=0):
        fileExtension = 'tif'

        # precompute steps for xy scan
        # snake scan
        if self.xyScanEnabled:
            xyScanStepsAbsolute = []
            xyScanIndices = []
            # we snake over y
            fwdpath = np.arange(self.yScanMin, self.yScanMax, self.yScanStep)
            bwdpath = np.flip(fwdpath)
            # we increase linearly over x
            for indexX, ix in enumerate(np.arange(self.xScanMin, self.xScanMax, self.xScanStep)):
                if indexX%2==0:
                    for indexY, iy in enumerate(fwdpath):
                        xyScanStepsAbsolute.append([ix, iy])
                else:
                    for indexY, iy in enumerate(bwdpath):
                        xyScanStepsAbsolute.append([ix, iy])

            # reserve space for tiled image
            downScaleFactor = 4
            nTilesX = int(np.ceil((self.xScanMax-self.xScanMin)/self.xScanStep))
            nTilesY = int(np.ceil((self.yScanMax-self.yScanMin)/self.yScanStep))
            imageDimensions = self.detector.getLatestFrame().shape
            imageDimensionsDownscaled = (imageDimensions[1]//downScaleFactor, imageDimensions[0]//downScaleFactor) # Y/X
            tiledImageDimensions = (nTilesX*imageDimensions[1]//downScaleFactor, nTilesY*imageDimensions[0]//downScaleFactor)
            self.tiledImage = np.zeros(tiledImageDimensions)

        else:
            xyScanStepsAbsolute = [[0,0]]
            self.xScanMin = 0
            self.xScanMax = 0
            self.yScanMin = 0
            self.yScanMax = 0


        # precompute steps for z scan
        if self.zStackEnabled:
            zStepsAbsolute =  np.arange(self.zStackMin, self.zStackMax, self.zStackStep) + self.initialPositionZ
        else:
            zStepsAbsolute = [self.initialPositionZ]


        # in case something is not connected we want to reconnect!
        # TODO: This should go into some function outside the MCT!!!
        #if not ("IDENTIFIER_NAME" in self._master.UC2ConfigManager.ESP32.state.get_state() and self._master.UC2ConfigManager.ESP32.state.get_state()["IDENTIFIER_NAME"] == "uc2-esp"):
        #    mThread = threading.Thread(target=self._master.UC2ConfigManager.initSerial)
        #    mThread.start()
        #    mThread.join()

        # initialize xyz coordinates
        if self.xyScanEnabled:
            self.stages.move(value=(self.xScanMin+self.initialPosition[0],self.yScanMin+self.initialPosition[1]), axis="XY", is_absolute=True, is_blocking=True)

        # initialize iterator
        imageIndex = 0
        self._widget.gridLayer = None
        # iterate over all xy coordinates iteratively

        # if we only have one light-source, keep it on during scanning
        '''
        if (self.Laser1Value>0 + self.Laser2Value>0 + self.LEDValue>0)>1:
            turnOffIlluInBetween = True
        else:
            turnOffIlluInBetween = False
        '''
        turnOffIlluInBetween=True
        for ipos, iXYPos in enumerate(xyScanStepsAbsolute):
            if not self.isMCTrunning:
                break
            # move to xy position is necessary
            if self.xyScanEnabled:
                self.stages.move(value=(iXYPos[0]+self.initialPosition[0],iXYPos[1]+self.initialPosition[1]), axis="XY", is_absolute=True, is_blocking=True)
            # measure framenumber and check if it has been renewed after stage has stopped => avoid motion blur!
            nFrameSyncWait = 5
            '''
            if hasattr(self.detector, "getFrameNumber"):
                frameNumber = self.detector.getFrameNumber()
            else:
                frameNumber = -nFrameSyncWait
            '''


            # perform a z-stack
            for iZ in zStepsAbsolute:
                # move to each position
                if self.zStackEnabled:
                    self.stages.move(value=iZ, axis="Z", is_absolute=True, is_blocking=True)
                    time.sleep(self.tUnshake) # unshake

                # capture image for every illumination
                if self.Laser1Value>0 and len(self.lasers)>0:
                    filePath = self.getSaveFilePath(date=self.MCTDate,
                                timestamp=timestamp,
                                filename=f'{self.MCTFilename}_Laser1_i_{imageIndex}_Z_{iZ}_X_{xyScanStepsAbsolute[ipos][0]}_Y_{xyScanStepsAbsolute[ipos][1]}',
                                extension=fileExtension)
                    self.lasers[0].setValue(self.Laser1Value)
                    self.lasers[0].setEnabled(True)
                    time.sleep(.05)
                    time.sleep(self.tWait)
                    lastFrame = self.detector.getLatestFrame()
                    # wait for frame after next frame to appear. Avoid motion blurring
                    #while self.detector.getFrameNumber()<(frameNumber+nFrameSyncWait):time.sleep(0.05)
                    #TODO: USE self._master.recordingManager.snap()
                    tif.imwrite(filePath, lastFrame, append=True)
                    if turnOffIlluInBetween: self.lasers[0].setEnabled(False)
                    self.LastStackLaser1.append(lastFrame.copy())

                if self.Laser2Value>0 and len(self.lasers)>0:
                    filePath = self.getSaveFilePath(date=self.MCTDate,
                                timestamp=timestamp,
                                filename=f'{self.MCTFilename}_Laser2_i_{imageIndex}_Z_{iZ}_X_{xyScanStepsAbsolute[ipos][0]}_Y_{xyScanStepsAbsolute[ipos][1]}',
                                extension=fileExtension)
                    self.lasers[1].setValue(self.Laser2Value)
                    self.lasers[1].setEnabled(True)
                    time.sleep(.05)
                    time.sleep(self.tWait)
                    lastFrame = self.detector.getLatestFrame()
                    tif.imwrite(filePath, lastFrame, append=True)
                    if turnOffIlluInBetween: self.lasers[1].setEnabled(False)
                    self.LastStackLaser2.append(lastFrame.copy())

                if self.LEDValue>0 and len(self.leds)>0:
                    filePath = self.getSaveFilePath(date=self.MCTDate,
                                timestamp=timestamp,
                                filename=f'{self.MCTFilename}_LED_i_{imageIndex}_Z_{iZ}_X_{xyScanStepsAbsolute[ipos][0]}_Y_{xyScanStepsAbsolute[ipos][1]}',
                                extension=fileExtension)
                    try:
                        if len(self.leds)>0:
                            self.leds[0].setValue(self.LEDValue)
                            self.leds[0].setEnabled(True)
                        time.sleep(.1)
                        time.sleep(self.tWait)
                        lastFrame = self.detector.getLatestFrame()
                        tif.imwrite(filePath, lastFrame, append=True)
                        if turnOffIlluInBetween: self.leds[0].setEnabled(False)
                        self.LastStackLED.append(lastFrame.copy())
                    except:
                        pass


                imageIndex += 1

            # reduce backlash => increase chance to endup at the same position
            if self.zStackEnabled:
                self.stages.move(value=(self.initialPositionZ), axis="Z", is_absolute=True, is_blocking=True)

            if self.xyScanEnabled:
                # lets try to visualize each slice in napari
                # def setImage(self, im, colormap="gray", name="", pixelsize=(1,1,1)):
                # construct the tiled image
                iX = int(np.floor((iXYPos[0]-self.xScanMin) // self.xScanStep))
                iY = int(np.floor((iXYPos[1]-self.yScanMin) // self.yScanStep))
                # handle rgb => turn to mono for now
                if len(lastFrame.shape)>2:
                    lastFrame = np.uint16(np.mean(lastFrame, 0))
                # add tile to large canvas
                lastFrameScaled = cv2.resize(lastFrame, None, fx = 1/downScaleFactor, fy = 1/downScaleFactor, interpolation = cv2.INTER_NEAREST)
                try:
                    self.tiledImage[int(iY*imageDimensionsDownscaled[1]):int(iY*imageDimensionsDownscaled[1]+imageDimensionsDownscaled[1]),
                        int(iX*imageDimensionsDownscaled[0]):int(iX*imageDimensionsDownscaled[0]+imageDimensionsDownscaled[0])] = lastFrameScaled
                except Exception as e:
                    self._logger.error(e)
                    self._logger.error("Failed to parse a frame into the tiledImage array")
                self.sigImageReceived.emit() # => displays image


        # initialize xy coordinates
        if self.xyScanEnabled:
            self.stages.move(value=(self.initialPosition[0], self.initialPosition[1]), axis="XY", is_absolute=True, is_blocking=True)
        if self.zStackEnabled:
            self.stages.move(value=(self.initialPositionZ), axis="Z", is_absolute=True, is_blocking=True)

        # ensure all illus are off
        self.switchOffIllumination()

        # disable motors to prevent overheating
        self._logger.debug("Setting enable to: "+str(self.stages.is_enabled))
        self.stages.enalbeMotors(enable=self.stages.is_enabled)

    def switchOffIllumination(self):
        # switch off all illu sources
        for lasers in self.lasers:
            if lasers.name.find("Laser")>-1:
                lasers.setEnabled(False)
                #lasers.setValue(0)
                time.sleep(0.1)
        if len(self.leds)>0:
            self.leds[0].setValue(0)
            #self.illu.setAll((0,0,0))

    def valueLaser1Changed(self, value):
        self.Laser1Value= value
        self._widget.mctLabelLaser1.setText('Intensity (Laser 1):'+str(value))
        if not self.lasers[0].enabled: self.lasers[0].setEnabled(1)
        if len(self.lasers)>0:self.lasers[0].setValue(self.Laser1Value)
        if self.lasers[1].power: self.lasers[1].setValue(0)
        if len(self.leds)>0 and self.leds[0].power: self.leds[0].setValue(0)

    def valueLaser2Changed(self, value):
        self.Laser2Value = value
        self._widget.mctLabelLaser2.setText('Intensity (Laser 2):'+str(value))
        if not self.lasers[1].enabled: self.lasers[1].setEnabled(1)
        if len(self.lasers)>1: self.lasers[1].setValue(self.Laser2Value)
        if self.lasers[0].power: self.lasers[0].setValue(0)
        if len(self.leds)>0 and self.leds[0].power: self.leds[0].setValue(0)

    def valueLEDChanged(self, value):
        self.LEDValue= value
        self._widget.mctLabelLED.setText('Intensity (LED):'+str(value))
        if len(self.leds) and not self.leds[0].enabled: self.leds[0].setEnabled(1)
        if len(self.leds): self.leds[0].setValue(self.LEDValue, getReturn=False)
        if len(self.lasers)>0: self.lasers[0].power: self.lasers[0].setValue(0)
        if len(self.lasers)>1: self.lasers[1].power: self.lasers[1].setValue(0)

    def __del__(self):
        self.imageComputationThread.quit()
        self.imageComputationThread.wait()

    def getSaveFilePath(self, date, timestamp, filename, extension):
        mFilename =  f"{date}_{filename}.{extension}"
        dirPath  = os.path.join(dirtools.UserFileDirs.Root, 'recordings', date, "t"+str(timestamp))

        newPath = os.path.join(dirPath,mFilename)

        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        return newPath

    def setAutoFocusIsRunning(self, isRunning):
        # this is set by the AutofocusController once the AF is finished/initiated
        self.isAutofocusRunning = isRunning

    def displayImage(self):
        # a bit weird, but we cannot update outside the main thread
        name = "tilescanning"
        self._widget.setImage(np.uint16(self.tiledImage), colormap="gray", name=name, pixelsize=(1,1), translation=(0,0))


    # helper functions
    def downscale_image(self, image, factor):
        # Downscale the image
        downscaled_image = transform.downscale_local_mean(image, (factor, factor))
        return downscaled_image

    def crop_center(self, image, size):
        # Get the dimensions of the image
        height, width = image.shape[:2]

        # Calculate the coordinates for cropping
        start_x = max(0, int((width - size) / 2))
        start_y = max(0, int((height - size) / 2))
        end_x = min(width, start_x + size)
        end_y = min(height, start_y + size)

        # Crop the image
        cropped_image = image[start_y:end_y, start_x:end_x]

        return cropped_image



class mTimer(object):
    def __init__(self, waittime, mFunc) -> None:
        self.waittime = waittime
        self.starttime = time.time()
        self.running = False
        self.isStop = False
        self.mFunc = mFunc

    def start(self):
        self.starttime = time.time()
        self.running = True

        ticker = threading.Event( daemon=True)
        self.waittimeLoop=0 # make sure first run runs immediately
        while not ticker.wait(self.waittimeLoop) and self.isStop==False:
            self.waittimeLoop = self.waittime
            self.mFunc()
        self.running = False

    def stop(self):
        self.running = False
        self.isStop = True


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
