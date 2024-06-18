import numpy as np
from PIL import Image
import os

# 데이터 로드 
npy_file_path = r"C:\github\Data\final_files\p1data.npy"
images = np.load(npy_file_path)

# 저장 위치 
output_dir = r"C:\github\Data\final_files\images"
os.makedirs(output_dir, exist_ok=True)

# 이미지 데이터를 jpg 파일로 변환하여 저장
for i, img_array in enumerate(images):
    img = Image.fromarray(img_array.astype('uint8'))  
    img.save(os.path.join(output_dir, f'image_{i+1}.jpg'))  

print(f'Successfully saved {len(images)} images to {output_dir}')