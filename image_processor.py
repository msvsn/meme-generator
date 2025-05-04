import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List, Dict, Optional, Union
from utils import TextPosition


class ImageProcessor:
    def __init__(self):
        self.image = None
        self.original_image = None
        self.height = 0
        self.width = 0
        
        self.default_font_path = self.get_system_font_with_cyrillic()

    def get_system_font_with_cyrillic(self) -> str:
        font_paths = []
        
        if os.name == 'nt':
            font_paths = [
                os.path.join(os.environ['WINDIR'], 'Fonts', 'arial.ttf'),
                os.path.join(os.environ['WINDIR'], 'Fonts', 'arialbd.ttf'),
                os.path.join(os.environ['WINDIR'], 'Fonts', 'times.ttf'),
                os.path.join(os.environ['WINDIR'], 'Fonts', 'segoeui.ttf'),
                os.path.join(os.environ['WINDIR'], 'Fonts', 'tahoma.ttf'),
            ]
        elif os.name == 'posix':
            font_paths = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
                '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
            ]
        elif os.name == 'mac':
            font_paths = [
                '/Library/Fonts/Arial.ttf',
                '/Library/Fonts/Times New Roman.ttf',
                '/System/Library/Fonts/Helvetica.ttc',
            ]
        
        for path in font_paths:
            if os.path.exists(path):
                return path
        
        return None

    def load_image(self, image_path: str) -> bool:
        try:
            self.image = cv2.imread(image_path)
            if self.image is None:
                return False
            
            self.original_image = self.image.copy()
            self.height, self.width = self.image.shape[:2]
            return True
        except Exception as e:
            print(f"помилка завантаження зображення: {e}")
            return False

    def reset_image(self) -> None:
        if self.original_image is not None:
            self.image = self.original_image.copy()

    def add_text(self, text: str, position: TextPosition, font_name: str, 
                 font_size: int, color: Tuple[int, int, int]) -> bool:
        if self.image is None:
            return False

        try:
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            draw = ImageDraw.Draw(pil_image)
            font_path = self.default_font_path
            try:
                if os.name == 'nt' and font_name in ["Arial", "Times New Roman", "Comic Sans MS", "Courier New", "Impact"]:
                    system_font = {
                        "Arial": "arial.ttf",
                        "Times New Roman": "times.ttf",
                        "Comic Sans MS": "comic.ttf",
                        "Courier New": "cour.ttf",
                        "Impact": "impact.ttf"
                    }
                    font_file = system_font.get(font_name)
                    if font_file:
                        system_path = os.path.join(os.environ['WINDIR'], 'Fonts', font_file)
                        if os.path.exists(system_path):
                            font_path = system_path
                
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                print(f"шрифт не знайдено, використовуємо стандартний")
                font = ImageFont.load_default()

            left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
            text_width = right - left
            text_height = bottom - top
            
            x = (self.width - text_width) // 2
            
            if position == TextPosition.TOP:
                y = 10
            elif position == TextPosition.BOTTOM:
                y = self.height - text_height - 10
            else:
                y = (self.height - text_height) // 2

            outline_width = max(2, font_size // 30)
            
            for offset_x, offset_y in [(-outline_width, -outline_width), 
                                       (-outline_width, outline_width), 
                                       (outline_width, -outline_width), 
                                       (outline_width, outline_width)]:
                draw.text((x + offset_x, y + offset_y), text, font=font, fill=(0, 0, 0))
            
            draw.text((x, y), text, font=font, fill=color)
            
            self.image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            return True
            
        except Exception as e:
            print(f"помилка додавання тексту: {e}")
            return False

    def apply_filter(self, filter_name: str) -> bool:
        if self.image is None:
            print("помилка: зображення не завантажено")
            return False
        
        try:
            print(f"застосовую фільтр: {filter_name}")
            
            if filter_name == "Чорно-білий":
                gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                self.image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                
            elif filter_name == "Розмиття":
                self.image = cv2.GaussianBlur(self.image, (15, 15), 0)
                
            elif filter_name == "Різкість":
                kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                self.image = cv2.filter2D(self.image, -1, kernel)
                
            elif filter_name == "Сепія":
                sepia_kernel = np.array([[0.272, 0.534, 0.131],
                                         [0.349, 0.686, 0.168],
                                         [0.393, 0.769, 0.189]])
                self.image = cv2.transform(self.image, sepia_kernel)
                
            elif filter_name == "Виділення країв":
                gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 100, 200)
                self.image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                
            elif filter_name == "Негатив":
                self.image = cv2.bitwise_not(self.image)
                
            elif filter_name == "Вінтаж":
                hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
                hsv = hsv.astype(np.float32)
                hsv[:, :, 1] = hsv[:, :, 1] * 0.6
                
                hsv[:, :, 0] = hsv[:, :, 0] * 0.8
                hsv = np.clip(hsv, 0, 255).astype(np.uint8)
                
                self.image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
                
                noise = np.zeros(self.image.shape, np.uint8)
                cv2.randu(noise, 0, 50)
                self.image = cv2.add(self.image, noise)
                
                self.image = cv2.GaussianBlur(self.image, (3, 3), 0)
            else:
                print(f"невідомий фільтр: {filter_name}")
                return False
            
            print(f"фільтр {filter_name} успішно застосовано")
            return True
            
        except Exception as e:
            print(f"помилка застосування фільтру: {e}")
            import traceback
            traceback.print_exc()
            return False

    def save_image(self, save_path: str) -> bool:
        if self.image is None:
            return False
            
        try:
            return cv2.imwrite(save_path, self.image)
        except Exception as e:
            print(f"помилка збереження зображення: {e}")
            return False

    def get_image_for_qt(self) -> np.ndarray:
        if self.image is None:
            return np.zeros((100, 100, 3), dtype=np.uint8)
            
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def resize_image(self, max_width: int, max_height: int) -> np.ndarray:
        if self.image is None:
            print("помилка: зображення не завантажено")
            return np.zeros((100, 100, 3), dtype=np.uint8)
            
        try:
            h, w = self.image.shape[:2]
            
            scale = min(max_width / w, max_height / h)
            
            if scale < 1:
                new_width = int(w * scale)
                new_height = int(h * scale)
                resized = cv2.resize(self.image, (new_width, new_height), interpolation=cv2.INTER_AREA)
                return cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            else:
                return cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"помилка зміни розміру зображення: {e}")
            import traceback
            traceback.print_exc()
            return np.zeros((100, 100, 3), dtype=np.uint8) 