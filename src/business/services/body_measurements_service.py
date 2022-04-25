from unittest import result
import numpy as np
import cv2
import mediapipe as mp
from tensorflow.keras.models import load_model

from fastapi import Depends, UploadFile
from persistence.repositories.repositories import BodyMeasurementsRepository
from business.handlers.service_exception import ServiceException

mp_face_detection = mp.solutions.face_detection

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


means_2=[77.10342857142857,87.78114285714283,100.40971428571429,99.62799999999999,32.92171428571427,26.45257142857143,84.41028571428566,35.84742857142857,18.828,95.19142857142853,34.81257142857143,37.500571428571455,36.33142857142859,29.982285714285698,15.495999999999999,55.835428571428565,12.517142857142854,27.756571428571416,143.1519999999999,57.643999999999984,37.187428571428576,95.06514285714285,80.87542857142856,102.95257142857142,76.75885714285711]

std_devs_2=[4.427070554506816,6.825378508904789,6.706367486234776,5.298900775187941,2.9993653406402205,2.6817350950212506,4.572256092999075,1.8772631443066485,2.2717060276061387,6.280135231200638,2.3024379169150135,2.741643460954592,2.713860912225075,2.718809625547026,0.9422008961657978,3.121173835013742,1.1277293110559723,2.4600602072544717,6.251858022670714,4.928961560913772,3.2417112187262704,5.290230299089592,7.499250668642371,6.975044326006372,4.522957894084187]

def getNeck(w,h,results,img):
  y_s=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y*h))
  y_m=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT].y*h))
  return int((y_s+y_m)*(1-0.1)/2) 

def getNeck2(w,h,results,img):
  y_s=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y*h))
  y_m=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT].y*h))
  return int((y_s+y_m)/2) 

def getMidtermPointRight(w,h,results,img):
  y_w=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y*h))
  x_w=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x*w))
  x_f=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x*w))
  return int((x_w+x_f)/2),int(y_w*(1+0.03)) 

def getMidtermPointLeft(w,h,results,img):
  y_w=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y*h))
  x_w=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x*w))
  x_f=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x*w))
  return int((x_w+x_f)/2),int(y_w*(1+0.03)) 

def getBotPointRight(w,h,results,img):
  y_a=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y*h))
  x_a=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x*w))
  return int((x_a+(w/2))/2),int(y_a*(1+0.01))

def getBotPointLeft(w,h,results,img):
  y_a=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y*h))
  x_a=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x*w))
  return int((x_a+(w/2))/2),int(y_a*(1+0.01))

def getBotPointLeft2(w,h,results,img):
  y_a=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y*h))
  x_a=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x*w))
  return int(y_a*(1+0.01))  

def process_person_body(image,value) -> any:
    BG_COLOR = (255, 255, 255)
    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5) as pose:
    
      #image = cv2.imread(file)
      image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = pose.process(image_rgb)
      h,w,_=image.shape

      if results.pose_landmarks is not None:

        #mp_drawing.draw_landmarks(image, results.pose_landmarks,
        #                          mp_pose.POSE_CONNECTIONS)

        image_no_bg = image.copy()
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        image_no_bg = np.where(condition, image_no_bg, bg_image)

        if value=="1":
          neck_y=getNeck(w,h,results,image_no_bg)

          mid_right_x,mid_right_y=getMidtermPointRight(w,h,results,image_no_bg)

          mid_left_x,mid_left_y=getMidtermPointLeft(w,h,results,image_no_bg)

          bot_right_x,bot_right_y=getBotPointRight(w,h,results,image_no_bg)

          bot_left_x,bot_left_y=getBotPointLeft(w,h,results,image_no_bg)  

          image_no_bg[:neck_y][image_no_bg[:neck_y]!=255]=255

          image_no_bg[mid_right_y:,:mid_right_x][image_no_bg[mid_right_y:,:mid_right_x]!=255]=255

          image_no_bg[mid_left_y:,mid_left_x:][image_no_bg[mid_left_y:,mid_left_x:]!=255]=255

          image_no_bg[bot_right_y:,:bot_right_x][image_no_bg[bot_right_y:,:bot_right_x]!=255]=255

          image_no_bg[bot_left_y:,bot_left_x:][image_no_bg[bot_left_y:,bot_left_x:]!=255]=255      

        if value=="2":
          neck_y=getNeck2(w,h,results,image_no_bg)
          
          bot_left_y=getBotPointLeft2(w,h,results,image_no_bg)  

          image_no_bg[:neck_y][image_no_bg[:neck_y]!=255]=255
          
          image_no_bg[bot_left_y:][image_no_bg[bot_left_y:]!=255]=255      

        image_no_bg[image_no_bg!=255]=0
        return image_no_bg



class BodyMeasurementsService():
    def __init__(self, repository: BodyMeasurementsRepository = Depends(BodyMeasurementsRepository)) -> None:
        self.repository = repository

    async def get_all(self) -> list:
        result = await self.repository.get_all()
        return result

    async def take_measurements(self, file: UploadFile,file2: UploadFile, height):
        content_1 = await file.read()
        
        bytes_as_np_array_1 = np.frombuffer(content_1, dtype=np.uint8)
        image_1 = cv2.imdecode(bytes_as_np_array_1, cv2.IMREAD_COLOR)

        with  mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB))
            if not results.detections:
                raise ServiceException("No hay personas", 10005)

        content_2 = await file2.read()
        bytes_as_np_array_2 = np.frombuffer(content_2, dtype=np.uint8)
        image_2 = cv2.imdecode(bytes_as_np_array_2, cv2.IMREAD_COLOR)

        with  mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB))
            if not results.detections:
                raise ServiceException("No hay personas", 10005)
        
        # pre procesamiento 

        #Para predecir nuestros datos de TEST, cargamos primero el modelo entrenado

        x1_l,x2_l,x3_l=[],[],[]
        answer=[]

        x1 = process_person_body(image_1,"1")   
        x1 = cv2.resize(x1, (500,250))  

        x2 = process_person_body(image_2,"2")   
        x2 = cv2.resize(x2, (500,250))

        l_m = load_model('D:/UPC/2022-01/Taller de Proyecto Profesional/Semana 05/PatronesMedidasService/src/domain/MeasurementVPredict.h5')

        x1_l.append(x1)
        x2_l.append(x2)
        x3_l.append(height)

        pdt=l_m.predict([np.array(x1_l),np.array(x2_l),np.array(x3_l)])

        #answer.append((pdt[0].flatten()*std_devs_2[0]) + means_2[0])

        #prediccion con CNN

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

                
