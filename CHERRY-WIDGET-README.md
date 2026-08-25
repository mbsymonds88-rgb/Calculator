# Cherry's Neon Orchard Dashboard 🍒

A delightful widget dashboard with twinkling fairy lights and sparkle effects, now integrated into the Jared Assistant application!

## Features

### ✨ Twinkling Fairy Lights
- Animated light bulbs across the top
- Side hanging lights that twinkle in pink and white
- Soft neutral glow with random sparkle effects
- Updates every 600ms for smooth animation

### 🎨 Sparkle Labels
- Five colorful widget sections with sparkle effects
- Labels alternate between original color and white
- Each section has a unique neon color:
  - **Music** 🎵 - Pink (#FF6F91)
  - **Jokes** 😂 - Yellow (#FFC75F)
  - **Fun Fact** 💡 - Purple (#845EC2)
  - **Affirmation** 💚 - Teal (#00C9A7)
  - **Meme** 🤪 - Orange (#FF9671)

### 🎵 Music Controls
- Play, Pause, and Next buttons
- Styled with neon pink theme
- Hover effects for better interactivity
- Located in the Music widget section

### 🌙 Midnight Blue Theme
- Beautiful dark theme (#191A40)
- Contrasts perfectly with neon colors
- Easy on the eyes for extended use

## File Structure

```
/workspace/
├── cherrys_widget.py        # Standalone tkinter version
├── cherry_tab_widget.py     # PySide6 integrated version
└── main.py                  # Updated with Cherry tab integration
```

## Usage

### Integrated Version (Recommended)

Cherry's widget is now integrated as a tab in the Jared Assistant application:

```bash
python main.py
```

Then click on the **"🍒 Cherry's Orchard"** tab to access the widget dashboard!

### Standalone Version

You can also run Cherry's widget as a standalone application:

```bash
python cherrys_widget.py
```

This version uses tkinter and runs independently of Jared Assistant.

## Integration Details

### How It Connects

1. **Import**: Cherry widget is imported in `main.py`:
   ```python
   from cherry_tab_widget import CherryWidget
   ```

2. **Tab System**: Main window now uses `QTabWidget` with two tabs:
   - **Jared Assistant Tab**: Original voice assistant interface
   - **Cherry's Orchard Tab**: New neon dashboard widget

3. **Styling**: Cherry's tab maintains its own styling while respecting the main window theme

4. **No Conflicts**: All animations and timers are self-contained within the Cherry widget

## Technical Implementation

### PySide6 Version (cherry_tab_widget.py)

**Components:**

1. **FairyLightsCanvas**: Custom QWidget that draws twinkling lights
   - Uses QPainter for drawing circles
   - QTimer for animation updates
   - Random color changes for twinkle effect

2. **SparkleLabel**: QLabel with alternating colors
   - QTimer-based sparkle animation
   - Switches between original color and white

3. **WidgetSection**: QFrame with colored borders
   - Cube-style 3D effect
   - Contains SparkleLabel
   - Fixed size for consistency

4. **CherryWidget**: Main container widget
   - Combines all components
   - Handles music button actions
   - Midnight blue background

### Tkinter Version (cherrys_widget.py)

**Components:**

1. **SparkleLabel**: Custom tk.Label subclass
   - After() method for animation
   - Alternates text color

2. **FairyLightsCanvas**: tk.Canvas for drawing lights
   - Creates oval shapes for bulbs
   - itemconfig() for color updates

3. **CherrysWidget**: Main tk.Tk window
   - Grid layout for widgets
   - Button styling and hover effects

## Customization

### Adding New Widget Sections

Edit the `COLORS` dictionary in `cherry_tab_widget.py`:

```python
COLORS = {
    "music": "#FF6F91",
    "jokes": "#FFC75F",
    "fun_fact": "#845EC2",
    "affirmation": "#00C9A7",
    "meme": "#FF9671",
    "your_section": "#YOUR_COLOR"  # Add your own!
}
```

### Changing Twinkle Speed

Modify timer intervals:

```python
# In FairyLightsCanvas.__init__()
self.timer.start(600)  # Change 600 to desired milliseconds

# In SparkleLabel.__init__()
self.timer.start(700)  # Change 700 to desired milliseconds
```

### Adjusting Light Positions

Edit bulb positions in `FairyLightsCanvas`:

```python
self.light_strings_top = [
    [40, 140, 240, 340, 440, 540],  # First row
    [80, 180, 280, 380, 480],       # Second row
]
```

### Button Actions

Implement your own music control logic in `CherryWidget`:

```python
def play_music(self):
    # Add your music player integration here
    print("▶ Play button clicked")

def pause_music(self):
    # Add pause functionality
    print("⏸ Pause button clicked")

def next_track(self):
    # Add next track functionality
    print("➡ Next button clicked")
```

## Color Palette

| Section | Hex Code | Color Name |
|---------|----------|------------|
| Music | #FF6F91 | Neon Pink |
| Jokes | #FFC75F | Bright Yellow |
| Fun Fact | #845EC2 | Purple |
| Affirmation | #00C9A7 | Teal |
| Meme | #FF9671 | Orange |
| Background | #191A40 | Midnight Blue |
| Widget BG | #222244 | Dark Purple |

## Animation Details

### Fairy Lights Twinkle
- **Interval**: 600ms
- **Effect**: 35% chance of color change per update
- **Colors**: Pink (#FF6F91), White (#FFFFFF), or Neutral (#FFFAF0)

### Label Sparkle
- **Interval**: 700ms
- **Effect**: Alternates between original color and white
- **Smooth**: Color transition every cycle

## Compatibility

### PySide6 Version
- ✅ Works with Jared Assistant
- ✅ Integrated tabbed interface
- ✅ Maintains all animations
- ✅ Consistent styling with main app

### Tkinter Version
- ✅ Standalone application
- ✅ Lighter weight
- ✅ Original design specification
- ✅ Cross-platform compatible

## Future Enhancements

Potential features to add:

- [ ] Actual music player integration (Spotify, etc.)
- [ ] Joke API integration for the jokes section
- [ ] Random fun facts generator
- [ ] Daily affirmations
- [ ] Meme viewer/generator
- [ ] Save favorite settings
- [ ] Customizable color themes
- [ ] More animation options
- [ ] Widget rearrangement
- [ ] Export/import configurations

## Troubleshooting

### Animations Not Working
- Ensure QTimer or after() methods are being called
- Check that the widget is visible
- Verify no exceptions in console

### Colors Not Displaying
- Confirm hex color codes are valid
- Check stylesheet syntax
- Verify painter setup in PySide6 version

### Integration Issues
- Ensure `cherry_tab_widget.py` is in the same directory as `main.py`
- Check import statement is correct
- Verify no circular imports

## Credits

Created as a delightful addition to the Jared Voice Assistant application. Features beautiful neon aesthetics with twinkling fairy lights and sparkle effects.

**Design Specification**: Based on Cherry's Neon Orchard concept
**Framework**: PySide6 (Qt) and tkinter
**Animation**: QTimer-based and after()-based updates
**Theme**: Midnight blue with neon accents

Enjoy the twinkling lights! ✨🍒
