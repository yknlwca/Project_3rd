from flask import Flask, render_template, request, jsonify
from flask import redirect, url_for
import os
from pathlib import Path
from ultralytics import YOLO

app = Flask(__name__)

# 이미지를 저장할 폴더 경로
UPLOAD_FOLDER = './static/uploads'
# DETECT_FOLDER = './static/detects'
DETECT_FOLDER = 'C:/Users/user/runs/detect/predict'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DETECT_FOLDER'] = DETECT_FOLDER

# 검출결과
DETECT_RESULT = []


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'images' in request.files:
            images = request.files.getlist('images')

            # 이미지를 업로드 폴더에 저장
            for i, image in enumerate(images):
                image_filename = f"image_{i + 1}.jpg"  # 이미지 파일 이름을 정의
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

            result = '이미지 전송 및 저장 성공'
        else:
            result = '이미지를 선택하세요.'
    except Exception as e:
        result = f'오류 발생: {str(e)}'

    return jsonify({'result': result})

@app.route('/display')
def display():
    # 업로드된 이미지와 설명을 읽어서 테이블 생성
    image_data = []
    # upload_folder_path = Path(app.config['DETECT_FOLDER'])
    upload_folder_path = Path(DETECT_FOLDER)

    for image_path in upload_folder_path.glob('*.jpg'):
        image_filename = image_path.name
        # description_filename = 'image_1.txt'
        # try:
        #     with open(upload_folder_path / description_filename, 'r') as file:
        #         descriptions = file.read().splitlines()
        # except FileNotFoundError:
        #     descriptions = []
        # image_data.append({'filename': image_filename, 'descriptions': descriptions})
        image_data.append({'filename': image_filename, 'descriptions': ['not yet 1234567890...']})

    return render_template('display.html', image_data=image_data)

@app.route('/yolo')
def yolo():
    model = YOLO('yolov8n.pt')
    results = model.predict(UPLOAD_FOLDER, task='detect', save=True)
    DETECT_RESULT.append(results[0].tojson())

    return redirect(url_for('display'))

if __name__ == '__main__':
    app.run(debug=True)
