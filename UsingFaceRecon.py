import face_recognition
import os
import cv2
import pickle


def getLabel(result,label):
    j=0
    for i in result:
        if(i):
            print("Image has "+label[j]+"in it .")
        j+=1
if(os.path.isfile("TrainingData.pkl")):
    trainedfile = open('TrainingData.pkl', 'rb')
    Labelfile = open('LabelData.pkl', 'rb')
    TrainingData=pickle.load(trainedfile)
    labels=pickle.load(Labelfile)
else:
    TrainingData=[]
    labels=[]
    TestData=[]
if(not(os.path.isfile("TrainingData.pkl"))):
    TraningFiles=os.listdir("TrainingData")
    for files in TraningFiles:
        file=os.listdir("TrainingData"+"/"+files)
        for Image in file:
            IMAGE=face_recognition.load_image_file("TrainingData"+"/"+TraningFiles[TraningFiles.index(files)]+"/"+Image)
            try:
                image= cv2.imread("TrainingData"+"/"+TraningFiles[TraningFiles.index(files)]+"/"+Image,0)
                (top, right, bottom, left) = face_recognition.face_locations(IMAGE)
                cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.imshow('Training Data',image)
                cv2.wait(500)
                TrainingData.append(face_recognition.face_encodings(IMAGE)[0])
                labels.append(TraningFiles[TraningFiles.index(files)])
                cv2.destroyAllWindows()
            except:
                print("I wasn't able to locate any faces in at least one of the images. Check the image files: "+"TrainingData"+"/"+TraningFiles[TraningFiles.index(files)]+"/"+Image)
    trainedfile = open('TrainingData.pkl', 'wb')
    Labelfile = open('LabelData.pkl', 'wb')
    pickle.dump(TrainingData, trainedfile)
    pickle.dump(labels,Labelfile)
else:
    trainedfile = open('TrainingData.pkl', 'rb')
    Labelfile = open('LabelData.pkl', 'rb')
    TrainingData=pickle.load(trainedfile)
    labels=pickle.load(Labelfile)
# TestFiles=os.listdir("TestData")
# for Image in TestFiles:
#     IMAGE=face_recognition.load_image_file("TestData"+"/"+Image)
#     try:
#         TestData.append(face_recognition.face_encodings(IMAGE)[0])
#     except IndexError:
#         print("I wasn't able to locate any faces in at least one of the images. Check the image files. "+Image)
# for test in TestData:
#     results = face_recognition.compare_faces(TrainingData, test)
#     getLabel(results,labels)
video_capture = cv2.VideoCapture(0)
process_this_frame=True
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_names=[]
    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(TrainingData, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = labels[first_match_index]
                print(name)
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()