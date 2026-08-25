"""
Cherry's Neon Orchard Dashboard
A delightful widget dashboard with twinkling fairy lights and sparkle effects
"""

import tkinter as tk
import random


# Color palette for different sections
colors = {
    "music": "#FF6F91",
    "jokes": "#FFC75F",
    "fun_fact": "#845EC2",
    "affirmation": "#00C9A7",
    "meme": "#FF9671"
}


class SparkleLabel(tk.Label):
    """Label that sparkles by alternating colors"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.original_color = None
        self.after(500, self.sparkle)

    def sparkle(self):
        """Alternate between original color and white"""
        current_color = self.cget("fg")
        new_color = "white" if current_color != "white" else self.original_color
        self.config(fg=new_color)
        self.after(700, self.sparkle)

    def set_original_color(self, color):
        """Set the base color for sparkling"""
        self.original_color = color
        self.config(fg=color)


def create_cube_border(frame, color):
    """Create a 3D cube-style border with the given color"""
    frame.config(
        highlightbackground=color,
        highlightthickness=4,
        bd=0,
        relief="raised"
    )


class CherrysWidget(tk.Tk):
    """Main widget dashboard window"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Cherry's Neon Orchard Dashboard")
        self.geometry("600x420")
        self.configure(bg="#191A40")  # Midnight blue background
        
        self.bulbs = []
        self.sections = {}
        
        self.create_fairy_lights()
        self.create_widget_sections()
        self.start_twinkling()
    
    def create_fairy_lights(self):
        """Create twinkling fairy lights across top and sides"""
        self.canvas = tk.Canvas(
            self,
            width=600,
            height=80,
            bg="#191A40",
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, columnspan=5)
        
        # Positions for light strings (top)
        light_strings_top = [
            [40, 140, 240, 340, 440, 540],
            [80, 180, 280, 380, 480],
        ]
        
        # Side strings hanging halfway down (about 60 px)
        side_string_y_positions = [20, 40, 60]
        
        # Draw top light bulbs
        for y, positions in enumerate(light_strings_top, start=1):
            for x in positions:
                self.make_bulb(x, 10 * y)
        
        # Draw side hanging bulbs (left)
        side_x_left = 10
        for y in side_string_y_positions:
            self.make_bulb(side_x_left, y)
        
        # Draw side hanging bulbs (right)
        side_x_right = 590
        for y in side_string_y_positions:
            self.make_bulb(side_x_right, y)
    
    def make_bulb(self, x, y):
        """Create a single light bulb"""
        bulb = self.canvas.create_oval(
            x, y, x+10, y+10,
            fill="#FFFAF0",
            outline=""
        )
        self.bulbs.append(bulb)
    
    def twinkle(self):
        """Make the fairy lights twinkle"""
        for bulb in self.bulbs:
            rand_val = random.random()
            if rand_val < 0.35:
                # Randomly choose pink or white for twinkle
                color = "#FF6F91" if random.random() < 0.5 else "#FFFFFF"
                self.canvas.itemconfig(bulb, fill=color)
            else:
                self.canvas.itemconfig(bulb, fill="#FFFAF0")  # Soft neutral
        
        self.after(600, self.twinkle)
    
    def start_twinkling(self):
        """Start the twinkling animation"""
        self.twinkle()
    
    def create_widget_sections(self):
        """Create all widget sections below the fairy lights"""
        frame_row = 1
        
        for i, (name, color) in enumerate(colors.items()):
            frame = tk.Frame(
                self,
                bg="#222244",
                width=110,
                height=110
            )
            create_cube_border(frame, color)
            frame.grid(row=frame_row, column=i, padx=8, pady=10)
            
            label = SparkleLabel(
                frame,
                text=name.replace("_", " ").title(),
                font=("Helvetica", 12, "bold"),
                bg="#222244"
            )
            label.set_original_color(color)
            label.pack(expand=True, fill="both", padx=5, pady=5)
            
            self.sections[name] = frame
        
        # Add music control buttons
        self.create_music_controls()
    
    def create_music_controls(self):
        """Create music control buttons with improved visibility"""
        control_frame = tk.Frame(self.sections["music"], bg="#222244")
        control_frame.pack(pady=5)
        
        btn_play = tk.Button(control_frame, text="▶ Play", command=self.play_music)
        btn_pause = tk.Button(control_frame, text="⏸ Pause", command=self.pause_music)
        btn_next = tk.Button(control_frame, text="➡ Next", command=self.next_track)
        
        for btn in (btn_play, btn_pause, btn_next):
            self.apply_button_style(btn)
        
        btn_play.grid(row=0, column=0, padx=2)
        btn_pause.grid(row=0, column=1, padx=2)
        btn_next.grid(row=0, column=2, padx=2)
    
    def apply_button_style(self, btn):
        """Apply consistent styling to buttons"""
        btn.config(
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg="#FF6F91",
            relief="raised",
            padx=6,
            pady=2,
            highlightthickness=1,
            highlightbackground="white",
            highlightcolor="white"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg="#FF8AA7"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#FF6F91"))
    
    def play_music(self):
        """Handle play button click"""
        print("▶ Play button clicked")
    
    def pause_music(self):
        """Handle pause button click"""
        print("⏸ Pause button clicked")
    
    def next_track(self):
        """Handle next button click"""
        print("➡ Next button clicked")


def main():
    """Main entry point for Cherry's Widget"""
    app = CherrysWidget()
    app.mainloop()


if __name__ == "__main__":
    main()
