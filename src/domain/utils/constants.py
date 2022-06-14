from enum import Enum

BASE_FILENAME_DIR = './src/domain/models/machine_learning/model_measure_'

LITE_MODELS = [
    BASE_FILENAME_DIR + 'Across_Back.tflite',
    BASE_FILENAME_DIR + 'Across_Front.tflite',
    BASE_FILENAME_DIR + 'Bicep_Circ.tflite',
    BASE_FILENAME_DIR + 'Busct_Circ.tflite',
    BASE_FILENAME_DIR + 'Bust_to_Bust.tflite',
    BASE_FILENAME_DIR + 'Calf_Circ.tflite',
    BASE_FILENAME_DIR + 'CrotchLength_Back.tflite',
    BASE_FILENAME_DIR + 'CrotchLength_Front.tflite',
    BASE_FILENAME_DIR + 'Hip_2_Circ.tflite',
    BASE_FILENAME_DIR + 'Hip_2_Height.tflite',
    BASE_FILENAME_DIR + 'HIP_Circ.tflite',
    BASE_FILENAME_DIR + 'Hip_Height.tflite',
    BASE_FILENAME_DIR + 'Inseam.tflite',
    BASE_FILENAME_DIR + 'Knee_Circ.tflite',
    BASE_FILENAME_DIR + 'NaturalWAIST_Circ.tflite',
    BASE_FILENAME_DIR + 'NECK_Height.tflite',
    BASE_FILENAME_DIR + 'NeckBase_Circ.tflite',
    BASE_FILENAME_DIR + 'Shoulder_Length.tflite',
    BASE_FILENAME_DIR + 'Shoulder_to_Wrist.tflite',
    BASE_FILENAME_DIR + 'SideNeck_to_Bust.tflite',
    BASE_FILENAME_DIR + 'Thigh_Circ.tflite',
    BASE_FILENAME_DIR + 'TrouserWAIST_Circ.tflite',
    BASE_FILENAME_DIR + 'TrouserWaist_Height_Back.tflite',
    BASE_FILENAME_DIR + 'TrouserWaist_Height_Front.tflite',
    BASE_FILENAME_DIR + 'Wrist_Circ.tflite'
]

class MeasuresEnum(Enum):
    Across_Back = 1
    Across_Front = 2
    Bicep_Circ = 3
    Bust_Circ = 4
    Bust_to_Bust = 5 
    Calf_Circ = 6
    CrotchLength_Back = 7
    CrotchLength_Front = 8
    Hip_2_Circ = 9
    Hip_2_Height = 10 
    HIP_Circ = 11
    Hip_Height = 12
    Inseam = 13
    Knee_Circ = 14 
    NaturalWAIST_Circ = 15
    NECK_Height = 16
    Shoulder_Length = 17
    Shoulder_to_Wrist = 18
    SideNeck_to_Bust = 19
    Thigh_Circ = 20
    TrouserWAIST_Circ = 21
    TrouserWaist_Height_Back = 22
    TrouserWaist_Height_Front = 23
    Wrist_Circ = 24
    NeckBase_Circ = 25
