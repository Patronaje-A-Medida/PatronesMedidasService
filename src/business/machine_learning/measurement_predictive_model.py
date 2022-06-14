import numpy as np
import tensorflow as tf

from business.machine_learning.image_processing import *


BASE_FILENAME_DIR = './src/domain/models/machine_learning/model_measure_'
LITE_MODELS = [
    'Across_Back.tflite',
    'Across_Front.tflite',
    'Bicep_Circ.tflite',
    'Bust_Circ.tflite',
    'Bust_to_Bust.tflite',
    'Calf_Circ.tflite',
    'CrotchLength_Back.tflite',
    'CrotchLength_Front.tflite',
    'Hip_2_Circ.tflite',
    'Hip_2_Height.tflite',
    'HIP_Circ.tflite',
    'Hip_Height.tflite',
    'Inseam.tflite',
    'Knee_Circ.tflite',
    'NaturalWAIST_Circ.tflite',
    'NECK_Height.tflite',
    'NeckBase_Circ.tflite',
    'Shoulder_Length.tflite',
    'Shoulder_to_Wrist.tflite',
    'SideNeck_to_Bust.tflite',
    'Thigh_Circ.tflite',
    'TrouserWAIST_Circ.tflite',
    'TrouserWaist_Height_Back.tflite',
    'TrouserWaist_Height_Front.tflite',
    'Wrist_Circ.tflite'
]



class MeasurementPredictiveModel():
    def __init__(self) -> None:
        pass
    
    def predict(self, image_frontal: any) -> dict:
        image = process_body_person(image_frontal)
        image = image * 1./255
        x1 = []
        x1.append(image)
        x1 = np.array(x1, dtype=np.float32)
        x1 = np.reshape(x1, (1,480,200,1))
        measurements = dict()

        for file_name in LITE_MODELS:
            model_path = BASE_FILENAME_DIR + file_name
            interpreter = tf.lite.Interpreter(model_path=model_path)
            interpreter.allocate_tensors()

            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            #input_shape = input_details[0]['shape']
            input_data = np.array(x1)
            interpreter.set_tensor(input_details[0]['index'], input_data)

            interpreter.invoke()

            output_data = interpreter.get_tensor(output_details[0]['index'])
            key = file_name.split('.')[0]
            measure = output_data[0][0] * 100
            measurements[key] = measure
        
        return measurements
        