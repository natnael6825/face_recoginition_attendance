import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv
import time

###########################################################################################################################333



def create_folder():
    folder_name = input("Enter folder name: ")
    path = os.path.join("photo", folder_name)
    os.makedirs(path, exist_ok=True)




###########################################################################################################################333





def select_folder():
    root = "photo"
    folders = os.listdir(root)
    print("Select a Class:")

    for i, folder in enumerate(folders):
        print(f"{i+1}. {folder}")
    choice = int(input()) - 1
    folder_path = os.path.join(root, folders[choice])
    return folder_path






###########################################################################################################################333










def delete_photo():


    photo_dir = select_folder()
    image_files = [f for f in os.listdir(photo_dir) if os.path.isfile(os.path.join(photo_dir, f))]
    if not image_files:
        print("No photos to delete")
        return


    print("Select an image to delete:")
    for i, f in enumerate(image_files):
        print(f"{i+1}. {f}")


    while True:
        try:
            selection = int(input("Enter number of image to delete (or 0 to cancel): "))
            if selection == 0:
                return
            elif selection < 1 or selection > len(image_files):
                print("Invalid selection")
            else:
                break
        except ValueError:
            print("Invalid input")


    filename = os.path.join(photo_dir, image_files[selection-1])
    os.remove(filename)
    print(f"Deleted {filename}")

###########################################################################################################################333






def capture_image():

    path=select_folder()

    cap = cv2.VideoCapture(0)

    time.sleep(1)
    print("Press 'q' to quit, or 's' to save")
    while True:
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)


        cv2.imshow("Video Stream", frame)

        key = cv2.waitKey(1)
        if key == ord("q"):

            break

        if key == ord("r"):
            continue

        if key == ord("s"):

            cap.release()
            cv2.destroyAllWindows()

            name = input("Enter name for Student: ")


            if not os.path.exists(path):
                os.makedirs(path)
            filename = f"{name}.jpg"
            save_file = os.path.join(path, filename)
            cv2.imwrite(save_file, frame)
            print(f"Image saved to {save_file}")
            return


    cap.release()
    cv2.destroyAllWindows()



###########################################################################################################################333







def attendance():
    path = select_folder()
    images = []
    classNames = []
    myList = os.listdir(path)

    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        print(path)


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
        folder_name =path.replace("photo\\", "")
        file_name = f"{folder_name}_Attendance_{date_string}.csv"


        if not os.path.isfile(file_name):
            with open(file_name, "w") as f:
                f.write("Name,Date\n")


        with open(file_name, "r+") as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(",")
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{name},{dtString}")



    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    face_detected = False
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
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
                if not face_detected:
                    markAttendance(name)
                    face_detected = True
            else:
                face_detected = False

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break



###########################################################################################################################333






def main():
    while True:
        print("\nChoose an operation:")
        print("1. Attendance")
        print("2. Add Picture to attendance")
        print("3. Delete from attendance")
        print("4. Create Attendance")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            attendance()
        elif choice == '2':
            capture_image()
        elif choice == '3':
            delete_photo()
        elif choice == '4':
            create_folder()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()













