import os
import cv2
import numpy as np
import pyautogui
import keyboard
import tkinter as tk
from tkinter import filedialog
import pytesseract
from PIL import Image


def create_folders():
    current_directory = os.getcwd()
    config_folder_path = os.path.join(current_directory, "Config")

    if not os.path.exists(config_folder_path):
        print("\033[32m[INFO]: 正在创建名为 'Config' 文件夹\033[0m")
        os.makedirs(config_folder_path)
        print("\033[32m[INFO]: 'Config' 文件夹创建成功\033[0m")

        picture_folder_path = os.path.join(config_folder_path, "picture")
        print("\033[32m[INFO]: 正在 Config 中创建名为 'picture' 文件夹\033[0m")
        os.makedirs(picture_folder_path)
        print("\033[32m[INFO]: 'picture' 文件夹创建成功\033[0m")
        input("\033[32m[INFO]: 按回车键退出......\033[0m")
    else:
        print("\033[32m[INFO]: Config 文件夹存在，程序运行\033[0m")
        text_recognition_folder_path = os.path.join(config_folder_path, "Text Recognition")
        if not os.path.exists(text_recognition_folder_path):
            print("\033[32m[INFO]: 正在 'Config' 中创建名为 'Text Recognition' 文件夹\033[0m")
            os.makedirs(text_recognition_folder_path)
            print("\033[32m[INFO]: 'Text Recognition' 文件夹创建成功\033[0m")
        else:
            print("\033[32m[INFO]: 'Text Recognition' 文件夹已存在\033[0m")


def browse_images(picture_folder=None):
    root = tk.Tk()
    root.withdraw()

    image_files = filedialog.askopenfilenames(title="选择要识别的图像文件", initialdir=picture_folder,
                                              filetypes=(("PNG files", "*.png"), ("All files", "*.*")))

    target_images = []
    for image_file in image_files:
        target_image = cv2.imread(image_file)
        if target_image is not None:
            target_images.append(target_image)
        else:
            print(f"\033[31m[error]: 无法读取图像 {image_file}，请检查文件名是否正确\033[0m")
    return target_images


def perform_image_recognition():
    create_folders()

    target_images = browse_images()
    if not target_images:
        print("\033[31m[error]: 未选择要识别的图像\033[0m")
        return

    print("\033[32m[INFO]: 为了防止鼠标失控, 必要时按F8退出\033[0m")

    while True:
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        for target_image in target_images:
            result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > 0.8:
                print("\033[32m[INFO]: 识别到图像，移动并点击\033[0m")
                target_width, target_height = target_image.shape[1], target_image.shape[0]
                top_left = max_loc
                bottom_right = (top_left[0] + target_width, top_left[1] + target_height)
                print(f'\033[32m[INFO]: 图像屏幕空间坐标: {top_left} - {bottom_right}\033[0m')

                target_center = (top_left[0] + target_width // 2, top_left[1] + target_height // 2)
                pyautogui.moveTo(target_center)
                pyautogui.click()
            else:
                print("\033[32m[INFO]: 未识别到图像\033[0m")

        if keyboard.is_pressed('f8'):
            break

    input("\033[32m[INFO]: 按回车键退出......\033[0m")


def perform_text_recognition():
    create_folders()

    text_recognition_dir = os.path.join(os.getcwd(), "Config", "Text Recognition")
    file_path = os.path.join(text_recognition_dir, "recognition_result.txt")

    root = tk.Tk()
    root.withdraw()

    image_files = filedialog.askopenfilenames(title="选择图片文件",
                                              filetypes=(("图片文件", "*.jpg *.png"), ("所有文件", "*.*")))

    langs = ['eng', 'chi_sim']  # 英语和中文
    with open(file_path, "a", encoding='utf-8') as file:
        for image_file in image_files:
            img = Image.open(image_file)
            for lang in langs:
                data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang=lang)

                file.write(f"图片文件: {image_file}, 语言: {lang}\n")
                for i in range(len(data["text"])):
                    text = data["text"][i]
                    left = data["left"][i]
                    top = data["top"][i]
                    width = data["width"][i]
                    height = data["height"][i]
                    confidence = data["conf"][i]
                    if text:
                        file.write(f"{text} ")
                        print(
                            f"\033[32m[INFO]: 识别结果 ({lang}): {text}(坐标: 左={left}, 上={top}, 宽={width}, 高={height}, 置信度={confidence})\033[0m")
                    # 输出识别结果到控制台，包含语言信息
                file.write("\n")

    print(f"\033[32m[INFO]: 识别结果和文字坐标已写入文件: {file_path}\033[0m")
    print("\033[32m[INFO]: 如果txt文档乱码请用UTF-8编码打开文件~\033[0m")
    root.destroy()
    input("\033[32m[INFO]: 按回车键退出......\033[0m")


def display_menu():
    print("\033[32m请选择功能:\033[0m")
    print("\033[32m1. 自动化图像识别\033[0m")
    print("\033[32m2. 文字识别\033[0m")
    choice = input("\033[32m请输入选项: \033[0m")

    if choice == "1":
        perform_image_recognition()
    elif choice == "2":
        perform_text_recognition()
    else:
        print("\033[32m[INFO]:无效选项，请重新选择\033[0m")
        display_menu()


if __name__ == "__main__":
    display_menu()
