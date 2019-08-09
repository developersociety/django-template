# Alignment
LEFT = "left"
CENTER = "center"
RIGHT = "right"

ALIGNMENTS = [(LEFT, "Left"), (RIGHT, "Right"), (CENTER, "Center")]

# Background colours
NONE = "none"
PRIMARY = "primary"
SECONDARY = "secondary"
GREY = "grey"

BACKGROUND_COLORS = [
    (NONE, "None"),
    (PRIMARY, "Primary"),
    (SECONDARY, "Secondary"),
    (GREY, "Grey"),
]

# Column alignment
HALVES = "halves"
LEFT_WIDE = "left-wide"
RIGHT_WIDE = "right-wide"
LEFT_WIDER = "left-wider"
RIGHT_WIDER = "right-wider"

COLUMN_ALIGNMENTS = [
    (HALVES, "Equal 50:50"),
    (LEFT_WIDE, "Wide left column 60:40"),
    (RIGHT_WIDE, "Wide right column 40:60"),
    (LEFT_WIDER, "Wider left column 70:30"),
    (RIGHT_WIDER, "Wider right column 30:70"),
]

# Button styles
BUTTON_UNSTYLED = ""
BUTTON_PRIMARY = "button"
BUTTON_SECONDARY = "button button--secondary"
BUTTON_OUTLINE = "button button--outline"

BUTTON_STYLES = [
    (BUTTON_UNSTYLED, "Unstyled button"),
    (BUTTON_PRIMARY, "Primary colour button"),
    (BUTTON_SECONDARY, "Secondary colour button"),
    (BUTTON_OUTLINE, "Outlined button"),
]
