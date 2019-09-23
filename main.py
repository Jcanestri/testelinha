import cv2
import numpy as np
from VideoPlayer import VideoPlayer
from VideoWriter import VideoWriter
from LineDrawer import LineDrawer
from Model import Model
from LinePicker import LinePicker
from ModelTransformer import ModelTransformer
from HSVTrackbar import HSVPicker

if __name__ == '__main__':

    vp = VideoPlayer('resources/video/field1/cliphd4.mp4') #inicializa com o caminho
    frames = vp.extract_frames() # abre o arquivo e retorna um vetor com os frames
    frames_with_line = [] # cria vetor com frames com linha
    field_lines_mask = [] # mascara das linhas do campo

    lp = LinePicker(frames[1]) #abre o frame de número 1 para a escolha dos pontos (fp,sc) -apertar enter

    #copia e imprime os pontos
    first_point = lp.first_down_point
    scrimmage = lp.scrimmage_point
    print(first_point, scrimmage)


    HSV_LOW, HSV_HIGH, BLUR = HSVPicker(frames[1]).getHSVMask()  #abre o seletor de filtros pro HSV e retorna os limites da máscara

    modelImage = cv2.imread('resources/model/model_cfl.png') #o arquivo do modelo do campo
    model = Model(modelImage)  #aqui dentro tem o ymin e ymax do modelo... corrigir isso depois
    modelTr = ModelTransformer(model, frames[1], [HSV_LOW, HSV_HIGH], True) #cria a matriz de transformação (PS: NÃO POR PONTOS COLINEARES!!!!)

    ld = LineDrawer(modelTr, first_point, scrimmage, model, [HSV_LOW, HSV_HIGH])#transforma os pontos

    start_index = 1
    all_homo = list()
    nframes = frames[start_index:]
    print('Número total de frames: ' + str(len(nframes)))
    frames_with_line=[]
    for index, frame in enumerate(nframes):
        print('Processando frame ' + str(index) + ' :')
        modelTr.novo_frame(frame)
        output = ld.desenhalinha(frame, modelTr.H)
        frames_with_line.append(output)
        #cv2.imshow('lines', output)

    cv2.destroyAllWindows()
    vw = VideoWriter('footage_line_test',frames_with_line)