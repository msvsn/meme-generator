import os
import random
from typing import List, Dict, Tuple, Optional
from image_processor import ImageProcessor
from utils import TextPosition, MEME_TEMPLATES


class MemeGenerator:
    def __init__(self, image_processor: ImageProcessor):
        self.image_processor = image_processor
        self.custom_texts = []
        self.templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)

    def add_text_to_meme(self, text: str, position: TextPosition, font_path: str, 
                        font_size: int, color: Tuple[int, int, int]) -> bool:
        return self.image_processor.add_text(text, position, font_path, font_size, color)
    
    def add_caption(self, top_text: str = "", bottom_text: str = "", font_path: str = "", 
                   font_size: int = 120, color: Tuple[int, int, int] = (255, 255, 255)) -> bool:
        success = True
        
        if top_text:
            success = success and self.add_text_to_meme(
                top_text, TextPosition.TOP, font_path, font_size, color
            )
            
        if bottom_text:
            success = success and self.add_text_to_meme(
                bottom_text, TextPosition.BOTTOM, font_path, font_size, color
            )
            
        return success
    
    def get_template_path(self, template_name: str) -> Optional[str]:
        template_extensions = [".jpg", ".jpeg", ".png"]
        
        for ext in template_extensions:
            path = os.path.join(self.templates_dir, f"{template_name}{ext}")
            if os.path.exists(path):
                return path
        
        return None
    
    def auto_generate_meme(self, template_name: str, custom_texts: List[str] = None) -> bool:
        template_path = self.get_template_path(template_name)
        
        if not template_path or template_name not in MEME_TEMPLATES:
            return False
        
        if not self.image_processor.load_image(template_path):
            return False
        
        template_info = MEME_TEMPLATES[template_name]
        template_positions = template_info["positions"]
        
        texts = custom_texts if custom_texts else template_info["template_text"]
        
        if len(texts) != len(template_positions):
            return False
        
        for i, (text, position) in enumerate(zip(texts, template_positions)):
            success = self.add_text_to_meme(
                text, position, "Arial.ttf", 36, (255, 255, 255)
            )
            if not success:
                return False
        
        return True
    
    def generate_random_meme(self, custom_texts: List[str] = None) -> bool:
        if not MEME_TEMPLATES:
            return False
            
        template_name = random.choice(list(MEME_TEMPLATES.keys()))
        return self.auto_generate_meme(template_name, custom_texts)
    
    def save_meme(self, output_path: str) -> bool:
        return self.image_processor.save_image(output_path) 