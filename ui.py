import os
import sys
from typing import Dict, Tuple, List, Optional
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QLineEdit, QComboBox, QFileDialog,
                            QScrollArea, QGroupBox, QRadioButton, QSlider, QColorDialog,
                            QMessageBox, QTabWidget, QSplitter, QFrame)
from PyQt5.QtGui import QPixmap, QImage, QFont, QColor
from PyQt5.QtCore import Qt, QSize

from image_processor import ImageProcessor
from meme_generator import MemeGenerator
from utils import TextPosition, MEME_COLORS, DEFAULT_FONTS, COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT


class MemeGeneratorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.image_processor = ImageProcessor()
        self.meme_generator = MemeGenerator(self.image_processor)
        
        self.setWindowTitle("Генератор мемів")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {COLOR_PRIMARY};
                color: {COLOR_SECONDARY};
            }}
            QPushButton {{
                background-color: {COLOR_ACCENT};
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #0088cc;
            }}
            QLabel {{
                color: {COLOR_SECONDARY};
            }}
            QComboBox, QLineEdit, QSlider {{
                border: 1px solid {COLOR_ACCENT};
                border-radius: 4px;
                padding: 4px;
                background-color: #333333;
                color: white;
            }}
            QGroupBox {{
                border: 1px solid {COLOR_ACCENT};
                border-radius: 4px;
                margin-top: 10px;
                font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """)
        
        self.init_ui()
    
    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        splitter = QSplitter(Qt.Horizontal)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        self.load_btn = QPushButton("Завантажити зображення")
        self.load_btn.clicked.connect(self.load_image)
        left_layout.addWidget(self.load_btn)
        
        self.tabs = QTabWidget()
        
        text_tab = QWidget()
        text_layout = QVBoxLayout()
        
        top_text_group = QGroupBox("Верхній текст")
        top_text_layout = QVBoxLayout()
        self.top_text_input = QLineEdit()
        self.top_text_input.setPlaceholderText("Введіть верхній текст")
        top_text_layout.addWidget(self.top_text_input)
        top_text_group.setLayout(top_text_layout)
        text_layout.addWidget(top_text_group)
        
        bottom_text_group = QGroupBox("Нижній текст")
        bottom_text_layout = QVBoxLayout()
        self.bottom_text_input = QLineEdit()
        self.bottom_text_input.setPlaceholderText("Введіть нижній текст")
        bottom_text_layout.addWidget(self.bottom_text_input)
        bottom_text_group.setLayout(bottom_text_layout)
        text_layout.addWidget(bottom_text_group)
        
        font_group = QGroupBox("Налаштування шрифту")
        font_layout = QVBoxLayout()
        
        font_label = QLabel("Шрифт:")
        self.font_combo = QComboBox()
        self.font_combo.addItems(DEFAULT_FONTS)
        
        size_label = QLabel("Розмір шрифту:")
        self.font_size_slider = QSlider(Qt.Horizontal)
        self.font_size_slider.setMinimum(20)
        self.font_size_slider.setMaximum(500)
        self.font_size_slider.setValue(120)
        self.font_size_label = QLabel("120")
        self.font_size_slider.valueChanged.connect(
            lambda value: self.font_size_label.setText(str(value))
        )
        
        color_label = QLabel("Колір:")
        self.color_combo = QComboBox()
        for color_name in MEME_COLORS.keys():
            self.color_combo.addItem(color_name)
        
        custom_color_btn = QPushButton("Користувацький колір")
        custom_color_btn.clicked.connect(self.choose_custom_color)
        self.custom_color = QColor(255, 255, 255)
        
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_combo)
        font_layout.addWidget(size_label)
        font_layout.addWidget(self.font_size_slider)
        font_layout.addWidget(self.font_size_label)
        font_layout.addWidget(color_label)
        font_layout.addWidget(self.color_combo)
        font_layout.addWidget(custom_color_btn)
        font_group.setLayout(font_layout)
        text_layout.addWidget(font_group)
        
        self.add_text_btn = QPushButton("Додати текст")
        self.add_text_btn.clicked.connect(self.add_text)
        text_layout.addWidget(self.add_text_btn)
        
        text_tab.setLayout(text_layout)
        self.tabs.addTab(text_tab, "Додати текст")
        
        filters_tab = QWidget()
        filters_layout = QVBoxLayout()
        
        filters_group = QGroupBox("Фільтри зображення")
        filters_group_layout = QVBoxLayout()
        
        self.filters_combo = QComboBox()
        self.filters_combo.addItems([
            "Оригінал", "Чорно-білий", "Розмиття", "Різкість", 
            "Сепія", "Виділення країв", "Негатив", "Вінтаж"
        ])
        
        apply_filter_btn = QPushButton("Застосувати фільтр")
        apply_filter_btn.clicked.connect(self.apply_filter)
        
        filters_group_layout.addWidget(QLabel("Виберіть фільтр:"))
        filters_group_layout.addWidget(self.filters_combo)
        filters_group_layout.addWidget(apply_filter_btn)
        filters_group.setLayout(filters_group_layout)
        filters_layout.addWidget(filters_group)
        
        filters_tab.setLayout(filters_layout)
        self.tabs.addTab(filters_tab, "Фільтри")
        
        left_layout.addWidget(self.tabs)
        
        nav_buttons_layout = QHBoxLayout()
        
        self.text_tab_btn = QPushButton("Додати текст")
        self.text_tab_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(0))
        nav_buttons_layout.addWidget(self.text_tab_btn)
        
        self.filters_tab_btn = QPushButton("Фільтри")
        self.filters_tab_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        nav_buttons_layout.addWidget(self.filters_tab_btn)
        
        left_layout.addLayout(nav_buttons_layout)
        
        buttons_layout = QHBoxLayout()
        
        self.reset_btn = QPushButton("Скинути")
        self.reset_btn.clicked.connect(self.reset_image)
        buttons_layout.addWidget(self.reset_btn)
        
        self.save_btn = QPushButton("Зберегти")
        self.save_btn.clicked.connect(self.save_image)
        buttons_layout.addWidget(self.save_btn)
        
        left_layout.addLayout(buttons_layout)
        left_panel.setLayout(left_layout)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        preview_label = QLabel("Попередній перегляд:")
        right_layout.addWidget(preview_label)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 400)
        self.image_label.setStyleSheet("border: 2px dashed #888888;")
        self.image_label.setText("Завантажте зображення для початку роботи")
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.image_label)
        scroll_area.setWidgetResizable(True)
        right_layout.addWidget(scroll_area)
        
        right_panel.setLayout(right_layout)
        
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Відкрити зображення", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            if self.image_processor.load_image(file_path):
                self.update_preview()
                print(f"Зображення успішно завантажено: {file_path}")
            else:
                QMessageBox.critical(self, "Помилка", "Не вдалося завантажити зображення")
    
    def update_preview(self):
        if self.image_processor.image is not None:
            try:
                rgb_image = self.image_processor.resize_image(800, 600)
                
                h, w, ch = rgb_image.shape
                q_img = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
                
                pixmap = QPixmap.fromImage(q_img)
                self.image_label.setPixmap(pixmap)
                self.image_label.setMinimumSize(1, 1)
                print("Попередній перегляд оновлено")
            except Exception as e:
                print(f"Помилка оновлення попереднього перегляду: {e}")
                QMessageBox.critical(self, "Помилка", f"Помилка оновлення попереднього перегляду: {e}")
    
    def get_selected_color(self) -> Tuple[int, int, int]:
        color_name = self.color_combo.currentText()
        
        if color_name in MEME_COLORS:
            return MEME_COLORS[color_name]
        
        return (self.custom_color.red(), self.custom_color.green(), self.custom_color.blue())
    
    def choose_custom_color(self):
        color = QColorDialog.getColor(initial=self.custom_color, parent=self)
        
        if color.isValid():
            self.custom_color = color
            custom_index = self.color_combo.findText("Користувацький")
            
            if custom_index == -1:
                self.color_combo.addItem("Користувацький")
                self.color_combo.setCurrentIndex(self.color_combo.count() - 1)
            else:
                self.color_combo.setCurrentIndex(custom_index)
    
    def add_text(self):
        if self.image_processor.image is None:
            QMessageBox.warning(self, "Попередження", "Спочатку завантажте зображення")
            return
        
        top_text = self.top_text_input.text()
        bottom_text = self.bottom_text_input.text()
        
        if not top_text and not bottom_text:
            QMessageBox.warning(self, "Попередження", "Введіть текст для додавання")
            return
        
        self.image_processor.reset_image()
        
        font = self.font_combo.currentText()
        font_size = self.font_size_slider.value()
        color = self.get_selected_color()
        
        self.meme_generator.add_caption(
            top_text=top_text,
            bottom_text=bottom_text,
            font_path=font,
            font_size=font_size,
            color=color
        )
        
        self.update_preview()
    
    def apply_filter(self):
        if self.image_processor.image is None:
            QMessageBox.warning(self, "Попередження", "Спочатку завантажте зображення")
            return
        
        filter_name = self.filters_combo.currentText()
        print(f"Застосовую фільтр: {filter_name}")
        
        self.image_processor.reset_image()
        
        if filter_name != "Оригінал":
            success = self.image_processor.apply_filter(filter_name)
            if success:
                print(f"Фільтр {filter_name} успішно застосовано")
            else:
                print(f"Помилка застосування фільтру {filter_name}")
                QMessageBox.warning(self, "Помилка", f"Не вдалося застосувати фільтр {filter_name}")
                return
        
        self.update_preview()
    
    def reset_image(self):
        if self.image_processor.image is not None:
            self.image_processor.reset_image()
            self.update_preview()
            print("Зображення скинуто до оригінального")
    
    def save_image(self):
        if self.image_processor.image is None:
            QMessageBox.warning(self, "Попередження", "Немає зображення для збереження")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Зберегти зображення", "", "PNG (*.png);;JPEG (*.jpg *.jpeg);;All Files (*)"
        )
        
        if file_path:
            if self.image_processor.save_image(file_path):
                QMessageBox.information(self, "Успіх", "Зображення успішно збережено")
                print(f"Зображення збережено: {file_path}")
            else:
                QMessageBox.critical(self, "Помилка", "Не вдалося зберегти зображення")
                print(f"Помилка збереження зображення: {file_path}") 