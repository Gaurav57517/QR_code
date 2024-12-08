from tkinter import *
import qrcode
import cv2
import os
from PIL import Image, ImageTk
from resizeimage import resizeimage
from tkinter import filedialog, messagebox

class QrGenerator:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x500+200+50")
        self.root.title("QR Generator | Developed by Gaurav")
        self.root.resizable(False, False)
        self.create_main_window()

    def create_main_window(self):
        # Title and Subtitle
        Label(self.root, text="QR Code Generator", font=("Times New Roman", 40), bg='#00ff00', fg='black').pack(fill=X)
        Label(self.root, text="Developed by Gaurav", font=("Times New Roman", 10), bg='#00ff00', fg='black').place(x=670, y=10)

        # Student Details Frame
        self.student_details_frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        self.student_details_frame.place(x=50, y=80, width=500, height=380)
        
        Label(self.student_details_frame, text="Student Details", font=("Goudy Old Style", 20), bg='#00ff00', fg='black').pack(fill=X)

        labels = ["Student Name", "Student Roll", "Student Mobile", "Student Email"]
        self.entries = {}
        for i, label in enumerate(labels):
            Label(self.student_details_frame, text=f"{label}:", font=("Times New Roman", 15, 'bold'), bg='white').place(x=20, y=60 + i*40)
            self.entries[label] = Entry(self.student_details_frame, font=("Times New Roman", 15, 'bold'), bg='lightyellow')
            self.entries[label].place(x=200, y=60 + i*40)

        Button(self.student_details_frame, text='CLEAR', command=self.clear_fields, font=("Times New Roman", 18, 'bold'), bg='#607d8b', fg='white').place(x=50, y=250, width=120, height=30)
        Button(self.student_details_frame, text='GENERATE', command=self.generate_qr_code, font=("Times New Roman", 18, 'bold'), bg='#2196f3', fg='white').place(x=200, y=250, width=180, height=30)

        self.message = Label(self.student_details_frame, text='', font=("Times New Roman", 20, 'bold'), bg='white', fg='green')
        self.message.place(x=0, y=310, relwidth=1)

        # QR Code Frame
        self.qr_frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        self.qr_frame.place(x=600, y=80, width=250, height=380)
        
        Label(self.qr_frame, text="Student QR Code", font=("Goudy Old Style", 20), bg='#00ff00', fg='black').pack(fill=X)

        self.qr_code_label = Label(self.qr_frame, text="NO IMAGE\nor\n QR CODE", font=("Times New Roman", 15), bg='#607d8b', fg='white', bd=1, relief=RIDGE)
        self.qr_code_label.place(x=35, y=80, width=180, height=180)

        Button(self.qr_frame, text='SAVE', command=self.save_qr_code, font=("Times New Roman", 18, 'bold'), bg='#2196f3', fg='white').place(x=120, y=320, width=120, height=30)
        Button(self.qr_frame, text='EXIT', command=self.root.quit, font=("Times New Roman", 18, 'bold'), bg='#607d8b', fg='white').place(x=5, y=320, width=100, height=30)

        Button(self.root, text='SCAN', command=self.open_scanner, font=("Times New Roman", 18, 'bold'), bg='#607d8b', fg='white').place(x=5, y=15, width=100, height=30)

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, END)
        self.message.config(text='')
        self.qr_code_label.config(image='', text="NO IMAGE\nor\n QR CODE")

    def generate_qr_code(self):
        try:
            data = {label: entry.get() for label, entry in self.entries.items()}
            if not all(data.values()):
                self.message.config(text='All fields are required!!!!', fg='red')
                return

            qr_data = '\n'.join(f"{key}: {value}" for key, value in data.items())
            qr_code = qrcode.make(qr_data)
            qr_code = resizeimage.resize_cover(qr_code, [180, 180])

            if not os.path.exists("Image"):
                os.makedirs("Image")

            file_path = os.path.join("Image", f"{data['Student Mobile']}.png")
            qr_code.save(file_path)

            self.display_qr_code(file_path)
            self.message.config(text='QR Generated Successfully....', fg='green')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {e}")

    def display_qr_code(self, file_path):
        image = Image.open(file_path)
        self.qr_code_image = ImageTk.PhotoImage(image)
        self.qr_code_label.config(image=self.qr_code_image, text='')

    def save_qr_code(self):
        try:
            if not self.qr_code_image:
                self.msg = 'QR code is not available!!!!'
                self.lbl_msg.config(text=self.msg, fg='red')
                return

            data = {label: entry.get() for label, entry in self.entries.items()}
            qr_data = '\n'.join(f"{key}: {value}" for key, value in data.items())
            qr_code = qrcode.make(qr_data)
            resized_img = qr_code.resize((280, 250))

            path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if path:
                resized_img.save(path)
                messagebox.showinfo("Success", "QR Code is saved")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save QR code: {e}")

    def open_scanner(self):
        try:
            self.root.withdraw()
            scanner_window = Toplevel(self.root)
            QrScanner(scanner_window, self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open scanner: {e}")

class QrScanner:
    def __init__(self, scanner_window, main_window):
        self.scanner_window = scanner_window
        self.main_window = main_window
        self.scanner_window.geometry("900x500+200+50")
        self.scanner_window.title("QR Scanner | Developed by Gaurav")
        self.scanner_window.resizable(False, False)
        self.create_scanner_window()

    def create_scanner_window(self):
        # Title and Subtitle
        Label(self.scanner_window, text="QR Code Scanner", font=("Times New Roman", 40), bg='#00ff00', fg='black').pack(fill=X)
        Label(self.scanner_window, text="Developed by Gaurav", font=("Times New Roman", 10), bg='#00ff00', fg='black').place(x=670, y=10)

        # Back Button
        back_button = Button(self.scanner_window, text="Back", bg='#607d8b', fg='white', font=("Times New Roman", 15, 'bold'), relief=RAISED, command=self.go_back)
        back_button.place(x=5, y=15, width=100, height=30)

        # QR Code Frames
        self.create_qr_code_frames()

    def load_image(self, path, size, default_color):
        try:
            img = Image.open(path)
            img = resizeimage.resize_cover(img, size)
        except FileNotFoundError:
            img = Image.new('RGB', size, color=default_color)
        return ImageTk.PhotoImage(img)

    def create_qr_code_frames(self):
        qr_frames = Frame(self.scanner_window, bd=2, relief=RIDGE, bg='white')
        qr_frames.place(x=600, y=80, width=280, height=380)
        Label(qr_frames, text="Upload QR Code", font=("Goudy Old Style", 20), bg='#00ff00', fg='black').pack(fill=X)

        self.upload_frame = Frame(self.scanner_window, bd=2, relief=RIDGE, bg='white')
        self.upload_frame.place(x=338, y=80, width=290, height=380)
        Label(self.upload_frame, text="Scan QR Code", font=("Goudy Old Style", 20), bg='#00ff00', fg='black').pack(fill=X)

        self.qr_code_frame = Frame(self.scanner_window, bd=2, relief=RIDGE, bg='white')
        self.qr_code_frame.place(x=50, y=80, width=290, height=380)
        self.qr_code_inner_frame = Frame(self.qr_code_frame, bd=2, relief=RIDGE, bg='white')
        self.qr_code_inner_frame.place(x=15, y=60, width=260, height=220)

        self.qr_code_text = Text(self.qr_code_inner_frame, height=10, width=30, font=("Goudy Old Style", 10))
        self.qr_code_text.pack(expand=True)
        Label(self.qr_code_frame, text="QR Details", font=("Goudy Old Style", 20), bg='#00ff00', fg='black').pack(fill=X)

        self.upload_qr_code_label = Label(qr_frames, text="NO IMAGE\nor\n QR CODE", font=("Times New Roman", 15), bg='#607d8b', fg='white', bd=1, relief=RIDGE)
        self.upload_qr_code_label.place(x=60, y=80, width=180, height=180)

        Button(self.upload_frame, text='SCAN', command=self.scan_qr_code, font=("Times New Roman", 18, 'bold'), bg='#2196f3', fg='white').place(x=85, y=300, width=100, height=30)
        Button(qr_frames, text='UPLOAD', command=self.upload_file, font=("Times New Roman", 18, 'bold'), bg='#2196f3', fg='white').place(x=85, y=300, width=120, height=30)
        Button(self.qr_code_frame, text='CLEAR', command=self.clear_text, font=("Times New Roman", 18, 'bold'), bg='#607d8b', fg='white').place(x=85, y=300, width=110, height=30)

    def upload_file(self):
        try:
            filepath = filedialog.askopenfilename(initialdir="./", title="Select Image File", filetypes=[("All files", "*.*"), ("JPEG files", "*.jpg"), ("PNG files", "*.png")])
            if filepath:
                self.display_qr_image(filepath)
                self.decode_qr_code(filepath)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

    def display_qr_image(self, filepath):
        img = Image.open(filepath)
        img.thumbnail((200, 180))
        self.upload_qr_code_image = ImageTk.PhotoImage(img)
        self.upload_qr_code_label.config(image=self.upload_qr_code_image)

    def decode_qr_code(self, filepath):
        img = cv2.imread(filepath)
        detector = cv2.QRCodeDetector()
        value, _, _ = detector.detectAndDecode(img)
        self.qr_code_text.delete("1.0", "end")
        self.qr_code_text.insert("1.0", value)

    def scan_qr_code(self):
        try:
            cap = cv2.VideoCapture(0)
            detector = cv2.QRCodeDetector()
            while True:
                ret, img = cap.read()
                if not ret:
                    break
                data, _, _ = detector.detectAndDecode(img)
                if data:
                    self.qr_code_text.delete("1.0", "end")
                    self.qr_code_text.insert("1.0", data)
                    break
                cv2.imshow("QR Scanner", img)
                if cv2.waitKey(1) == ord("q"):
                    break
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scan QR code: {e}")

    def clear_text(self):
        self.qr_code_text.delete("1.0", "end")
        self.upload_qr_code_label.config(image='', text="NO IMAGE\nor\n QR CODE")

    def go_back(self):
        self.scanner_window.destroy()
        self.main_window.deiconify()

if __name__ == "__main__":
    root = Tk()
    QrGenerator(root)
    root.mainloop()
