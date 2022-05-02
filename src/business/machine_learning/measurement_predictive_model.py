import numpy as np

from keras.models import load_model
from keras.applications import imagenet_utils

from business.machine_learning.body_landmarks import *


means_2=[77.10342857142857,87.78114285714283,100.40971428571429,99.62799999999999,32.92171428571427,26.45257142857143,84.41028571428566,35.84742857142857,18.828,95.19142857142853,34.81257142857143,37.500571428571455,36.33142857142859,29.982285714285698,15.495999999999999,55.835428571428565,12.517142857142854,27.756571428571416,143.1519999999999,57.643999999999984,37.187428571428576,95.06514285714285,80.87542857142856,102.95257142857142,76.75885714285711]
std_devs_2=[4.427070554506816,6.825378508904789,6.706367486234776,5.298900775187941,2.9993653406402205,2.6817350950212506,4.572256092999075,1.8772631443066485,2.2717060276061387,6.280135231200638,2.3024379169150135,2.741643460954592,2.713860912225075,2.718809625547026,0.9422008961657978,3.121173835013742,1.1277293110559723,2.4600602072544717,6.251858022670714,4.928961560913772,3.2417112187262704,5.290230299089592,7.499250668642371,6.975044326006372,4.522957894084187]


class MeasurementPredictiveModel():
    def __init__(self) -> None:
        self.__means_2 = means_2
        self.__std_devs_2 = std_devs_2
        #self.__l_m = load_model('./src/domain/models/machine_learning/MeasurementVPredict.h5', custom_objects={'imagenet_utils': imagenet_utils})
    
    def predict(self, image_frontal: any, image_lateral: any, height: float) -> list:
        x1_l,x2_l,x3_l=[],[],[]
        answer=[]

        x1 = process_person_body(image_frontal,"1")   
        x1 = cv2.resize(x1, (500,250))  

        x2 = process_person_body(image_lateral,"2")   
        x2 = cv2.resize(x2, (500,250))

        l_m = load_model('./src/domain/models/machine_learning/MeasurementVPredict.h5', custom_objects={'imagenet_utils': imagenet_utils})

        x1_l.append(x1)
        x2_l.append(x2)
        x3_l.append(height)

        pdt=l_m.predict([np.array(x1_l),np.array(x2_l),np.array(x3_l)])

        answer.append(((pdt[0].flatten()*std_devs_2[0]) + means_2[0])[0]) 
        answer.append(((pdt[1].flatten()*std_devs_2[1]) + means_2[1])[0]) 
        answer.append(((pdt[2].flatten()*std_devs_2[2]) + means_2[2])[0]) 
        answer.append(((pdt[3].flatten()*std_devs_2[3]) + means_2[3])[0]) 
        answer.append(((pdt[4].flatten()*std_devs_2[4]) + means_2[4])[0]) 
        answer.append(((pdt[5].flatten()*std_devs_2[5]) + means_2[5])[0]) 
        answer.append(((pdt[6].flatten()*std_devs_2[6]) + means_2[6])[0]) 
        answer.append(((pdt[7].flatten()*std_devs_2[7]) + means_2[7])[0]) 
        answer.append(((pdt[8].flatten()*std_devs_2[8]) + means_2[8])[0]) 
        answer.append(((pdt[9].flatten()*std_devs_2[9]) + means_2[9])[0]) 
        answer.append(((pdt[10].flatten()*std_devs_2[10]) + means_2[10])[0]) 
        answer.append(((pdt[11].flatten()*std_devs_2[11]) + means_2[11])[0]) 
        answer.append(((pdt[12].flatten()*std_devs_2[12]) + means_2[12])[0]) 
        answer.append(((pdt[13].flatten()*std_devs_2[13]) + means_2[13])[0]) 
        answer.append(((pdt[14].flatten()*std_devs_2[14]) + means_2[14])[0]) 
        answer.append(((pdt[15].flatten()*std_devs_2[15]) + means_2[15])[0]) 
        answer.append(((pdt[16].flatten()*std_devs_2[16]) + means_2[16])[0]) 
        answer.append(((pdt[17].flatten()*std_devs_2[17]) + means_2[17])[0]) 
        answer.append(((pdt[18].flatten()*std_devs_2[18]) + means_2[18])[0]) 
        answer.append(((pdt[19].flatten()*std_devs_2[19]) + means_2[19])[0]) 
        answer.append(((pdt[20].flatten()*std_devs_2[20]) + means_2[20])[0]) 
        answer.append(((pdt[21].flatten()*std_devs_2[21]) + means_2[21])[0]) 
        answer.append(((pdt[22].flatten()*std_devs_2[22]) + means_2[22])[0]) 
        answer.append(((pdt[23].flatten()*std_devs_2[23]) + means_2[23])[0]) 
        answer.append(((pdt[24].flatten()*std_devs_2[24]) + means_2[24])[0])  

        # retornar el output de la CNN   
        return answer