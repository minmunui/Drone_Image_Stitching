import sys
import os
import time
import threading
import cv2
import numpy as np

data_dir = 'data'
image_dir = 'src1'
dst_dir = 'dst'

cv2.ocl.setUseOpenCL(False)

base_path = os.getcwd()
data_path = os.path.join(base_path, data_dir)
image_path = os.path.join(data_path, image_dir)
print(f"image directory : {image_path}")

file_names = os.listdir(image_path)

print(f"detected [{len(file_names)}] files : {file_names}")

images = []

for name in file_names:
    img_path = os.path.join(image_path, name)
    print(f"loading : {img_path}")
    img = cv2.imread(img_path)
    images.append(img)

is_end = False


def time_counting():
    counting = 0
    while not is_end:
        print(f"stitching... {counting} second")
        time.sleep(10)
        counting += 10

thread = threading.Thread(target=time_counting)
# thread.start()
stitcher = cv2.Stitcher.create()
status, stitched_image = stitcher.stitch(images)

if status == cv2.Stitcher_OK:
    # 스티칭 성공
    cv2.imshow('Stitched Image', stitched_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 여백 확인
    gray_stitched = cv2.cvtColor(stitched_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_stitched, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 여백이 있다면 알파 채널을 0으로 설정하여 투명하게 만들기
    if len(contours) > 0:
        contour = contours[0]
        mask = np.zeros_like(gray_stitched)
        cv2.drawContours(mask, [contour], 0, (255), -1)

        # 알파 채널 추가
        stitched_image_with_alpha = cv2.cvtColor(stitched_image, cv2.COLOR_BGR2BGRA)
        stitched_image_with_alpha[mask == 0, 3] = 0  # 알파 채널을 0으로 설정하여 투명하게 만들기

        cv2.imshow('Transparent Image', stitched_image_with_alpha)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
else:
    print("스티칭 실패")

is_end = True

dst_path = os.path.join(data_path, dst_dir)
print(f'Stitched image will be saved : {dst_path}')
cv2.imwrite(f'{image_dir}.jpg', stitched_image)
