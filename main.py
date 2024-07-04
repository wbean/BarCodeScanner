import cv2
from pyzbar import pyzbar
import pyperclip
import pyautogui
import time

def decode_qrcode(frame):
    # 找到所有二维码并解码
    qrcodes = pyzbar.decode(frame)
    for qrcode in qrcodes:
        # 提取二维码的边界框的位置
        (x, y, w, h) = qrcode.rect
        # 在图像上绘制边界框
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 二维码数据为字节对象，所以如果我们想在输出图像上绘制它
        # 我们需要将它转换成字符串
        qrcode_data = qrcode.data.decode("utf-8")
        qrcode_type = qrcode.type

        # 在图像上绘制二维码数据和类型
        text = f"{qrcode_data} ({qrcode_type})"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 将二维码数据复制到剪贴板
        pyperclip.copy(qrcode_data)
        print(f"二维码数据已复制到剪贴板: {qrcode_data}")

        # 尝试将二维码数据插入到当前光标处
        try:
            insert_text_at_cursor(qrcode_data)
        except Exception as e:
            print(f"插入二维码数据失败: {e}")

        return frame, True  # 返回帧和识别状态

    return frame, False  # 返回帧和识别状态

def insert_text_at_cursor(text):
    time.sleep(0.5)  # 延迟以确保焦点切换完成
    pyautogui.write(text)


# 打开默认摄像头
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

paused = False

while True:
    if not paused:
        # 逐帧捕捉
        ret, frame = cap.read()

        # 如果帧被正确地捕获
        if not ret:
            print("无法接收帧（流结束？）")
            break

        # 调用解码函数
        frame, found = decode_qrcode(frame)

        if found:
            paused = True

        # 调整显示窗口的大小
        display_frame = cv2.resize(frame, (320, int(frame.shape[0] * 320 / frame.shape[1])))
        
        # 显示结果帧
        cv2.imshow('scanner', display_frame)

    # 按 'q' 键退出循环
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif paused and (key == ord(' ') or key == ord('\r')):
        paused = False

# 完成后释放捕获
cap.release()
cv2.destroyAllWindows()

