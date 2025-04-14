from PIL import Image, ImageDraw
import os

# 512x512 크기의 이미지 생성
img = Image.new('RGBA', (512, 512), (43, 43, 43, 255))
draw = ImageDraw.Draw(img)

# 둥근 사각형 그리기
draw.rounded_rectangle([(128, 128), (384, 384)], radius=32, fill=(255, 255, 255, 255))

# 세 개의 가로선 그리기
draw.rectangle([(192, 192), (320, 224)], fill=(43, 43, 43, 255))
draw.rectangle([(192, 256), (320, 288)], fill=(43, 43, 43, 255))
draw.rectangle([(192, 320), (320, 352)], fill=(43, 43, 43, 255))

# ICO 파일로 저장
ico_path = os.path.join(os.path.dirname(__file__), 'pdf_icon.ico')
img.save(ico_path, format='ICO', sizes=[(256, 256)])

print("아이콘 생성이 성공적으로 완료되었습니다.") 