import cv2
import numpy as np


class LineDrawer:
    def __init__(self, modelTr, first_down_point, scrimmage_point, model, hsv_values):
        print('Drawing...')
        self._modelTr = modelTr
        self._point = first_down_point
        self._scrimmage_point = scrimmage_point
        self._model = model
        self._hsv_low, self._hsv_high = hsv_values

        self.homogeneous_point = np.array([self._point], dtype=np.float32)
        self.point_in_model = cv2.perspectiveTransform(np.array([self.homogeneous_point]), self._modelTr.H)

        self.homogeneous_point_scrimmage = np.array([self._scrimmage_point], dtype=np.float32)
        self.scrimmage_point_in_model = cv2.perspectiveTransform(np.array([self.homogeneous_point_scrimmage]),
                                                                 self._modelTr.H)

        self.model_image = np.copy(self._modelTr.model)
        print('sp:'+str(self._scrimmage_point))
        print('sp_m:'+str(self.scrimmage_point_in_model))
        print('dp:' + str(self._point))
        print('dp_m:' + str(self.point_in_model))
        cv2.circle(self.model_image, (self.scrimmage_point_in_model[0][0][0], self.scrimmage_point_in_model[0][0][1]), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(self.model_image, (self.point_in_model[0][0][0], self.point_in_model[0][0][1]), 10, (0, 0, 255), cv2.FILLED)
        cv2.imshow('model_plus_line_points', self.model_image)
        cv2.waitKey()

    def draw_line(self, image, pt1, pt2, pt3, pt4):
        print(pt1,pt2,pt3,pt4)
        height, width, depth = image.shape
        line_mask = np.zeros((height, width), np.uint8)
        line_image = np.zeros((height, width, 3), np.uint8)
        cv2.line(line_image, pt1, pt2, (43, 124, 220), 10)
        cv2.line(line_mask, pt1, pt2, (255, 255, 255), 3)

        scrimmage_line_mask = np.zeros((height, width), np.uint8)
        scrimmage_line_image = np.zeros((height, width, 3), np.uint8)
        cv2.line(scrimmage_line_image, pt3, pt4, (131, 65, 20), 10)
        cv2.line(scrimmage_line_mask, pt3, pt4, (255, 255, 255), 3)

        #field_mask = self.mask_builder(image, 38, 88, 34, 101, 0, 174)
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        field_mask = cv2.inRange(hsv_image, self._hsv_low, self._hsv_high)
        field_mask_inv = cv2.bitwise_not(field_mask)

        #cv2.imshow('field_mask', field_mask)
        #cv2.imshow('field_mask_inv', field_mask_inv)
        #cv2.waitKey()

        lineToDraw = cv2.addWeighted(line_mask, 1, field_mask_inv, -1, 0)
        lineToDraw_inv = cv2.bitwise_not(lineToDraw)
        line = cv2.bitwise_and(line_image, line_image, mask=lineToDraw)

        scrimmage_lineToDraw = cv2.addWeighted(scrimmage_line_mask, 1, field_mask_inv, -1, 0)
        scrimmage_lineToDraw_inv = cv2.bitwise_not(scrimmage_lineToDraw)

        scrimmage_line = cv2.bitwise_and(scrimmage_line_image, scrimmage_line_image, mask=scrimmage_lineToDraw)

        both_lines = cv2.bitwise_or(line,scrimmage_line)
        both_field = cv2.bitwise_and(lineToDraw_inv,scrimmage_lineToDraw_inv)
        field = cv2.bitwise_and(image, image, mask=both_field)
        output = cv2.addWeighted(both_lines, 1, field, 1, 0)

        #cv2.imshow('both_lines', both_lines)
        #cv2.imshow('both_field', both_field)
        #cv2.imshow('output', output)
        #cv2.waitKey()

        return output

    def applyHomographyToPoint(self, frame, H):
        start_line = (self.point_in_model[0][0][0].astype(int), self._model.params['upperLineY'])
        end_line = (self.point_in_model[0][0][0].astype(int), self._model.params['lowerLineY'])

        start_line_scrimmage = (self.scrimmage_point_in_model[0][0][0].astype(int), self._model.params['upperLineY'])
        end_line_scrimmage = (self.scrimmage_point_in_model[0][0][0].astype(int), self._model.params['lowerLineY'])

        res, inv_H = cv2.invert(H)
        model_line_points = np.array([start_line, end_line], dtype=np.float32)
        model_line_scrimmage_points = np.array([start_line_scrimmage, end_line_scrimmage], dtype=np.float32)

        field_line_points = cv2.perspectiveTransform(np.array([model_line_points]), inv_H)
        field_scrimmage_line_points = cv2.perspectiveTransform(np.array([model_line_scrimmage_points]), inv_H)

        start_line_field = (field_line_points[0][0][0], field_line_points[0][0][1])
        end_line_field = (field_line_points[0][1][0], field_line_points[0][1][1])

        start_scrimmage_line_field = (field_scrimmage_line_points[0][0][0], field_scrimmage_line_points[0][0][1])
        end_scrimmage_line_field = (field_scrimmage_line_points[0][1][0], field_scrimmage_line_points[0][1][1])
        return self.draw_line(frame, start_line_field, end_line_field, start_scrimmage_line_field,
                              end_scrimmage_line_field)

    def desenhalinha(self, frame, H):
        start_line = (self.point_in_model[0][0][0].astype(int), self._model.params['upperLineY'])
        end_line = (self.point_in_model[0][0][0].astype(int), self._model.params['lowerLineY'])

        md = self.model_image
        print("startl: %s" % (start_line,))
        print("endll: %s" % (end_line,))
        cv2.line(md,start_line,end_line,(255, 0, 0),2)
        cv2.imshow('linha_modelo', md)
        ldst=self._modelTr.dst
        cv2.line(ldst, start_line, end_line, (255, 0, 0), 2)
        cv2.imshow('modelo tudo', ldst)


        res, inv_H = cv2.invert(H)
        model_line_points = np.array([start_line, end_line], dtype=np.float32)
        field_line_points = cv2.perspectiveTransform(np.array([model_line_points]), inv_H)
        start_line_field = (field_line_points[0][0][0], field_line_points[0][0][1])
        end_line_field = (field_line_points[0][1][0], field_line_points[0][1][1])

        print("startl_field: %s" % (start_line_field,))
        print("endll_field: %s" % (end_line_field,))
        #frm=frame
        #cv2.line(frm, start_line_field, end_line_field, (0, 0, 255), 2)
        #cv2.imshow('linha_field', frm)
        #cv2.waitKey()

        height, width, depth = frame.shape
        line_mask = np.zeros((height, width), np.uint8)
        line_image = np.zeros((height, width, 3), np.uint8)
        cv2.line(line_image, start_line_field, end_line_field, (0, 0, 255), 4)
        cv2.line(line_mask, start_line_field, end_line_field, (255, 255, 255), 3)



        # field_mask = self.mask_builder(image, 38, 88, 34, 101, 0, 174)
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        field_mask = cv2.inRange(hsv_image, self._hsv_low, self._hsv_high)
        field_mask_inv = cv2.bitwise_not(field_mask)

        cv2.imshow('field_mask', field_mask)
        cv2.imshow('field_mask_inv', field_mask_inv)
        #cv2.waitKey()

        lineToDraw = cv2.addWeighted(line_mask, 1, field_mask_inv, -1, 0)
        lineToDraw_inv = cv2.bitwise_not(lineToDraw)
        line = cv2.bitwise_and(line_image, line_image, mask=lineToDraw)






        field = cv2.bitwise_and(frame, frame, mask=lineToDraw_inv)
        output = cv2.addWeighted(line, 1, field, 1, 0)

        #cv2.imshow('line', line)
        #cv2.imshow('field', field)
        #cv2.imshow('output', output)
        #cv2.waitKey()

        return output

