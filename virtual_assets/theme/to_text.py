import pytesseract

image_files = ['KakaoTalk_20220808_085853168.jpg',
'KakaoTalk_20220808_085853168_01.jpg',
'KakaoTalk_20220808_085853168_02.jpg',
'KakaoTalk_20220808_085853168_03.jpg',
'KakaoTalk_20220808_085853168_04.jpg',
'KakaoTalk_20220808_085853168_05.jpg',
'KakaoTalk_20220808_085853168_06.jpg',
'KakaoTalk_20220808_085853168_07.jpg',
'KakaoTalk_20220808_085853168_08.jpg',
'KakaoTalk_20220808_085853168_09.jpg',
'KakaoTalk_20220808_085853168_10.jpg',
'KakaoTalk_20220808_085853168_11.jpg',
'KakaoTalk_20220808_085853168_12.jpg',
'KakaoTalk_20220808_085853168_13.jpg',
'KakaoTalk_20220808_085853168_14.jpg',
]

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

for image_file in image_files:
    print(pytesseract.image_to_string(image_file, lang='kor+eng', timeout=2, config='-c preserve_interword_spaces=1 --psm 4'))

