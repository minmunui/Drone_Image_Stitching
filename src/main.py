# import cv2 as cv
# import utils
#
# img_name = 'src1.jpg'
#
# img = cv.imread(img_name)
# trim = utils.trim_black(img)
#
# file_name = img_name.split('.')[0]
#
# # 이미지 저장
# cv.imwrite(f'{file_name}_trim.jpg', trim)


import cv2
import numpy as np

# 이미지 로드
import cv2
import numpy as np

# 이미지와 알파 채널을 함께 로드
filename = 'src1.jpg'
image = cv2.imread(filename, cv2.COLOR_BGR2BGRA)
image_with_alpha = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
# image_with_alpha 보기

width, height = image.shape[:2]

for i in range(width):
    for j in range(height):
        r, g, b, a = image_with_alpha[i][j]
        if r == 0 and g == 0 and b == 0:
            image_with_alpha[i][j][3] = 0

# 새로운 이미지 생성, 검정색은 투명도가 0
dst_name = f'{filename.split(".")[0]}_trim.png'
print(f"dst_name : {dst_name}")
cv2.imwrite(dst_name, image_with_alpha)
# 결과 표시
# cv2.imshow('Original Image', image)
# cv2.imshow('Result', new_image)
# cv2.imwrite(f'{filename.split()[0]}_trim.png', new_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()