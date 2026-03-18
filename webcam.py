import cv2
import mediapipe as mp

mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=1)
mp_draw=mp.solutions.drawing_utils

cap=cv2.VideoCapture(0)

print("Camera turning on... Press 'Q' in the video window to quit!")

while True:
    success,img=cap.read()
    if not success:
        break

    img=cv2.flip(img,1)

    img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    results=hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img,hand_landmarks, mp_hands.HAND_CONNECTIONS)

            tip_y=hand_landmarks.landmark[8].y
            knuckle_y=hand_landmarks.landmark[6].y

            if tip_y<knuckle_y:
                print("UP!(Ready to JUMP)")

                h,w,c=img.shape
                cv2.circle(img,(int(hand_landmarks.landmark[8].x*w),int(tip_y*h)),15,(0,255,0),cv2.FILLED)

            else:
                print("Resting...")    
    cv2.imshow("Jedi Controller",img)

    if cv2.waitKey(1)& 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()