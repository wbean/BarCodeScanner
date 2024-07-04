import cv2
from pyzbar import pyzbar
import pyperclip
import pyautogui
import time

def decode_qrcode(frame):
    # find all qrcode/barcode and decode
    qrcodes = pyzbar.decode(frame)
    for qrcode in qrcodes:
        # get border for qrcode/barcode
        (x, y, w, h) = qrcode.rect
        # draw border on frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # convert code content to string
        qrcode_data = qrcode.data.decode("utf-8")
        qrcode_type = qrcode.type

        # draw code content and type on frame
        text = f"{qrcode_data} ({qrcode_type})"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # copy to clipboard
        pyperclip.copy(qrcode_data)
        print(f"copy to clipboard success: {qrcode_data}")

        # try to insert content to current cursor position
        try:
            insert_text_at_cursor(qrcode_data)
        except Exception as e:
            print(f"insert content failed: {e}")

        return frame, True  

    return frame, False  

def insert_text_at_cursor(text):
    time.sleep(0.5)  # delay to makesure write success
    pyautogui.write(text)


# default open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("can't open camera")
    exit()

paused = False

while True:
    if not paused:
        # process it frame by frame
        ret, frame = cap.read()

        # if get frame success
        if not ret:
            print("can't get frame, maybe stream is over.")
            break

        # call decode
        frame, found = decode_qrcode(frame)

        if found:
            paused = True

        # adjust window size
        display_frame = cv2.resize(frame, (320, int(frame.shape[0] * 320 / frame.shape[1])))
        
        # show frame result
        cv2.imshow('scanner', display_frame)

    # press 'q' exit, press 'space' or 'enter' start new scan
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif paused and (key == ord(' ') or key == ord('\r')):
        paused = False

# release before exit
cap.release()
cv2.destroyAllWindows()

