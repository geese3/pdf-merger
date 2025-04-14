import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import customtkinter as ctk
import platform

class PDFMergerApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("PDF 도구")
        self.root.geometry("600x500")
        
        # 테마 설정
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.pdf_files = []
        self.setup_ui()
        
        # Windows에서만 드래그앤드롭 이벤트 바인딩
        if platform.system() == "Windows":
            self.file_listbox.bind('<Drop>', self.handle_drop)
            self.file_listbox.bind('<DragEnter>', self.handle_drag_enter)
            self.file_listbox.bind('<DragLeave>', self.handle_drag_leave)
    
    def setup_ui(self):
        # 파일 선택 프레임
        self.file_frame = ctk.CTkFrame(self.root)
        self.file_frame.pack(pady=20, padx=20, fill="x")
        
        # 파일 선택 버튼
        self.select_button = ctk.CTkButton(
            self.file_frame,
            text="PDF 파일 선택",
            command=self.select_files
        )
        self.select_button.pack(pady=10)
        
        # 선택된 파일 목록
        self.file_listbox = tk.Listbox(
            self.file_frame,
            height=10,
            width=50,
            bg="#2b2b2b",
            fg="white",
            selectmode=tk.EXTENDED
        )
        self.file_listbox.pack(pady=10, fill="x")
        
        # Windows에서만 드래그앤드롭 안내 텍스트 추가
        if platform.system() == "Windows":
            self.file_listbox.insert(tk.END, "여기에 PDF 파일을 드래그앤드롭하세요")
            self.file_listbox.itemconfig(0, {'fg': 'gray'})
        
        # 안내 텍스트
        if platform.system() == "Windows":
            info_text = "파일 선택 버튼을 클릭하거나 PDF 파일을 드래그앤드롭하세요"
        else:
            info_text = "파일 선택 버튼을 클릭하여 PDF 파일을 선택하세요"
            
        self.info_label = ctk.CTkLabel(
            self.file_frame,
            text=info_text,
            text_color="gray"
        )
        self.info_label.pack(pady=5)
        
        # 파일 순서 변경 버튼
        self.move_frame = ctk.CTkFrame(self.file_frame)
        self.move_frame.pack(pady=10, fill="x")
        
        # 버튼들을 담을 프레임
        self.button_container = ctk.CTkFrame(self.move_frame)
        self.button_container.pack(expand=True)
        
        self.move_up_button = ctk.CTkButton(
            self.button_container,
            text="위로",
            command=self.move_up,
            width=100
        )
        self.move_up_button.pack(side="left", padx=5)
        
        self.move_down_button = ctk.CTkButton(
            self.button_container,
            text="아래로",
            command=self.move_down,
            width=100
        )
        self.move_down_button.pack(side="left", padx=5)
        
        self.remove_button = ctk.CTkButton(
            self.button_container,
            text="제거",
            command=self.remove_selected,
            width=100
        )
        self.remove_button.pack(side="left", padx=5)
        
        # 기능 선택 프레임
        self.function_frame = ctk.CTkFrame(self.root)
        self.function_frame.pack(pady=10, padx=20, fill="x")
        
        # 병합 버튼
        self.merge_button = ctk.CTkButton(
            self.function_frame,
            text="PDF 병합하기",
            command=self.merge_pdfs
        )
        self.merge_button.pack(side="left", padx=5, fill="x", expand=True)
        
        # 분리 버튼
        self.split_button = ctk.CTkButton(
            self.function_frame,
            text="PDF 분리하기",
            command=self.split_pdf
        )
        self.split_button.pack(side="left", padx=5, fill="x", expand=True)
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="PDF 파일 선택",
            filetypes=[("PDF 파일", "*.pdf")]
        )
        
        if files:
            self.pdf_files.extend(files)
            self.update_file_list()
    
    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        if platform.system() == "Windows" and not self.pdf_files:
            self.file_listbox.insert(tk.END, "여기에 PDF 파일을 드래그앤드롭하세요")
            self.file_listbox.itemconfig(0, {'fg': 'gray'})
        else:
            for file in self.pdf_files:
                self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def move_up(self):
        selected = self.file_listbox.curselection()
        if not selected or selected[0] == 0:
            return
        
        index = selected[0]
        self.pdf_files[index], self.pdf_files[index-1] = self.pdf_files[index-1], self.pdf_files[index]
        self.update_file_list()
        self.file_listbox.selection_set(index-1)
    
    def move_down(self):
        selected = self.file_listbox.curselection()
        if not selected or selected[0] == len(self.pdf_files) - 1:
            return
        
        index = selected[0]
        self.pdf_files[index], self.pdf_files[index+1] = self.pdf_files[index+1], self.pdf_files[index]
        self.update_file_list()
        self.file_listbox.selection_set(index+1)
    
    def remove_selected(self):
        selected = self.file_listbox.curselection()
        if not selected:
            return
        
        for index in sorted(selected, reverse=True):
            self.pdf_files.pop(index)
        
        self.update_file_list()
    
    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("경고", "병합할 PDF 파일을 선택해주세요.")
            return
        
        output_file = filedialog.asksaveasfilename(
            title="결과 파일 저장",
            defaultextension=".pdf",
            filetypes=[("PDF 파일", "*.pdf")]
        )
        
        if not output_file:
            return
        
        try:
            merger = PdfMerger()
            for pdf in self.pdf_files:
                merger.append(pdf)
            
            merger.write(output_file)
            merger.close()
            
            messagebox.showinfo("성공", "PDF 파일이 성공적으로 병합되었습니다.")
            
        except Exception as e:
            messagebox.showerror("오류", f"PDF 병합 중 오류가 발생했습니다:\n{str(e)}")
    
    def split_pdf(self):
        if not self.pdf_files:
            messagebox.showwarning("경고", "분리할 PDF 파일을 선택해주세요.")
            return
        
        if len(self.pdf_files) > 1:
            messagebox.showwarning("경고", "한 번에 하나의 PDF 파일만 분리할 수 있습니다.")
            return
        
        pdf_file = self.pdf_files[0]
        
        try:
            # PDF 파일 읽기
            reader = PdfReader(pdf_file)
            total_pages = len(reader.pages)
            
            # 분리할 페이지 범위 입력 다이얼로그
            dialog = ctk.CTkInputDialog(
                text=f"분리할 페이지 범위를 입력하세요 (1-{total_pages})\n예: 1-3,5,7-9\n나머지 페이지는 자동으로 분리됩니다.",
                title="페이지 범위 입력"
            )
            page_range = dialog.get_input()
            
            if not page_range:
                return
            
            # 페이지 범위 파싱
            ranges = self.parse_page_ranges(page_range, total_pages)
            if not ranges:
                messagebox.showerror("오류", "잘못된 페이지 범위입니다.")
                return
            
            # 나머지 페이지 범위 계산
            all_pages = set(range(1, total_pages + 1))
            selected_pages = set()
            for start, end in ranges:
                selected_pages.update(range(start, end + 1))
            
            remaining_pages = sorted(all_pages - selected_pages)
            if remaining_pages:
                # 연속된 페이지를 하나의 범위로 묶기
                current_range = [remaining_pages[0], remaining_pages[0]]
                for page in remaining_pages[1:]:
                    if page == current_range[1] + 1:
                        current_range[1] = page
                    else:
                        ranges.append(tuple(current_range))
                        current_range = [page, page]
                ranges.append(tuple(current_range))
            
            # 출력 디렉토리 선택
            output_dir = filedialog.askdirectory(title="분리된 파일 저장 위치 선택")
            if not output_dir:
                return
            
            # 파일 이름 기반으로 출력 파일 이름 생성
            base_name = os.path.splitext(os.path.basename(pdf_file))[0]
            
            # 각 범위별로 PDF 파일 생성
            for i, (start, end) in enumerate(ranges):
                writer = PdfWriter()
                for page_num in range(start, end + 1):
                    writer.add_page(reader.pages[page_num - 1])
                
                if start == end:
                    output_file = os.path.join(output_dir, f"{base_name}_page_{start}.pdf")
                else:
                    output_file = os.path.join(output_dir, f"{base_name}_pages_{start}-{end}.pdf")
                
                with open(output_file, "wb") as output:
                    writer.write(output)
            
            messagebox.showinfo("성공", "PDF 파일이 성공적으로 분리되었습니다.")
            
        except Exception as e:
            messagebox.showerror("오류", f"PDF 분리 중 오류가 발생했습니다:\n{str(e)}")
    
    def parse_page_ranges(self, page_range, total_pages):
        try:
            ranges = []
            parts = page_range.split(',')
            
            for part in parts:
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    if 1 <= start <= end <= total_pages:
                        ranges.append((start, end))
                    else:
                        return None
                else:
                    try:
                        page = int(part)
                        if 1 <= page <= total_pages:
                            ranges.append((page, page))
                        else:
                            return None
                    except ValueError:
                        return None
            
            return ranges
        except Exception as e:
            print(f"페이지 범위 파싱 오류: {str(e)}")
            return None
    
    def handle_drag_enter(self, event):
        self.file_listbox.configure(bg="#3b3b3b")
        return True
    
    def handle_drag_leave(self, event):
        self.file_listbox.configure(bg="#2b2b2b")
        return True
    
    def handle_drop(self, event):
        self.file_listbox.configure(bg="#2b2b2b")
        
        # Windows에서 파일 경로 처리
        files = event.data.split()
        valid_files = []
        
        for file in files:
            if file.lower().endswith('.pdf'):
                valid_files.append(file)
        
        if valid_files:
            self.pdf_files.extend(valid_files)
            self.update_file_list()
        
        return True
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PDFMergerApp()
    app.run() 