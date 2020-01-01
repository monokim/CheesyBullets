import cv2
import pyautogui
import numpy as np
import torch

class Monitor:
    __instance = None
    def get_instance():
        if Monitor.__instance == None:
            Monitor()
        return Monitor.__instance

    def __init__(self, device, region):
        if Monitor.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Monitor.__instance = self

        self.play_flag = False
        self.device = device
        self.region = region
        self.screen = np.array(pyautogui.screenshot(region=self.region))
        self.gray = None
        self.thres = None

    def caputre_screen(self):
        self.screen = np.array(pyautogui.screenshot(region=self.region))

    def get_screen(self, pytorch=False, size=(256, 256)):
        if pytorch == True:
            image = cv2.resize(self.screen, size).transpose((2, 0, 1))
            image = np.ascontiguousarray(image, dtype=np.float32) / 255
            return torch.from_numpy(image).unsqueeze(0).to(self.device)
        else:
            return self.screen
