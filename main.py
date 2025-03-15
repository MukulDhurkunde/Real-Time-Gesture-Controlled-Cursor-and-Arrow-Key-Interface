import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands and Drawing Utilities
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Get screen dimensions for mapping normalized coordinates to actual screen coordinates
screen_width, screen_height = pyautogui.size()

# Open the webcam
cap = cv2.VideoCapture(0)
prev_x = None
prev_y = None

while cap.isOpened():
    # Start timer for latency calculation
    start_time = time.time()

    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Mirror the frame so that the view is like a mirror
    frame = cv2.flip(frame, 1)

    # Convert the frame from BGR to RGB (MediaPipe works with RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)  # Process the frame and detect hand landmarks

    if results.multi_hand_landmarks:
        for idx, landmarks in enumerate(results.multi_hand_landmarks):
            # Determine handedness (Left or Right)
            handedness = results.multi_handedness[idx].classification[0].label

            # Draw landmarks and connections on the frame
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the landmarks for the index finger tip and PIP joint for click detection
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_mid = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

            if handedness == "Left":  # Left hand controls the mouse
                # Use the middle finger MCP joint as the reference for cursor movement
                mcp = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                cursor_x = int(mcp.x * screen_width)
                cursor_y = int(mcp.y * screen_height)
                pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

                # Click when the index finger tip is below (or level with) the PIP joint
                if index_tip.y >= index_mid.y:
                    pyautogui.click()

            elif handedness == "Right":  # Right hand controls keyboard arrow keys
                # Calculate the index finger tip position in screen coordinates
                x, y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)
                if prev_x is not None and prev_y is not None:
                    dx = x - prev_x
                    dy = y - prev_y

                    # Determine swipe direction based on the difference between frames
                    if abs(dx) > abs(dy):
                        if dx > 50:  # Swipe to the right
                            pyautogui.press('right')
                        elif dx < -50:  # Swipe to the left
                            pyautogui.press('left')
                    else:
                        if dy > 50:  # Swipe down
                            pyautogui.press('down')
                        elif dy < -50:  # Swipe up
                            pyautogui.press('up')
                prev_x = x
                prev_y = y

    # Calculate latency (processing time for the current frame) in milliseconds
    end_time = time.time()
    latency_ms = (end_time - start_time) * 1000

    # Overlay the latency information on the frame
    cv2.putText(frame,
                f"Latency: {latency_ms:.2f} ms",
                (10, 30),  # Position on the frame (x, y)
                cv2.FONT_HERSHEY_SIMPLEX,
                1,         # Font scale
                (0, 255, 0),  # Font color (green)
                2,         # Thickness of the text
                cv2.LINE_AA)

    # Display the final frame with gesture annotations and latency info
    cv2.imshow("Gesture Recognition with Latency", frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
