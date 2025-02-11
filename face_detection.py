```
import cv2
import time
import winsound  # For Windows alert sound

def sound_alert():
    winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500ms

def main():
    # Load the pre-trained Haar cascades for face and eye detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    # Open the default camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    drowsy_frames = 0  # Counter for drowsy eye detections
    
    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        # Convert the frame to grayscale for better detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the grayscale image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            # Detect eyes
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))
            if len(eyes) < 2:
                drowsy_frames += 1
            else:
                drowsy_frames = 0
            
            # Trigger alerts
            if drowsy_frames > 15:
                cv2.putText(frame, " ALERT DROWSINESS DETECTED!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                sound_alert()
            
            # Print detected features in console
            print(f"Face at ({x}, {y}) with width {w} and height {h}")
            for (ex, ey, ew, eh) in eyes:
                print(f"Eye detected at ({ex}, {ey}) with width {ew} and height {eh}")
        
        # Display the frame with detections
        cv2.imshow('Driver Drowsiness Detection', frame)
        
        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
  ```
