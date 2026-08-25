"""
Cherry's Neon Orchard Dashboard - PySide6 Version
Integrated widget tab for the Jared Assistant application
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QPushButton, QGridLayout
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
import random


# Color palette for different sections
COLORS = {
    "music": "#FF6F91",
    "jokes": "#FFC75F",
    "fun_fact": "#845EC2",
    "affirmation": "#00C9A7",
    "meme": "#FF9671"
}


class FairyLightsCanvas(QWidget):
    """Canvas widget for drawing twinkling fairy lights"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)
        self.setMinimumWidth(600)
        
        # Light bulb positions
        self.light_strings_top = [
            [40, 140, 240, 340, 440, 540],
            [80, 180, 280, 380, 480],
        ]
        self.side_string_y_positions = [20, 40, 60]
        
        # Store bulb data: (x, y, current_color)
        self.bulbs = []
        self._create_bulbs()
        
        # Timer for twinkling effect
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.twinkle)
        self.timer.start(600)
    
    def _create_bulbs(self):
        """Create all bulb positions"""
        # Top bulbs
        for y_idx, positions in enumerate(self.light_strings_top, start=1):
            for x in positions:
                self.bulbs.append([x, 10 * y_idx, "#FFFAF0"])
        
        # Left side bulbs
        side_x_left = 10
        for y in self.side_string_y_positions:
            self.bulbs.append([side_x_left, y, "#FFFAF0"])
        
        # Right side bulbs
        side_x_right = 590
        for y in self.side_string_y_positions:
            self.bulbs.append([side_x_right, y, "#FFFAF0"])
    
    def twinkle(self):
        """Update bulb colors for twinkling effect"""
        for bulb in self.bulbs:
            rand_val = random.random()
            if rand_val < 0.35:
                # Randomly choose pink or white for twinkle
                bulb[2] = "#FF6F91" if random.random() < 0.5 else "#FFFFFF"
            else:
                bulb[2] = "#FFFAF0"  # Soft neutral
        
        self.update()  # Trigger repaint
    
    def paintEvent(self, event):
        """Draw all the fairy light bulbs"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        for x, y, color in self.bulbs:
            brush = QBrush(QColor(color))
            painter.setBrush(brush)
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            painter.drawEllipse(x, y, 10, 10)


class SparkleLabel(QLabel):
    """Label that sparkles by alternating colors"""
    
    def __init__(self, text, original_color, parent=None):
        super().__init__(text, parent)
        self.original_color = original_color
        self.is_white = False
        
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"""
            QLabel {{
                color: {original_color};
                font-size: 12pt;
                font-weight: bold;
                background-color: #222244;
            }}
        """)
        
        # Timer for sparkle effect
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.sparkle)
        self.timer.start(700)
    
    def sparkle(self):
        """Alternate between original color and white"""
        if self.is_white:
            color = self.original_color
        else:
            color = "white"
        
        self.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 12pt;
                font-weight: bold;
                background-color: #222244;
            }}
        """)
        
        self.is_white = not self.is_white


class WidgetSection(QFrame):
    """Individual widget section with cube border"""
    
    def __init__(self, name, color, parent=None):
        super().__init__(parent)
        self.name = name
        self.color = color
        
        self.setFixedSize(110, 110)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #222244;
                border: 4px solid {color};
                border-radius: 0px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Create sparkle label
        display_name = name.replace("_", " ").title()
        self.label = SparkleLabel(display_name, color, self)
        layout.addWidget(self.label)


class CherryWidget(QWidget):
    """Main Cherry's Neon Orchard Dashboard Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set midnight blue background
        self.setStyleSheet("""
            QWidget {
                background-color: #191A40;
            }
        """)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add fairy lights canvas
        self.fairy_lights = FairyLightsCanvas(self)
        main_layout.addWidget(self.fairy_lights)
        
        # Create grid layout for widget sections
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)
        grid_layout.setContentsMargins(8, 10, 8, 10)
        
        self.sections = {}
        
        # Add widget sections
        for i, (name, color) in enumerate(COLORS.items()):
            section = WidgetSection(name, color, self)
            grid_layout.addWidget(section, 0, i)
            self.sections[name] = section
        
        main_layout.addLayout(grid_layout)
        
        # Add music controls to the music section
        self.add_music_controls()
        
        # Add spacer at bottom
        main_layout.addStretch()
    
    def add_music_controls(self):
        """Add music control buttons to the music section"""
        music_section = self.sections["music"]
        
        # Create controls frame
        controls_frame = QWidget(music_section)
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setContentsMargins(2, 5, 2, 2)
        controls_layout.setSpacing(2)
        
        # Create buttons
        btn_play = QPushButton("▶ Play", controls_frame)
        btn_pause = QPushButton("⏸ Pause", controls_frame)
        btn_next = QPushButton("➡ Next", controls_frame)
        
        # Apply styling to buttons
        button_style = """
            QPushButton {
                background-color: #FF6F91;
                color: white;
                border: 1px solid white;
                border-radius: 3px;
                padding: 2px 6px;
                font-size: 10pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF8AA7;
            }
            QPushButton:pressed {
                background-color: #FF5577;
            }
        """
        
        for btn in (btn_play, btn_pause, btn_next):
            btn.setStyleSheet(button_style)
        
        # Connect button signals
        btn_play.clicked.connect(self.play_music)
        btn_pause.clicked.connect(self.pause_music)
        btn_next.clicked.connect(self.next_track)
        
        controls_layout.addWidget(btn_play)
        controls_layout.addWidget(btn_pause)
        controls_layout.addWidget(btn_next)
        
        # Add controls to music section layout
        music_section.layout().addWidget(controls_frame)
    
    def play_music(self):
        """Handle play button click"""
        print("▶ Play button clicked")
    
    def pause_music(self):
        """Handle pause button click"""
        print("⏸ Pause button clicked")
    
    def next_track(self):
        """Handle next button click"""
        print("➡ Next button clicked")
