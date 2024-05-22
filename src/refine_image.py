import os

import cv2


def remove_black_padding(image):
    """
    이미지의 검정색 여백을 제거합니다.
    :param image: 검정색 여백을 제거할 이미지
    :return: 검정색 여백이 제거된 이미지
    """
    # 이미지를 그레이 스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # binary thereshold로 검정색 여백 추출 (1보다 작은 값은 0으로, 1 이상의 값은 255로 설정)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    # image와 thresh를 곱하여 검정색 여백을 제거합니다.
    image = cv2.bitwise_and(image, image, mask=thresh)
    return image


# 아래 함수는 위의 함수와 동일한 기능을 수행합니다. 그러나 많이 느립니다.
def remove_black_with_iterate(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    width, height = image.shape[:2]

    for i in range(width):
        for j in range(height):
            r, g, b, a = image[i][j]
            if r == 0 and g == 0 and b == 0:
                image[i][j][3] = 0

    return image


def stitch_image(src_dir, dst_dir=None):
    if dst_dir is None:
        dst_dir = src_dir + "_stitched"
    base_path = os.getcwd()
    data_path = os.path.join(base_path, "input")
    image_path = os.path.join(data_path, src_dir)
    print(f"image directory : {image_path}")

    file_names = os.listdir(image_path)

    print(f"detected [{len(file_names)}] files : {file_names}")

    images = []

    for name in file_names:
        img_path = os.path.join(image_path, name)
        print(f"loading : {img_path}")
        img = cv2.imread(img_path)
        images.append(img)

    stitcher = cv2.Stitcher.create()
    status, stitched_image = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        dst_path = os.path.join(base_path, "output", f"{dst_dir}")
        print(f'Stitched image will be saved : {dst_path}')
        cv2.imwrite(f'{dst_path}.jpg', stitched_image)
    else:
        print("스티칭 실패")
