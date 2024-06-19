import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import logging
import sys
import time
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img
from tensorflow.lite.python.interpreter import Interpreter
from sklearn.utils import shuffle

# 로그 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 모델 및 데이터 파일 경로
model_path = r"C:\github\Data\Puang_modelV5\model_unquant.tflite"
npy_file_path = r"C:\github\Data\final_files\p1data.npy"

# TensorFlow Lite 모델 로드
interpreter = Interpreter(model_path)
interpreter.allocate_tensors()

# 입력 및 출력 텐서 정보 가져오기
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# npy 파일 로드
with open(npy_file_path, 'rb') as infile:
    test_images = np.load(infile)
    test_labels = np.load(infile)

yourid = 20224531
test_images, test_labels = shuffle(test_images, test_labels, random_state=yourid)

total_images = len(test_images)
logging.info(f'npy 파일 로드 완료: 총 {total_images}개의 이미지')

# 모델 입력 크기 가져오기
input_shape = input_details[0]['shape'][1:4]

# puang 확률 기준 설정
puang_threshold = 0.3  

# 이미지 분류 및 puang 이미지 저장
puang_images = []
probabilities = []
start_time = time.time()

for i, image in enumerate(test_images):
    # 이미지 리사이즈
    img = array_to_img(image)
    img = img.resize(input_shape[:2])
    image = img_to_array(img) / 255.0  # 픽셀 값을 [0, 1] 사이로 스케일링
    image = np.expand_dims(image, axis=0)  # 모델 입력에 맞게 차원 확장

    # TensorFlow Lite 모델로 예측
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]['index'])[0]

    if prediction[10] >= puang_threshold:  # puang 확률이 기준 이상인 경우
        puang_images.append(image[0])
        probabilities.append(prediction[10])  # puang 확률 저장
    
    # 진행 상황 표시
    percent_complete = (i + 1) / total_images * 100
    elapsed_time = time.time() - start_time
    if (i + 1) % 10 == 0:  # 10개마다 업데이트
        print(f'\r진행 상황: {percent_complete:.2f}% ({i + 1}/{total_images}), 경과 시간: {elapsed_time:.2f}초', end='')
        sys.stdout.flush()

print()  # 진행 상황 표시를 완료한 후 줄 바꿈

# puang 이미지 플롯
if puang_images:
    sorted_indices = np.argsort(probabilities)[::-1]  # 확률 내림차순으로 정렬
    top_indices = sorted_indices[:100]  # 상위 100개 인덱스

    plt.figure(figsize=(10, 10))
    for j, idx in enumerate(top_indices):
        plt.subplot(10, 10, j + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(array_to_img(puang_images[idx]))
    plt.show()
else:
    logging.info('puang으로 분류된 이미지가 없습니다.')

logging.info(f'총 {len(puang_images)}개의 puang 이미지가 분류되었습니다.')
