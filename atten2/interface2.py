import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv
import time
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # create the main menu
        main_menu = tk.Menu(self.root)
        self.root.config(menu=main_menu)

        # create the file menu
        file_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Create New Class", command=self.create_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # create the student menu
        student_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Student", menu=student_menu)
        student_menu.add_command(label="Add Photo", command=self.capture_image)
        student_menu.add_command(label="Delete Photo", command=self.delete_photo)

        # create the attendance menu
        attendance_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Attendance", menu=attendance_menu)
        attendance_menu.add_command(label="Take Attendance", command=self.attendance)

        # create the quit menu
        main_menu.add_command(label="Quit", command=self.root.quit)

    def create_folder(self):
        folder_name = filedialog.askdirectory(title="Create New Class")
        print(folder_name)
        name = simpledialog.askstring("Add Student Photo", "Enter name for Student:")
        if folder_name:
            path = os.path.join(folder_name, name)
            os.makedirs(path, exist_ok=True)
            messagebox.showinfo("Success", f"Class {os.path.basename(name)} created successfully")

    def select_folder(self):
        folder_name = filedialog.askdirectory(title="Select a Class")
        return folder_name

    def delete_photo(self):
        folder_path = self.select_folder()
        if not folder_path:
            return

        image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not image_files:
            messagebox.showinfo("Info", "No photos to delete")
            return

        selected_photo = messagebox.askquestion("Delete Photo", "Are you sure you want to delete a photo?")
        if selected_photo == "yes":
            # Display list of images with corresponding numbers
            options = [os.path.splitext(f)[0] for f in image_files]
            selected_option = tk.StringVar(value=options[0])
            option_menu = tk.OptionMenu(self.root, selected_option, *options)
            option_menu.pack(pady=10)

            def delete_image():
                filename = os.path.join(folder_path, selected_option.get() + ".jpg")
                os.remove(filename)
                messagebox.showinfo("Success", f"{filename} deleted successfully")
                self.root.focus()

            delete_button = tk.Button(self.root, text="Delete", command=delete_image)
            delete_button.pack(pady=5)

    def capture_image(self):
        folder_path = self.select_folder()
        if not folder_path:
            return

        # Capture image from default camera
        cap = cv2.VideoCapture(0)
        # Give camera time to adjust to lighting conditions
        time.sleep(1)
        print("Press 'q' to quit, or 's' to save")
        while True:
            success, frame = cap.read()
            frame = cv2.flip(frame, 1)  # Flip the frame horizontally for mirror effect

            # Display the video stream as a mirror image
            cv2.imshow("Video Stream", frame)

            key = cv2.waitKey(1)
            if key == ord("q"):
                break

            if key == ord("r"):
                continue

            if key == ord("s"):
                # Release the camera and close the video window
                cap.release()
                cv2.destroyAllWindows()

                name = simpledialog.askstring("Add Student Photo", "Enter name for Student:")

                # Save image to specified path
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                filename = f"{name}.jpg"
                save_file = os.path.join(folder_path, filename)
                cv2.imwrite(save_file, frame)
                messagebox.showinfo("Success", f"Image saved to {save_file}")
                break

        # Release the camera and close the video window
        cap.release()
        cv2.destroyAllWindows()

    def attendance(self):
        folder_path = self.select_folder()

        folder = os.path.basename(folder_path)

        if not folder_path:
            return

        images = []
        classNames = []
        myList = os.listdir(folder_path)

        for cl in myList:
            curImg = cv2.imread(f'{folder_path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                face_encodings = face_recognition.face_encodings(img)
                if len(face_encodings) > 0:
                    encodeList.append(face_encodings[0])
            return encodeList

        def markAttendance(name):

            now = datetime.now()
            date_string = now.strftime("%Y-%m-%d")
            folder_name = folder_path

            file_name = f"{folder}_Attendance_{date_string}.csv"


            attendance_file = os.path.join(folder_path2, file_name)
            if not os.path.exists(attendance_file):
                with open(attendance_file, 'w') as f:
                    f.write("Name,Time\n")


            with open(attendance_file, 'r+') as f:
                existing_names = [line.split(',')[0] for line in f.readlines()]
                if name not in existing_names:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S')
                    f.writelines(f'\n{name},{dtString}')

        encodeListKnown = findEncodings(images)
        print('Encoding Complete')
        folder_path2 = filedialog.askdirectory(title="Where to dave the attendance")
        cap = cv2.VideoCapture(0)
        # Give camera time to adjust to lighting conditions
        time.sleep(1)
        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurrentFrame = face_recognition.face_locations(imgS)
            encodesCurrentFrame = face_recognition.face_encodings(imgS, facesCurrentFrame)

            for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                    markAttendance(name)

            cv2.imshow('Webcam', img)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    root = tk.Tk()
    attendance_system = AttendanceSystem(root)
    root.mainloop()