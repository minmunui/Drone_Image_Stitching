import datetime
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


def stitch_image(src_dir, dst_dir=None, crop_level=0, pano_confident_thresh=1.0):
    # 현재 시각
    print("현재 시각 : ", datetime.datetime.now())
    if dst_dir is None:
        dst_dir = src_dir + "_stitched"
    base_path = os.getcwd()
    data_path = os.path.join(base_path, "input")
    image_path = os.path.join(data_path, src_dir)
    print(f"image directory : {image_path}")

    file_names = os.listdir(image_path)

    print(f"detected [{len(file_names)}] files : {file_names}")
    dst_path = os.path.join(base_path, "output", f"{dst_dir}")

    images = []
    index = 0

    for name in file_names:
        img_path = os.path.join(image_path, name)
        print(f"loading : {img_path}")
        img = cv2.imread(img_path)
        for i in range(crop_level):
            img = cv2.pyrDown(img)
        # down된 이미지 저장
        # cv2.imwrite(f'{dst_path}_down_{index}.jpg', img)
        images.append(img)
        index += 1

    status, stitched_image = stitch_divide_and_conquer(images, batch_size=2, dst_path=dst_path)

    if status == cv2.Stitcher_OK:
        print(f'Stitched image will be saved : {dst_path}')
        cv2.imwrite(f'{dst_path}.jpg', stitched_image)
    else:
        print("스티칭 실패")

    # 현재 시각을 출력
    print("현재 시각 : ", datetime.datetime.now())


def stitch_all_in_one(images):
    stitcher = cv2.Stitcher.create(mode=cv2.Stitcher_SCANS)
    status, stitched_image = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        return stitched_image, status
    else:
        return None, status


def stitch_divide_and_conquer(images, batch_size=2, dst_path="output", pano_confident_thresh=1.0):

    stitcher = cv2.Stitcher.create(mode=cv2.Stitcher_SCANS)
    stitcher.setPanoConfidenceThresh(pano_confident_thresh)

    input_images = images
    input_image_names = []

    stitched_images = []

    _round = 0

    while len(input_images) > 1:
        n_patch = (len(input_images) // batch_size) + 1
        print(f"round : {_round} ")
        for i in range(n_patch):
            print(f"patch : {i} / {n_patch}")
            start = i * batch_size
            end = min((i + 1) * batch_size, len(input_images))

            status, stitched_image = stitcher.stitch(input_images[start:end])

            if status == cv2.Stitcher_OK:
                stitched_images.append(stitched_image)
                cv2.imwrite(f"{dst_path}_stitched_round{_round}_step{i}.jpg", stitched_image)
                input_image_names.append(f"{dst_path}_stitched_round{_round}_step{i}.jpg")
            else:
                print(f"stitching failed at {i}th patch in {_round}th round")
                if _round > 0:
                    print("failed images :")
                    for name in input_image_names[start:end]:
                        print(name)

        input_images = stitched_images
        stitched_images = []
        input_image_names = []
        _round += 1

    return 1, input_images[0]

