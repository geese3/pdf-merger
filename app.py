import os
import uuid
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from PyPDF2 import PdfMerger

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # 실제 운영 환경에서는 보안을 위해 변경해야 합니다

# 업로드된 파일을 저장할 디렉토리 설정
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 허용되는 파일 확장자
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(filename):
    # 파일 확장자 추출
    ext = filename.rsplit('.', 1)[1].lower()
    # 고유한 파일명 생성
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return unique_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    if 'files[]' not in request.files:
        flash('파일이 선택되지 않았습니다.')
        return redirect(request.url)
    
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        flash('파일이 선택되지 않았습니다.')
        return redirect(request.url)
    
    # PDF 파일만 필터링
    pdf_files = []
    for file in files:
        if file and allowed_file(file.filename):
            # 고유한 파일명 생성
            unique_filename = get_unique_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            pdf_files.append(file_path)
    
    if not pdf_files:
        flash('PDF 파일이 없습니다.')
        return redirect(request.url)
    
    try:
        # PDF 병합
        merger = PdfMerger()
        for pdf in pdf_files:
            merger.append(pdf)
        
        # 결과 파일 저장
        output_filename = f"merged_{uuid.uuid4().hex}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        merger.write(output_path)
        merger.close()
        
        # 임시 파일 정리
        for pdf in pdf_files:
            try:
                os.remove(pdf)
            except Exception as e:
                print(f"임시 파일 삭제 중 오류 발생: {str(e)}")
        
        # 결과 파일 다운로드
        return send_file(output_path, as_attachment=True, download_name=output_filename)
        
    except Exception as e:
        flash(f'오류가 발생했습니다: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 