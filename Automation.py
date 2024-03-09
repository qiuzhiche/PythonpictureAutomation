import os

current_directory = os.getcwd()
config_folder_path = os.path.join(current_directory, "Config")

if os.path.exists(config_folder_path) and os.path.isdir(config_folder_path):
    print("\033[32m[normal]:Config文件夹存在,程序运行\033[0m")
    print("\033[32m自动化图像识别\033[0m")
    print("\033[32m作者：MWPDT\033[0m")
    print("\033[32mV1.0\033[0m")
else:
    print("\033[32m[normal]:正在创建名为'Config'文件夹\033[0m")
    path = "Config/picture"
    os.makedirs(path)
    print("\033[32m[normal]:'Config'文件夹创建成功\033[0m")
    print("\033[32m[normal]:正在Config中创建名为'picture'文件夹\033[0m")
    print("\033[32m[normal]:'picture'文件夹创建成功\033[0m")
    # 在程序运行目录下创建名为"Config"的文件夹，在名为"Config"的文件夹再创建一个名为"picture"

import os
import cv2
import numpy as np
import pyautogui
import keyboard
import tkinter as tk
from tkinter import filedialog

# 获取当前程序运行目录
current_dir = os.path.dirname(os.path.abspath(__file__))
picture_folder = os.path.join(current_dir, 'Config', 'picture')


def browse_images():
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
            print(
                f"\033[31m[error]: 无法读取图像 {image_file},请将文件名改成target_image如果有多个图像请按顺序因此递增(例如：target_image1 "
                f"target_image2 target_image3...)\033[0m")
            input("\033[32m[提示]：按回车键退出\033[0m")
    return target_images


def main():
    target_images = browse_images()
    if not target_images:
        print("\033[31m[error]: 未选择要识别的图像\033[0m")
        return
    print("\033[32m[提示]：为了防止鼠标失控,必要时按F8退出\033[0m")
    running = True
    while running:
        # 读取屏幕截图并转换为numpy数组
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        for target_image in target_images:
            # 在屏幕截图中查找目标图像
            result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val > 0.8:  # 设置阈值，确保识别准确性
                print("\033[32m[normal]:识别到图像,移动点击\033[0m")
                # 输出目标图像位置
                target_width, target_height = target_image.shape[1], target_image.shape[0]
                top_left = max_loc
                bottom_right = (top_left[0] + target_width, top_left[1] + target_height)
                print(f'\033[32m[normal]:图像屏幕空间坐标: {top_left} - {bottom_right}\033[0m')

                # 移动鼠标并点击目标图像中心
                target_center = (top_left[0] + target_width // 2, top_left[1] + target_height // 2)
                pyautogui.moveTo(target_center)
                pyautogui.click()
            else:
                print("\033[32m[normal]:未识别到图像\033[0m")

        # 检测是否按下F8键，如果是则结束循环
        if keyboard.is_pressed('f8'):
            running = False
            input("\033[32m[提示]：按回车键退出\033[0m")


if __name__ == "__main__":
    main()
