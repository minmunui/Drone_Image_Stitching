import cv2


def trim_black(img):
    # trim black area
    # 검은색 배경 제거
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    cv2.imshow('thresh', thresh)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours[0])
    trim = img[y:y + h, x:x + w]
    return trim
