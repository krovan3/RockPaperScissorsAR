import time
import random
import cv2
import datetime
import mediapipe as mp
import math
import tkinter as tk
from PIL import Image, ImageTk


rules_image_path = "venv/rules.png"
player_score = 0
comp_score = 0
mp_hands = mp.solutions.hands

rules = "rules.png",

def check_gesture(hand_landmarks):
    is_scissors = is_scissors_gesture(hand_landmarks)
    if is_scissors:
        #print("Игрок показал жест 'Ножницы'")
        player_gesture = 'ножницы'
        return player_gesture
    is_rock = is_rock_gesture(hand_landmarks)
    if is_rock:
        #print("Игрок показал жест 'Камень'")
        player_gesture = 'камень'
        return player_gesture
    is_paper = is_paper_gesture(hand_landmarks)
    if is_paper:
        #print("Игрок показал жест 'Бумага'")
        player_gesture = 'бумага'
        return player_gesture
    player_gesture = 'Указано неверно, попробуйте ещё'
    return player_gesture


def is_rock_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    if thumb_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y and \
            thumb_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y and \
            thumb_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y and \
            thumb_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y and \
            math.sqrt((thumb_tip.x - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x) ** 2 +
                      (thumb_tip.y - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y) ** 2) > 0.05:
        if index_finger.y > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y and \
                middle_finger.y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y and \
                ring_finger.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y and \
                pinky.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y:
            return True

    return False


def is_scissors_gesture(hand_landmarks):
    index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    if index_finger.y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y and \
            middle_finger.y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y and \
            ring_finger.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y and \
            pinky.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y:
        return True

    return False


def is_paper_gesture(hand_landmarks):
    thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    if thumb.y < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y and \
            index_finger.y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y and \
            middle_finger.y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y and \
            ring_finger.y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y and \
            pinky.y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y:
        return True

    return False


def choose_computer_gesture():
    gestures = ["камень", "ножницы", "бумага"]
    return random.choice(gestures)

def show_rules():
    rules_window = tk.Toplevel(root)
    rules_window.title("Правила")
    rules_image = Image.open(rules_image_path)
    rules_photo = ImageTk.PhotoImage(rules_image)
    rules_label = tk.Label(rules_window, image=rules_photo)
    rules_label.image = rules_photo  # Сохраняем ссылку на изображение, чтобы избежать ошибки отображения
    rules_label.pack()

def choose_winner(a, b):
    result = 0
    global player_score, comp_score
    if a == 'камень':
        if b == 'ножницы':
            result = 'Победа'
            player_score += 1
        elif b == 'камень':
            result = 'Ничья'
            comp_score += 0.5
            player_score += 0.5
        else:
            result = 'Поражение'
            comp_score += 1
    if a == 'ножницы':
        if b == 'ножницы':
            result = 'Ничья'
            comp_score += 0.5
            player_score += 0.5
        elif b == 'камень':
            result = 'Поражение'
            comp_score += 1
        else:
            result = 'Победа'
            player_score += 1
    if a == 'бумага':
        if b == 'ножницы':
            result = 'Поражение'
            comp_score += 1
        elif b == 'камень':
            result = 'Победа'
            player_score += 1
        else:
            result = 'Ничья'
            comp_score += 0.5
            player_score += 0.5
    score_label.config(text=f"Ваш счёт {player_score}:{comp_score} счёт компьютера", font=("Helvetica", 20))
    return result


def detect_hand_gesture():
    with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
        player_gesture = 0
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = mp_hands.Hands().process(image)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Получение координат указательного пальца
                index_finger_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x_pos = int(index_finger_landmark.x * 900)
                y_pos = int(index_finger_landmark.y * 700)
                if y_pos>550 and x_pos>750:
                    show_rules()
                player_gesture = check_gesture(hand_landmarks)
                break
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        frame = tk.Frame(root)
        frame.pack()
        return player_gesture


cap = cv2.VideoCapture(0)

root = tk.Tk()
root.title("Hand Gesture Recognition")
root.geometry("800x700")
player_score = 0
comp_score = 0
score_label = tk.Label(root, text=f"Ваш счёт {player_score}:{comp_score} счёт компьютера", font=("Helvetica", 20), background='#faebd7')
score_label.pack()

frame = tk.Frame(root)
frame.pack()
frame.config(background='#faebd7')
root.config(background='#faebd7')
video_label = tk.Label(frame)
video_label.pack()

def write_game_result(player_score, comp_score):
    with open('game_results.txt', 'a') as f:
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Счёт игрока: {player_score} - {comp_score} Счёт Компьтера \t {formatted_time}")
        f.write(f"\n________________________________________________________\n")

def show_video_stream():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Добавление значка вопроса в правый нижний угол
    question_mark = Image.open("C://Users/KotOr/PycharmProjects/VRFinalProject/venv/question_mark.png")
    frame[380:480, 540:640] = question_mark

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    video_label.after(10, show_video_stream)


show_video_stream()


def play_button_handler():
    gesture = detect_hand_gesture()
    comp_gesture = choose_computer_gesture()
    if gesture!=0:
        gesture_label.config(
            text=f'Жест комьютера: {comp_gesture} \n Ваш жест: {gesture} \n {choose_winner(gesture, comp_gesture)}',background='#faebd7')
    else:
        gesture_label.config(
            text=f'Жест не распознан, попробуйте ещё',
            background='#faebd7')


play_button = tk.Button(frame, text="Выбор сделан", command=play_button_handler, background='#faebd7', width=40,height=5)
play_button.pack()
gesture_label = tk.Label(root, text="", font=("Helvetica", 20))
gesture_label.pack()


root.mainloop()
write_game_result(player_score, comp_score)
