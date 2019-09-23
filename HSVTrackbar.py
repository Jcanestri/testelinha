import cv2
import numpy as np
from VideoPlayer import VideoPlayer


class HSVPicker():
    def __init__(self, frame):
        self._image = frame
        cv2.namedWindow('image')
        cv2.namedWindow('tbimg')
        cv2.namedWindow('blur')


    def nothing(self, x):
        pass

    def getHSVMask(self):
        mask=None
        # easy assigments
        hh = 'Hue High'
        hl = 'Hue Low'
        sh = 'Saturation High'
        sl = 'Saturation Low'
        vh = 'Value High'
        vl = 'Value Low'
        blur = 'Blur'

        cv2.createTrackbar(hl, 'image', 10, 179, self.nothing)
        cv2.createTrackbar(hh, 'image', 33, 179, self.nothing)
        cv2.createTrackbar(sl, 'image', 45, 255, self.nothing)
        cv2.createTrackbar(sh, 'image', 207, 255, self.nothing)
        cv2.createTrackbar(vl, 'image', 234, 255, self.nothing)
        cv2.createTrackbar(vh, 'image', 255, 255, self.nothing)
        cv2.createTrackbar(blur, 'image', 3, 60, self.nothing)

        while (1):

            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break






            # get current positions of four trackbars
            hul = cv2.getTrackbarPos(hl, 'image')
            huh = cv2.getTrackbarPos(hh, 'image')
            sal = cv2.getTrackbarPos(sl, 'image')
            sah = cv2.getTrackbarPos(sh, 'image')
            val = cv2.getTrackbarPos(vl, 'image')
            vah = cv2.getTrackbarPos(vh, 'image')
            blurv = cv2.getTrackbarPos(blur, 'image')
            resto = blurv % 2
            if resto == 0:
                blurv = blurv + 1
            blurimg = cv2.GaussianBlur(self._image, (blurv, blurv), 0)
            cv2.imshow('blur', blurimg)

            hsv = cv2.cvtColor(blurimg, cv2.COLOR_BGR2HSV)




            HSVLOW = np.array([hul, sal, val])
            HSVHIGH = np.array([huh, sah, vah])

            # apply the range on a mask
            mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
            res = cv2.bitwise_and(self._image, self._image, mask=mask)
            #cv2.imshow('image', res)
            cv2.imshow('tbimg', res)
        return HSVLOW, HSVHIGH, blurv
