import os
from PyPDF2 import PdfMerger

def merge_pdfs(input_files, output_file):
    """
    여러 PDF 파일을 하나로 병합하는 함수
    
    Args:
        input_files (list): 병합할 PDF 파일들의 경로 리스트
        output_file (str): 결과 PDF 파일의 경로
    """
    merger = PdfMerger()
    
    try:
        # 각 PDF 파일을 순차적으로 병합
        for pdf in input_files:
            merger.append(pdf)
        
        # 결과 파일 저장
        merger.write(output_file)
        merger.close()
        print(f"PDF 파일이 성공적으로 병합되었습니다: {output_file}")
        
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")
        merger.close()

def main():
    # 현재 디렉토리의 모든 PDF 파일 찾기
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    
    if not pdf_files:
        print("현재 디렉토리에 PDF 파일이 없습니다.")
        return
    
    print("병합할 PDF 파일 목록:")
    for i, pdf in enumerate(pdf_files, 1):
        print(f"{i}. {pdf}")
    
    # 사용자에게 병합할 파일 선택
    selected_files = input("\n병합할 파일 번호를 쉼표로 구분하여 입력하세요 (예: 1,2,3): ")
    selected_indices = [int(x.strip()) - 1 for x in selected_files.split(',')]
    
    # 선택된 파일들의 경로
    input_files = [pdf_files[i] for i in selected_indices]
    
    # 출력 파일 이름 입력
    output_file = input("결과 파일 이름을 입력하세요 (예: merged.pdf): ")
    
    # PDF 병합 실행
    merge_pdfs(input_files, output_file)

if __name__ == "__main__":
    main() 