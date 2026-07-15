#!/usr/bin/env python3
"""
AgriBot UGV - Industrial EE Drawing Pack
Generates clean, monochrome engineering diagrams in PDF.
Style: Siemens / ABB / Schneider Electric technical documentation.

Output: AgriBot_EE_Drawing_Pack.pdf (multi-page)
"""

from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import os
import sys

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "AgriBot_EE_Drawing_Pack.pdf")

W, H = landscape(A3)  # 420 x 297 mm

# Consistent styling
BORDER = 12 * mm
TITLE_BLOCK_H = 22 * mm
DRAW_LEFT = BORDER + 2 * mm
DRAW_RIGHT = W - BORDER - 2 * mm
DRAW_TOP = H - BORDER - 2 * mm
DRAW_BOTTOM = BORDER + TITLE_BLOCK_H + 4 * mm

# Fonts
FONT = "Helvetica"
FONT_B = "Helvetica-Bold"

# Colors
BLACK = (0, 0, 0)
DGRAY = (0.25, 0.25, 0.25)
MGRAY = (0.50, 0.50, 0.50)
LGRAY = (0.75, 0.75, 0.75)
VLGRAY = (0.90, 0.90, 0.90)
WHITE = (1, 1, 1)


class EEDrawing:
    """Base class for engineering drawing pages."""

    def __init__(self, c):
        self.c = c

    # ── Drawing primitives ──────────────────────────────────────────

    def draw_border(self):
        c = self.c
        # Outer border
        c.setStrokeColorRGB(*BLACK)
        c.setLineWidth(1.5)
        c.rect(BORDER, BORDER, W - 2 * BORDER, H - 2 * BORDER)
        # Inner border
        c.setLineWidth(0.5)
        c.rect(BORDER + 1.5 * mm, BORDER + 1.5 * mm,
               W - 2 * BORDER - 3 * mm, H - 2 * BORDER - 3 * mm)

    def draw_title_block(self, project, document, sheet, total_sheets,
                         rev, title, status, date):
        c = self.c
        x0 = W - BORDER - 1.5 * mm
        y0 = BORDER + 1.5 * mm
        bw = 160 * mm
        bh = TITLE_BLOCK_H

        x_left = x0 - bw
        y_top = y0 + bh

        c.setLineWidth(0.8)
        c.setStrokeColorRGB(*BLACK)
        # Outer box
        c.rect(x_left, y0, bw, bh)

        # Horizontal dividers
        c.line(x_left, y0 + bh / 2, x0, y0 + bh / 2)

        # Vertical dividers - top row
        col_w = bw / 4
        for i in range(1, 4):
            c.line(x_left + i * col_w, y0 + bh / 2,
                   x_left + i * col_w, y_top)

        # Vertical dividers - bottom row
        c.line(x_left + bw * 0.55, y0, x_left + bw * 0.55, y0 + bh / 2)

        # Labels (top row)
        c.setFont(FONT, 6)
        c.setFillColorRGB(*MGRAY)
        c.drawString(x_left + 2 * mm, y_top - 4 * mm, "PROJECT")
        c.drawString(x_left + col_w + 2 * mm, y_top - 4 * mm, "DOCUMENT")
        c.drawString(x_left + 2 * col_w + 2 * mm, y_top - 4 * mm, "SHEET")
        c.drawString(x_left + 3 * col_w + 2 * mm, y_top - 4 * mm, "REV")

        # Values (top row)
        c.setFont(FONT_B, 9)
        c.setFillColorRGB(*BLACK)
        c.drawString(x_left + 2 * mm, y_top - 9.5 * mm, project)
        c.setFont(FONT, 8)
        c.drawString(x_left + col_w + 2 * mm, y_top - 9.5 * mm, document)
        c.drawString(x_left + 2 * col_w + 2 * mm, y_top - 9.5 * mm,
                     f"{sheet}/{total_sheets}")
        c.drawString(x_left + 3 * col_w + 2 * mm, y_top - 9.5 * mm, rev)

        # Labels (bottom row)
        c.setFont(FONT, 6)
        c.setFillColorRGB(*MGRAY)
        c.drawString(x_left + 2 * mm, y0 + bh / 2 - 4 * mm, "TITLE")
        c.drawString(x_left + bw * 0.55 + 2 * mm, y0 + bh / 2 - 4 * mm,
                     "STATUS")

        # Values (bottom row)
        c.setFont(FONT_B, 8)
        c.setFillColorRGB(*BLACK)
        c.drawString(x_left + 2 * mm, y0 + 2 * mm, title)
        c.setFont(FONT, 7)
        c.drawString(x_left + bw * 0.55 + 2 * mm, y0 + 2 * mm, status)

        # Date
        c.setFont(FONT, 6)
        c.setFillColorRGB(*MGRAY)
        c.drawString(x_left + bw * 0.55 + 2 * mm, y0 + bh / 2 - 9.5 * mm,
                     f"DATE: {date}")

        # Note at bottom left
        c.setFont(FONT, 5.5)
        c.setFillColorRGB(*MGRAY)
        c.drawString(BORDER + 4 * mm, BORDER + 3 * mm,
                     "Note: Concept-level drawing for prototype development. "
                     "Verify ratings, pinout, wire gauge and fusing before "
                     "energizing hardware.")

    def draw_page_title(self, title, subtitle=""):
        c = self.c
        c.setFont(FONT_B, 16)
        c.setFillColorRGB(*BLACK)
        c.drawString(DRAW_LEFT + 3 * mm, DRAW_TOP - 8 * mm, title)
        if subtitle:
            c.setFont(FONT, 8)
            c.setFillColorRGB(*DGRAY)
            c.drawString(DRAW_LEFT + 3 * mm, DRAW_TOP - 14 * mm, subtitle)
        # Separator line
        c.setStrokeColorRGB(*BLACK)
        c.setLineWidth(0.8)
        y = DRAW_TOP - 17 * mm
        c.line(DRAW_LEFT + 2 * mm, y, DRAW_RIGHT - 2 * mm, y)
        # Right side label
        c.setFont(FONT, 7)
        c.setFillColorRGB(*MGRAY)
        c.drawRightString(DRAW_RIGHT - 3 * mm, DRAW_TOP - 8 * mm,
                          "Industrial EE Documentation Format")

    def block(self, x, y, w, h, label, ref="", details=None,
              bold_label=True, line_w=0.8, fill=None):
        """Draw a labeled block with optional reference designator."""
        c = self.c
        c.setLineWidth(line_w)
        c.setStrokeColorRGB(*BLACK)
        if fill:
            c.setFillColorRGB(*fill)
            c.rect(x, y, w, h, stroke=1, fill=1)
        else:
            c.rect(x, y, w, h)

        # Reference designator (top-right corner)
        if ref:
            c.setFont(FONT_B, 7)
            c.setFillColorRGB(*BLACK)
            c.drawRightString(x + w - 2 * mm, y + h - 5 * mm, ref)

        # Label
        if bold_label:
            c.setFont(FONT_B, 9)
        else:
            c.setFont(FONT, 9)
        c.setFillColorRGB(*BLACK)
        c.drawString(x + 3 * mm, y + h - 6 * mm, label)

        # Details
        if details:
            c.setFont(FONT, 7)
            c.setFillColorRGB(*DGRAY)
            for i, line in enumerate(details):
                c.drawString(x + 3 * mm, y + h - 12 * mm - i * 8,
                             line)

    def notes_block(self, x, y, w, title, notes, label_tag=""):
        """Draw a notes/rules box."""
        c = self.c
        line_h = 9
        h = 12 * mm + len(notes) * line_h

        c.setLineWidth(0.6)
        c.setStrokeColorRGB(*BLACK)
        c.rect(x, y, w, h)

        # Title bar
        c.setFont(FONT_B, 8)
        c.setFillColorRGB(*BLACK)
        c.drawString(x + 3 * mm, y + h - 5 * mm, title)
        if label_tag:
            c.setFont(FONT_B, 7)
            c.drawRightString(x + w - 2 * mm, y + h - 5 * mm, label_tag)
        c.setLineWidth(0.4)
        c.line(x, y + h - 7 * mm, x + w, y + h - 7 * mm)

        # Notes
        c.setFont(FONT, 6.5)
        c.setFillColorRGB(*DGRAY)
        for i, note in enumerate(notes):
            c.drawString(x + 3 * mm,
                         y + h - 7 * mm - 4 * mm - i * line_h, note)
        return h

    def arrow_h(self, x1, y, x2, label="", above=True):
        """Horizontal arrow with optional label."""
        c = self.c
        c.setStrokeColorRGB(*BLACK)
        c.setLineWidth(0.6)
        c.line(x1, y, x2, y)
        # Arrowhead
        d = 2.2 * mm
        if x2 > x1:
            c.line(x2, y, x2 - d, y + d * 0.5)
            c.line(x2, y, x2 - d, y - d * 0.5)
        else:
            c.line(x2, y, x2 + d, y + d * 0.5)
            c.line(x2, y, x2 + d, y - d * 0.5)
        if label:
            c.setFont(FONT, 6)
            c.setFillColorRGB(*DGRAY)
            mid = (x1 + x2) / 2
            if above:
                c.drawCentredString(mid, y + 2 * mm, label)
            else:
                c.drawCentredString(mid, y - 4 * mm, label)

    def arrow_v(self, x, y1, y2, label="", right=True):
        """Vertical arrow with optional label."""
        c = self.c
        c.setStrokeColorRGB(*BLACK)
        c.setLineWidth(0.6)
        c.line(x, y1, x, y2)
        d = 2.2 * mm
        if y2 < y1:
            c.line(x, y2, x - d * 0.5, y2 + d)
            c.line(x, y2, x + d * 0.5, y2 + d)
        else:
            c.line(x, y2, x - d * 0.5, y2 - d)
            c.line(x, y2, x + d * 0.5, y2 - d)
        if label:
            c.setFont(FONT, 6)
            c.setFillColorRGB(*DGRAY)
            mid = (y1 + y2) / 2
            if right:
                c.drawString(x + 2 * mm, mid, label)
            else:
                c.drawRightString(x - 2 * mm, mid, label)

    def line_h(self, x1, y, x2, dashed=False):
        c = self.c
        c.setStrokeColorRGB(*BLACK)
        c.setLineWidth(0.6)
        if dashed:
            c.setDash(3, 2)
        c.line(x1, y, x2, y)
        c.setDash()

    def line_v(self, x, y1, y2, dashed=False):
        c = self.c
        c.setStrokeColorRGB(*BLACK)
        c.setLineWidth(0.6)
        if dashed:
            c.setDash(3, 2)
        c.line(x, y1, x, y2)
        c.setDash()

    def dot(self, x, y, r=1.2):
        """Junction dot."""
        c = self.c
        c.setFillColorRGB(*BLACK)
        c.circle(x, y, r * mm, stroke=0, fill=1)

    def fuse_symbol(self, x, y, w=12*mm, label=""):
        """Draw IEC fuse symbol (rectangle with line through)."""
        c = self.c
        c.setLineWidth(0.6)
        c.setStrokeColorRGB(*BLACK)
        fh = 4 * mm
        c.rect(x, y - fh/2, w, fh)
        c.line(x, y, x + w, y)
        if label:
            c.setFont(FONT, 6)
            c.setFillColorRGB(*BLACK)
            c.drawCentredString(x + w/2, y + fh/2 + 1.5*mm, label)

    def switch_symbol(self, x, y, label=""):
        """Draw simple switch symbol."""
        c = self.c
        c.setLineWidth(0.6)
        c.setStrokeColorRGB(*BLACK)
        r = 1.2 * mm
        c.circle(x, y, r, stroke=1, fill=0)
        c.circle(x + 10*mm, y, r, stroke=1, fill=0)
        c.line(x + r, y + r*0.3, x + 10*mm - r, y + 3*mm)
        if label:
            c.setFont(FONT, 6)
            c.setFillColorRGB(*BLACK)
            c.drawCentredString(x + 5*mm, y + 5*mm, label)

    def motor_symbol(self, cx, cy, r=6*mm, label="M"):
        """Draw IEC motor symbol (circle with M)."""
        c = self.c
        c.setLineWidth(0.8)
        c.setStrokeColorRGB(*BLACK)
        c.circle(cx, cy, r, stroke=1, fill=0)
        c.setFont(FONT_B, 10)
        c.setFillColorRGB(*BLACK)
        c.drawCentredString(cx, cy - 3, label)

    def ground_symbol(self, x, y):
        """Draw IEC ground symbol."""
        c = self.c
        c.setLineWidth(0.6)
        c.setStrokeColorRGB(*BLACK)
        w = 8 * mm
        c.line(x - w/2, y, x + w/2, y)
        c.line(x - w/3, y - 2*mm, x + w/3, y - 2*mm)
        c.line(x - w/6, y - 4*mm, x + w/6, y - 4*mm)

    def dashed_zone(self, x, y, w, h, label=""):
        """Draw a dashed boundary zone."""
        c = self.c
        c.setStrokeColorRGB(*LGRAY)
        c.setLineWidth(0.5)
        c.setDash(4, 3)
        c.rect(x, y, w, h)
        c.setDash()
        if label:
            c.setFont(FONT_B, 7)
            c.setFillColorRGB(*MGRAY)
            c.drawString(x + 2*mm, y + h - 4*mm, label)


# ════════════════════════════════════════════════════════════════════
#  SHEET 1: V1 System Architecture
# ════════════════════════════════════════════════════════════════════

def draw_sheet_01(c):
    d = EEDrawing(c)
    d.draw_border()
    d.draw_page_title(
        "V1 System Architecture",
        "Teleoperation-first electrical concept, no CAN in V1"
    )
    d.draw_title_block("AgriBot UGV", "AGB-EE-DRW-001", "01", "08",
                       "A", "V1 System Architecture",
                       "PRELIMINARY / ENGINEERING CONCEPT", "2026-05-23")

    # ── Layout constants ──
    top = DRAW_TOP - 25 * mm
    col1 = DRAW_LEFT + 10 * mm    # Power domain
    col2 = DRAW_LEFT + 155 * mm   # Control domain
    col3 = DRAW_LEFT + 310 * mm   # Perception domain
    bw = 58 * mm
    bh = 22 * mm

    # ── Domain headers ──
    c.setFont(FONT_B, 9)
    c.setFillColorRGB(*BLACK)
    c.drawString(col1, top + 3*mm,
                 "POWER DOMAIN - 36 V / high current")
    c.drawString(col2, top + 3*mm,
                 "CONTROL DOMAIN - real-time embedded")
    c.drawString(col3, top + 3*mm,
                 "PERCEPTION / COMPUTE")
    c.setLineWidth(0.3)
    c.setStrokeColorRGB(*LGRAY)
    # Domain separator lines
    sep1 = col2 - 8*mm
    sep2 = col3 - 8*mm
    c.line(sep1, top + 7*mm, sep1, DRAW_BOTTOM + 5*mm)
    c.line(sep2, top + 7*mm, sep2, DRAW_BOTTOM + 5*mm)

    # ── Power Domain ──
    # Battery
    by = top - 30*mm
    d.block(col1, by, bw, bh, "B1 Battery Pack", "B1",
            ["Hoverboard battery", "36 V nominal", "BMS internal"])

    # Fuse + switch
    fy = by - 25*mm
    d.fuse_symbol(col1 + 10*mm, fy, label="F1 main")
    d.line_v(col1 + bw/2, by, fy + 2*mm)

    sy = fy - 20*mm
    d.switch_symbol(col1 + 14*mm, sy, label="QS1 master")

    # Protection block
    py = sy - 35*mm
    d.block(col1, py, bw, 24*mm, "Protection", "F1/QS1",
            ["F1 main fuse", "QS1 master switch",
             "S0 E-stop", "K1 motor cutoff"])

    # DC/DC converters
    dcy1 = py - 30*mm
    d.block(col1, dcy1, bw, bh, "DC/DC 5.1 V", "U1",
            ["Pi 5 supply", ">= 5 A"])

    dcy2 = dcy1 - 28*mm
    d.block(col1, dcy2, bw, bh, "DC/DC 5 V", "U2",
            ["36 V fused", "g/c supply",
             "STM32 + RX"])

    # Lines from protection to DC/DCs
    px_out = col1 + bw
    d.line_h(px_out, py + 16*mm, px_out + 10*mm)
    d.line_v(px_out + 10*mm, py + 16*mm, dcy1 + bh/2)
    d.arrow_h(px_out + 10*mm, dcy1 + bh/2, col1 + bw, label="36 V fused")
    # actually let me just connect cleanly
    d.line_v(col1 + bw/2, py, dcy1 + bh)
    d.line_v(col1 + bw/2, dcy1, dcy2 + bh)

    # ── Control Domain ──
    # FlySky Receiver
    ry = top - 30*mm
    d.block(col2, ry, bw + 10*mm, 28*mm, "FlySky Receiver", "A1",
            ["CH1 steering", "CH2 throttle",
             "CH5 arm", "CH6 mode"])

    # STM32 Nucleo
    sy2 = ry - 55*mm
    stm_w = bw + 20*mm
    stm_h = 36*mm
    d.block(col2, sy2, stm_w, stm_h, "STM32F767 Nucleo", "A2",
            ["vehicle control unit", "state machine",
             "RC failsafe", "PWM generation"])
    # Line from receiver to STM32
    d.arrow_v(col2 + 20*mm, ry, sy2 + stm_h, label="PWM/PPM/iBUS")

    # Left ZS-X11H
    lzy = sy2 - 35*mm
    d.block(col2, lzy, bw, bh, "Left ZS-X11H", "Q1",
            ["PWM/DIR/STOP", "BLDC + Hall"])

    # Right ZS-X11H
    rzy = lzy - 28*mm
    d.block(col2, rzy, bw, bh, "Right ZS-X11H", "Q2",
            ["PWM/DIR/STOP", "BLDC + Hall"])

    # STM32 to drivers
    d.arrow_v(col2 + 15*mm, sy2, lzy + bh, label="PWM")
    d.arrow_v(col2 + 35*mm, sy2, rzy + bh + 28*mm)
    d.line_v(col2 + 35*mm, rzy + bh + 28*mm, rzy + bh)

    # ── Perception Domain ──
    # Raspberry Pi 5
    rpy = top - 30*mm
    d.block(col3, rpy, bw + 10*mm, 28*mm, "Raspberry Pi 5", "A3",
            ["V1: logging", "future vision/EKF"])

    # Camera
    camy = rpy - 30*mm
    d.block(col3, camy, bw, bh, "Night Vision Camera", "B2",
            ["RGB/IR", "front mounted"])

    # Pi to camera
    d.arrow_v(col3 + 20*mm, rpy, camy + bh, label="USB/CSI")

    # STM32 to Pi link
    stm_right = col2 + stm_w
    pi_left = col3
    mid_y = sy2 + stm_h/2
    d.line_h(stm_right, mid_y, pi_left, dashed=True)
    c.setFont(FONT, 6)
    c.setFillColorRGB(*DGRAY)
    c.drawCentredString((stm_right + pi_left)/2, mid_y + 2.5*mm,
                        "future cmd_vel/log")

    # ── Actuators (bottom) ──
    # Motors
    moty = DRAW_BOTTOM + 20*mm
    motw = bw + 5*mm
    moth = 20*mm
    d.block(col2 + 80*mm, moty + 28*mm, motw, moth,
            "Left Drive Wheel", "M1",
            ["hoverboard BLDC", "fixed front wheel"])
    d.block(col2 + 80*mm, moty, motw, moth,
            "Right Drive Wheel", "M2",
            ["hoverboard BLDC", "fixed front wheel"])

    # ZS-X11H to motors
    mot_left_x = col2 + 80*mm
    d.arrow_h(col2 + bw, lzy + bh/2, mot_left_x,
              label="phase + hall")
    d.arrow_h(col2 + bw, rzy + bh/2, mot_left_x,
              label="phase + hall")

    # Rear casters
    d.block(col1, moty, bw, moth, "Rear Caster Wheels", "MECH",
            ["passive support", "swivel casters",
             "no electrical drive"])

    # ── Operator ──
    d.block(col3 + 20*mm, moty, bw, moth, "Operator", "HMI",
            ["RC handset", "manual override"])

    # FlySky wireless link
    c.setFont(FONT, 6)
    c.setFillColorRGB(*DGRAY)
    c.drawString(col3 + 25*mm, moty + moth + 3*mm, "RC 2.4 GHz")
    d.line_v(col3 + 45*mm, moty + moth, ry, dashed=True)
    # connect to receiver block area
    d.line_h(col3 + 45*mm, ry + 14*mm, col2 + bw + 10*mm, dashed=True)

    # ── Legend ──
    lx = DRAW_LEFT + 10*mm
    ly = DRAW_BOTTOM + 5*mm
    d.notes_block(lx, ly, 65*mm, "Signal Legend", [
        "solid line: required V1 connection",
        "dashed line: data or future path",
        "Power switching must default to",
        "motor-disabled on reset.",
    ], "")

    d.notes_block(lx + 72*mm, ly, 75*mm, "Design Rule", [
        "STM32 is the safety authority.",
        "Raspberry Pi requests motion only",
        "in future AUTO mode.",
        "E-stop removes motor power and",
        "leaves logic alive for diagnostics.",
    ], "")


# ════════════════════════════════════════════════════════════════════
#  SHEET 2: Power Distribution Single-Line Diagram
# ════════════════════════════════════════════════════════════════════

def draw_sheet_02(c):
    d = EEDrawing(c)
    d.draw_border()
    d.draw_page_title(
        "Power Distribution Single-Line Diagram",
        "36 V battery system, separated motor and logic branches"
    )
    d.draw_title_block("AgriBot UGV", "AGB-EE-DRW-001", "02", "08",
                       "A", "Power Distribution Single-Line Diagram",
                       "PRELIMINARY / ENGINEERING CONCEPT", "2026-05-23")

    top = DRAW_TOP - 30*mm

    # ── Positive distribution (left to right) ──
    c.setFont(FONT_B, 9)
    c.setFillColorRGB(*BLACK)
    c.drawString(DRAW_LEFT + 5*mm, top + 5*mm, "Positive distribution")

    # Battery
    bat_x = DRAW_LEFT + 10*mm
    bat_y = top - 25*mm
    d.block(bat_x, bat_y, 42*mm, 22*mm, "B1", "",
            ["36 V hoverboard", "battery + BMS"])

    # Main bus line
    bus_y = bat_y + 11*mm
    bus_start = bat_x + 42*mm

    # F1 main fuse
    f1_x = bus_start + 10*mm
    d.fuse_symbol(f1_x, bus_y, label="F1 main")
    d.line_h(bus_start, bus_y, f1_x)

    # QS1 master switch
    qs1_x = f1_x + 18*mm
    d.switch_symbol(qs1_x, bus_y, label="QS1")
    d.line_h(f1_x + 12*mm, bus_y, qs1_x)

    # ── Emergency stop chain ──
    estop_x = qs1_x + 25*mm
    estop_y = top - 5*mm
    d.block(estop_x, estop_y, 52*mm, 22*mm,
            "Emergency Stop Chain", "S0/K1",
            ["S0 E-stop NC", "K1 contactor coil",
             "manual reset"])
    d.line_h(qs1_x + 10*mm, bus_y, estop_x + 10*mm)
    d.line_v(estop_x + 10*mm, bus_y, estop_y)

    # K1 contactor
    k1_x = estop_x + 52*mm + 12*mm
    k1_y = bus_y - 2*mm
    c.setFont(FONT_B, 8)
    c.setFillColorRGB(*BLACK)
    c.drawCentredString(k1_x + 5*mm, k1_y + 10*mm, "K1")
    # Contactor symbol
    c.setLineWidth(0.6)
    c.setStrokeColorRGB(*BLACK)
    c.circle(k1_x, k1_y + 4*mm, 1.5*mm, stroke=1, fill=0)
    c.circle(k1_x + 10*mm, k1_y + 4*mm, 1.5*mm, stroke=1, fill=0)
    c.line(k1_x + 1.5*mm, k1_y + 5*mm, k1_x + 8.5*mm, k1_y + 8*mm)
    d.line_h(estop_x + 26*mm, estop_y, k1_x - 3*mm)
    d.line_v(k1_x - 3*mm, estop_y, k1_y + 4*mm)

    # 36 V MOTOR BUS
    motor_bus_x = k1_x + 20*mm
    motor_bus_end = DRAW_RIGHT - 30*mm
    c.setFont(FONT_B, 8)
    c.setFillColorRGB(*BLACK)
    c.drawString(motor_bus_x + 5*mm, bus_y + 5*mm,
                 "36 V MOTOR BUS - switched")
    c.setLineWidth(1.2)
    c.setStrokeColorRGB(*BLACK)
    c.line(k1_x + 10*mm, k1_y + 4*mm, motor_bus_x, bus_y)
    c.line(motor_bus_x, bus_y, motor_bus_end, bus_y)
    c.setLineWidth(0.6)

    # ── Motor branch fuses ──
    # F2 left drive
    f2_x = motor_bus_end - 80*mm
    f2_y = bus_y - 30*mm
    d.dot(f2_x + 6*mm, bus_y)
    d.line_v(f2_x + 6*mm, bus_y, f2_y + 5*mm)
    d.fuse_symbol(f2_x, f2_y, label="F2 Left drive")

    # Q1 Left ZS-X11H
    q1_x = f2_x - 5*mm
    q1_y = f2_y - 28*mm
    d.block(q1_x, q1_y, 50*mm, 20*mm, "Q1 ZS-X11H", "",
            ["BLDC power stage", "phase output"])
    d.line_v(f2_x + 6*mm, f2_y - 2*mm, q1_y + 20*mm)

    # M1 left motor
    m1_x = q1_x + 55*mm
    m1_y = q1_y + 5*mm
    d.motor_symbol(m1_x + 8*mm, m1_y + 5*mm, label="M1")
    c.setFont(FONT, 6)
    c.setFillColorRGB(*DGRAY)
    c.drawString(m1_x - 2*mm, m1_y - 6*mm, "M1 Left motor")
    d.arrow_h(q1_x + 50*mm, q1_y + 10*mm, m1_x)

    # F3 right drive
    f3_x = motor_bus_end - 15*mm
    f3_y = f2_y
    d.dot(f3_x + 6*mm, bus_y)
    d.line_v(f3_x + 6*mm, bus_y, f3_y + 5*mm)
    d.fuse_symbol(f3_x, f3_y, label="F3 Right drive")

    # Q2 Right ZS-X11H
    q2_x = f3_x - 5*mm
    q2_y = f3_y - 28*mm
    d.block(q2_x, q2_y, 50*mm, 20*mm, "Q2 ZS-X11H", "",
            ["BLDC power stage", "phase output"])
    d.line_v(f3_x + 6*mm, f3_y - 2*mm, q2_y + 20*mm)

    # M2 right motor
    m2_x = q2_x + 55*mm
    m2_y = q2_y + 5*mm
    d.motor_symbol(m2_x + 8*mm, m2_y + 5*mm, label="M2")
    c.setFont(FONT, 6)
    c.setFillColorRGB(*DGRAY)
    c.drawString(m2_x - 2*mm, m2_y - 6*mm, "M2 Right motor")
    d.arrow_h(q2_x + 50*mm, q2_y + 10*mm, m2_x)

    # ── Logic bus (unswitched after QS1, before E-stop) ──
    logic_y = q2_y - 35*mm
    c.setFont(FONT_B, 8)
    c.setFillColorRGB(*BLACK)
    c.drawString(DRAW_LEFT + 10*mm, logic_y + 28*mm,
                 "36 V LOGIC BUS - unswitched after QS1")

    # Tap point from main bus before K1
    tap_x = qs1_x + 15*mm
    d.dot(tap_x, bus_y)
    d.line_v(tap_x, bus_y, logic_y + 22*mm)

    # U1 Pi buck
    u1_x = tap_x + 20*mm
    u1_y = logic_y + 5*mm
    d.block(u1_x, u1_y, 50*mm, 18*mm, "U1  36->5.1 V", "U1",
            ["isolated preferred", "low ripple"])
    d.line_h(tap_x, logic_y + 14*mm, u1_x)

    # F4 pi fuse
    f4_x = tap_x + 2*mm
    d.fuse_symbol(f4_x, logic_y + 14*mm, 10*mm, "F4")

    # A3 Raspberry Pi
    a3_x = u1_x + 58*mm
    d.arrow_h(u1_x + 50*mm, u1_y + 9*mm, a3_x)
    c.setFont(FONT, 7)
    c.setFillColorRGB(*BLACK)
    c.drawString(a3_x + 2*mm, u1_y + 9*mm - 2, "A3 Raspberry Pi 5")

    # U2 logic buck
    u2_x = u1_x
    u2_y = u1_y - 25*mm
    d.block(u2_x, u2_y, 50*mm, 18*mm, "U2  36->5 V", "U2",
            ["isolated preferred", "low ripple"])
    d.line_v(tap_x, logic_y + 14*mm, u2_y + 9*mm)
    d.line_h(tap_x, u2_y + 9*mm, u2_x)

    # F5 logic fuse
    c.setFont(FONT, 6)
    c.setFillColorRGB(*BLACK)
    c.drawString(tap_x + 2*mm, u2_y + 12*mm, "F5")

    # A2 STM32 + RC
    a2_x = u2_x + 58*mm
    d.arrow_h(u2_x + 50*mm, u2_y + 9*mm, a2_x)
    c.setFont(FONT, 7)
    c.setFillColorRGB(*BLACK)
    c.drawString(a2_x + 2*mm, u2_y + 9*mm - 2, "A2 STM32 + RC")

    # U3 optional 12V
    u3_x = u2_x
    u3_y = u2_y - 25*mm
    d.block(u3_x, u3_y, 50*mm, 18*mm, "U3  36->12 V", "U3",
            ["isolated preferred", "low ripple"])
    d.line_v(tap_x, u2_y + 9*mm, u3_y + 9*mm)
    d.line_h(tap_x, u3_y + 9*mm, u3_x)

    c.setFont(FONT, 6)
    c.setFillColorRGB(*BLACK)
    c.drawString(tap_x + 2*mm, u3_y + 12*mm, "F6")
    a_aux = u3_x + 58*mm
    d.arrow_h(u3_x + 50*mm, u3_y + 9*mm, a_aux)
    c.setFont(FONT, 7)
    c.drawString(a_aux + 2*mm, u3_y + 9*mm - 2,
                 "optional lights/sensors")

    # ── Ground bus ──
    gnd_y = u3_y - 20*mm
    c.setFont(FONT, 7)
    c.setFillColorRGB(*BLACK)
    c.drawString(DRAW_LEFT + 10*mm, gnd_y + 5*mm,
                 "0 V RETURN / CHASSIS BONDING POINT P0 "
                 "- star connection near battery negative, "
                 "no motor current through logic ground")
    c.setLineWidth(1.0)
    c.setStrokeColorRGB(*BLACK)
    c.line(DRAW_LEFT + 10*mm, gnd_y,
           DRAW_LEFT + 200*mm, gnd_y)
    d.ground_symbol(DRAW_LEFT + 105*mm, gnd_y)

    # ── Notes ──
    d.notes_block(DRAW_LEFT + 10*mm, DRAW_BOTTOM + 8*mm, 65*mm,
                  "Protection Notes", [
        "F1 installed within 150 mm of battery positive.",
        "F2/F3 protect motor branch wiring.",
        "F4/F5 protect low-voltage converters.",
        "Fuse values shall be selected from",
        "measured current and wire gauge.",
    ], "NOTE")

    d.notes_block(DRAW_LEFT + 85*mm, DRAW_BOTTOM + 8*mm, 65*mm,
                  "Recommended Additions", [
        "TVS diode on 36 V bus",
        "bulk capacitor near motor drivers",
        "reverse-polarity protection",
        "pre-charge or soft-start if inrush trips BMS",
    ], "EMC")

    # IEC reference table
    ref_x = DRAW_RIGHT - 70*mm
    ref_y = DRAW_BOTTOM + 8*mm
    d.notes_block(ref_x, ref_y, 60*mm,
                  "Reference Designators", [
        "B = battery/sensor",
        "F = fuse",
        "K = relay/contactor",
        "Q = power driver",
        "S = switch",
        "U = converter/module",
        "M = motor",
        "A = assembly/PCB",
    ], "IEC")


# ════════════════════════════════════════════════════════════════════
#  SHEET 3: Control I/O and Wiring Overview
# ════════════════════════════════════════════════════════════════════

def draw_sheet_03(c):
    d = EEDrawing(c)
    d.draw_border()
    d.draw_page_title(
        "Control I/O and Wiring Overview",
        "STM32-centric vehicle control wiring for V1 teleoperation"
    )
    d.draw_title_block("AgriBot UGV", "AGB-EE-DRW-001", "03", "08",
                       "A", "Control I/O and Wiring Overview",
                       "PRELIMINARY / ENGINEERING CONCEPT", "2026-05-23")

    top = DRAW_TOP - 28*mm
    bw = 52*mm
    bh = 22*mm

    # ── Inputs (left column) ──
    # FlySky Receiver
    rx_x = DRAW_LEFT + 10*mm
    rx_y = top - 10*mm
    d.block(rx_x, rx_y, bw + 8*mm, 32*mm,
            "A1 FlySky Receiver", "RC",
            ["CH1 steering PWM", "CH2 throttle PWM",
             "CH5 arm switch", "CH6 mode switch",
             "5 V / GND"])

    # E-stop input
    es_x = rx_x
    es_y = rx_y - 45*mm
    d.block(es_x, es_y, bw, bh, "S0 E-stop Input", "S0",
            ["NC contact to STM32", "separate power cutoff"])

    # Battery sense
    bs_x = rx_x
    bs_y = es_y - 38*mm
    d.block(bs_x, bs_y, bw, bh, "Battery Sense", "VBAT",
            ["resistor divider", "filter capacitor",
             "ADC <= 3.0 V"])

    # ── STM32 (center) ──
    stm_x = DRAW_LEFT + 120*mm
    stm_y = top - 75*mm
    stm_w = 75*mm
    stm_h = 85*mm
    d.block(stm_x, stm_y, stm_w, stm_h,
            "A2 STM32F767 Nucleo", "VCU")

    # Internal function list
    c.setFont(FONT, 7)
    c.setFillColorRGB(*DGRAY)
    funcs = [
        "TIM input capture",
        "PWM timers",
        "GPIO outputs",
        "ADC battery sense",
        "USART/USB debug",
        "safety state machine",
    ]
    for i, f in enumerate(funcs):
        c.drawString(stm_x + 5*mm,
                     stm_y + stm_h - 15*mm - i * 9, f)

    # ── Connections to STM32 ──
    # Receiver -> STM32
    d.arrow_h(rx_x + bw + 8*mm, rx_y + 16*mm,
              stm_x, label="PWM/PPM/iBUS")

    # E-stop -> STM32
    d.arrow_h(es_x + bw, es_y + bh/2,
              stm_x, label="digital input")

    # Battery -> STM32
    d.arrow_h(bs_x + bw, bs_y + bh/2,
              stm_x, label="ADC")

    # ── Outputs (right column) ──
    # Q1 Left ZS-X11H
    q1_x = DRAW_LEFT + 260*mm
    q1_y = top - 15*mm
    d.block(q1_x, q1_y, bw + 5*mm, 30*mm,
            "Q1 Left ZS-X11H", "Q1",
            ["PWM speed", "DIR", "STOP/EN",
             "BRAKE", "GND reference"])

    # Q2 Right ZS-X11H
    q2_x = q1_x
    q2_y = q1_y - 42*mm
    d.block(q2_x, q2_y, bw + 5*mm, 30*mm,
            "Q2 Right ZS-X11H", "Q2",
            ["PWM speed", "DIR", "STOP/EN",
             "BRAKE", "GND reference"])

    # STM32 -> Q1
    d.arrow_h(stm_x + stm_w, q1_y + 15*mm,
              q1_x, label="left control")

    # STM32 -> Q2
    d.arrow_h(stm_x + stm_w, q2_y + 15*mm,
              q2_x, label="right control")

    # ── Motors ──
    m1_x = DRAW_RIGHT - 55*mm
    m1_y = q1_y - 5*mm
    d.block(m1_x, m1_y, 48*mm, 24*mm,
            "M1 Left BLDC", "M1",
            ["3 phases", "hall A/B/C"])

    m2_x = m1_x
    m2_y = q2_y - 5*mm
    d.block(m2_x, m2_y, 48*mm, 24*mm,
            "M2 Right BLDC", "M2",
            ["3 phases", "hall A/B/C"])

    # Q1 -> M1
    d.arrow_h(q1_x + bw + 5*mm, q1_y + 18*mm,
              m1_x, label="phase")
    d.arrow_h(m1_x, q1_y + 8*mm,
              q1_x + bw + 5*mm, label="hall")

    # Q2 -> M2
    d.arrow_h(q2_x + bw + 5*mm, q2_y + 18*mm,
              m2_x, label="phase")
    d.arrow_h(m2_x, q2_y + 8*mm,
              q2_x + bw + 5*mm, label="hall")

    # ── Pi (bottom right) ──
    pi_x = q2_x
    pi_y = q2_y - 50*mm
    d.block(pi_x, pi_y, bw + 5*mm, 22*mm,
            "A3 Raspberry Pi 5", "SBC",
            ["V1: logging only", "future: cmd_vel"])

    # Camera
    cam_x = m2_x
    cam_y = pi_y
    d.block(cam_x, cam_y, 48*mm, 22*mm,
            "B2 Camera", "CAM",
            ["USB/CSI", "front view"])

    # STM32 -> Pi
    d.line_v(stm_x + stm_w - 10*mm, stm_y, pi_y + 22*mm + 8*mm)
    d.line_h(stm_x + stm_w - 10*mm, pi_y + 22*mm + 8*mm,
             pi_x + 10*mm)
    d.arrow_v(pi_x + 10*mm, pi_y + 22*mm + 8*mm, pi_y + 22*mm,
              label="USB/UART debug")

    # Pi -> Camera
    d.arrow_h(pi_x + bw + 5*mm, pi_y + 11*mm,
              cam_x, label="USB/CSI")

    # ── Harness table ──
    d.notes_block(DRAW_LEFT + 10*mm, DRAW_BOTTOM + 8*mm, 80*mm,
                  "Connector Allocation - prototype harness", [
        "J1: 36 V battery and main return",
        "J2: left motor driver control and power",
        "J3: right motor driver control and power",
        "J4: RC receiver and operator controls",
        "J5: Raspberry Pi service/debug link",
        "J6: E-stop and motor contactor loop",
    ], "HARNESS")

    d.notes_block(DRAW_LEFT + 100*mm, DRAW_BOTTOM + 8*mm, 95*mm,
                  "Electrical Interface Rules", [
        "All STM32 outputs to motor-driver command pins shall",
        "fail LOW at reset. Use pull-down resistors on PWM,",
        "STOP and BRAKE. Direction changes only permitted",
        "after PWM = 0 and a dead time delay.",
    ], "RULES")


# ════════════════════════════════════════════════════════════════════
#  SHEET 4: Grounding, EMC and Physical Installation
# ════════════════════════════════════════════════════════════════════

def draw_sheet_04(c):
    d = EEDrawing(c)
    d.draw_border()
    d.draw_page_title(
        "Grounding, EMC and Physical Installation",
        "Harness routing and electrical zoning for noisy BLDC drive system"
    )
    d.draw_title_block("AgriBot UGV", "AGB-EE-DRW-001", "04", "08",
                       "A", "Grounding, EMC and Physical Installation",
                       "PRELIMINARY / ENGINEERING CONCEPT", "2026-05-23")

    top = DRAW_TOP - 28*mm

    # ── Top view zoning ──
    c.setFont(FONT_B, 9)
    c.setFillColorRGB(*BLACK)
    c.drawCentredString(DRAW_LEFT + (DRAW_RIGHT - DRAW_LEFT)/2,
                        top + 3*mm,
                        "Top view electrical zoning - "
                        "simplified chassis envelope")

    # Chassis outline
    chassis_x = DRAW_LEFT + 40*mm
    chassis_y = top - 140*mm
    chassis_w = 320*mm
    chassis_h = 130*mm
    c.setLineWidth(1.0)
    c.setStrokeColorRGB(*BLACK)
    c.rect(chassis_x, chassis_y, chassis_w, chassis_h)

    # Zone dividers
    zone1_w = chassis_w * 0.30  # motor power
    zone2_w = chassis_w * 0.35  # control
    zone3_w = chassis_w * 0.35  # compute/sensor

    z1_right = chassis_x + zone1_w
    z2_right = z1_right + zone2_w

    c.setLineWidth(0.5)
    c.setStrokeColorRGB(*LGRAY)
    c.setDash(5, 3)
    c.line(z1_right, chassis_y, z1_right, chassis_y + chassis_h)
    c.line(z2_right, chassis_y, z2_right, chassis_y + chassis_h)
    c.setDash()

    # Zone labels
    c.setFont(FONT_B, 9)
    c.setFillColorRGB(*BLACK)
    c.drawCentredString(chassis_x + zone1_w/2,
                        chassis_y + chassis_h - 8*mm,
                        "MOTOR POWER ZONE")
    c.drawCentredString(z1_right + zone2_w/2,
                        chassis_y + chassis_h - 8*mm,
                        "CONTROL ZONE")
    c.drawCentredString(z2_right + zone3_w/2,
                        chassis_y + chassis_h - 8*mm,
                        "COMPUTE / SENSOR ZONE")

    # Motor drivers in zone 1
    q_y = chassis_y + chassis_h/2 + 5*mm
    qw = 28*mm
    qh = 18*mm
    d.block(chassis_x + 15*mm, q_y, qw, qh, "Q1", "",
            ["left driver"])
    d.block(chassis_x + 15*mm + qw + 10*mm, q_y, qw, qh, "Q2", "",
            ["right driver"])

    # 36V busbar
    c.setFont(FONT, 7)
    c.setFillColorRGB(*DGRAY)
    bus_y2 = chassis_y + 25*mm
    c.setLineWidth(1.0)
    c.setStrokeColorRGB(*BLACK)
    c.line(chassis_x + 10*mm, bus_y2,
           chassis_x + zone1_w - 5*mm, bus_y2)
    c.drawString(chassis_x + 12*mm, bus_y2 + 3*mm, "36 V busbar")
    c.setFont(FONT, 6)
    c.drawString(chassis_x + 12*mm, bus_y2 - 5*mm, "fused branches")
    c.setLineWidth(0.6)

    # DC/DC converters in control zone
    dc_y = chassis_y + chassis_h/2
    d.block(z1_right + 15*mm, dc_y + 15*mm, 32*mm, 16*mm,
            "U2 5 V", "", ["logic DC/DC"])
    d.block(z1_right + 15*mm, dc_y - 8*mm, 32*mm, 16*mm,
            "U1 5.1 V", "", ["Pi DC/DC"])

    # STM32 in control zone
    stm_x2 = z1_right + 55*mm
    d.block(stm_x2, dc_y - 5*mm, 35*mm, 30*mm, "A2 STM32", "",
            ["VCU", "logic ground"])

    # Pi in compute zone
    pi_x2 = z2_right + 20*mm
    d.block(pi_x2, dc_y + 5*mm, 35*mm, 22*mm, "A3 Pi 5", "",
            ["logging", "future autonomy"])

    # Camera in compute zone (top right of chassis)
    cam_x2 = z2_right + zone3_w - 40*mm
    cam_y2 = chassis_y + chassis_h - 25*mm
    d.block(cam_x2, cam_y2, 30*mm, 16*mm, "B2", "", ["cam"])
    c.setFont(FONT, 6)
    c.setFillColorRGB(*DGRAY)
    # Camera routing note
    c.drawString(cam_x2 - 20*mm, cam_y2 + 18*mm,
                 "camera cable route - keep away from phase wires")
    c.setStrokeColorRGB(*LGRAY)
    c.setDash(3, 2)
    c.line(cam_x2, cam_y2 + 8*mm, cam_x2 - 15*mm, cam_y2 + 15*mm)
    c.setDash()

    # ── Ground point ──
    gnd_x = chassis_x + chassis_w/2 - 5*mm
    gnd_y = chassis_y - 5*mm
    d.ground_symbol(gnd_x, gnd_y)
    c.setFont(FONT, 7)
    c.setFillColorRGB(*BLACK)
    c.drawCentredString(gnd_x, gnd_y - 8*mm,
                        "single-point power return / chassis bond")
    c.drawCentredString(gnd_x, gnd_y - 13*mm, "P0")

    # Ground lines from zones to P0
    c.setLineWidth(0.5)
    c.setStrokeColorRGB(*BLACK)
    d.line_v(gnd_x, chassis_y, gnd_y + 5*mm)
    d.line_v(chassis_x + zone1_w/2, chassis_y, chassis_y - 3*mm)
    d.line_h(chassis_x + zone1_w/2, chassis_y - 3*mm, gnd_x)
    d.line_v(z2_right + zone3_w/2, chassis_y, chassis_y - 3*mm)
    d.line_h(z2_right + zone3_w/2, chassis_y - 3*mm, gnd_x)

    # Motor phase routing notes
    c.setFont(FONT, 7)
    c.setFillColorRGB(*DGRAY)
    c.drawString(chassis_x + 5*mm, chassis_y - 10*mm,
                 "Left motor phases: twisted/bundled, short, "
                 "away from camera")
    c.drawRightString(chassis_x + chassis_w - 5*mm, chassis_y - 10*mm,
                      "Right motor phases: twisted/bundled, short, "
                      "away from logic")

    # ── Rules boxes ──
    rules_y = DRAW_BOTTOM + 8*mm
    d.notes_block(DRAW_LEFT + 10*mm, rules_y, 80*mm,
                  "Grounding Rules", [
        "1. Star return at P0.",
        "2. Do not daisy-chain Pi/STM32 ground",
        "   through motor driver power return.",
        "3. Add ferrites on camera and USB",
        "   if noise appears.",
    ], "GND")

    d.notes_block(DRAW_LEFT + 100*mm, rules_y, 80*mm,
                  "Harness Rules", [
        "1. Motor phase wires: shortest path.",
        "2. RC/sensor wires: separate bundle.",
        "3. Cross noisy and sensitive cables",
        "   at 90 degrees.",
    ], "HARNESS")

    d.notes_block(DRAW_LEFT + 190*mm, rules_y, 80*mm,
                  "Enclosure Rules", [
        "1. Use cable glands and strain relief.",
        "2. Mount electronics low on chassis.",
        "3. Seal against dust, soil and",
        "   irrigation water.",
    ], "MECH")


# ════════════════════════════════════════════════════════════════════
#  SHEET 5: Safety and Operating State Machine
# ════════════════════════════════════════════════════════════════════

def draw_sheet_05(c):
    d = EEDrawing(c)
    d.draw_border()
    d.draw_page_title(
        "Safety and Operating State Machine",
        "STM32 state authority for teleoperation and future autonomy"
    )
    d.draw_title_block("AgriBot UGV", "AGB-EE-DRW-001", "05", "08",
                       "A", "Safety and Operating State Machine",
                       "PRELIMINARY / ENGINEERING CONCEPT", "2026-05-23")

    top = DRAW_TOP - 35*mm
    bw = 60*mm
    bh = 28*mm
    state_fill = VLGRAY

    # ── BOOT ──
    boot_x = DRAW_LEFT + 20*mm
    boot_y = top - 15*mm
    d.block(boot_x, boot_y, bw, bh, "BOOT", "STATE",
            ["init IO", "outputs disabled", "self-test"],
            fill=state_fill)

    # ── DISARMED ──
    dis_x = boot_x + bw + 35*mm
    dis_y = boot_y
    d.block(dis_x, dis_y, bw + 10*mm, bh, "DISARMED", "STATE",
            ["PWM=0", "STOP active", "wait for arm"],
            fill=state_fill)

    # BOOT -> DISARMED
    d.arrow_h(boot_x + bw, boot_y + bh/2,
              dis_x, label="init OK")

    # ── ARMED_MANUAL ──
    man_x = dis_x + bw + 10*mm + 40*mm
    man_y = boot_y
    d.block(man_x, man_y, bw + 15*mm, bh, "ARMED_MANUAL", "STATE",
            ["RC command source", "ramp limiting",
             "operator priority"],
            fill=state_fill)

    # DISARMED -> ARMED_MANUAL
    d.arrow_h(dis_x + bw + 10*mm, dis_y + bh/2,
              man_x, label="arm + RC valid")

    # ARMED_MANUAL -> DISARMED (back arrow above)
    back_y = man_y + bh + 8*mm
    d.line_v(man_x + 10*mm, man_y + bh, back_y)
    d.line_h(man_x + 10*mm, back_y, dis_x + 35*mm)
    d.arrow_v(dis_x + 35*mm, back_y, dis_y + bh)
    c.setFont(FONT, 6)
    c.setFillColorRGB(*DGRAY)
    c.drawCentredString((man_x + 10*mm + dis_x + 35*mm)/2,
                        back_y + 2*mm, "disarm / RC lost")

    # ── ARMED_AUTO ──
    auto_x = man_x + 20*mm
    auto_y = man_y - 55*mm
    d.block(auto_x, auto_y, bw + 15*mm, bh, "ARMED_AUTO", "STATE",
            ["future Pi command", "RC override",
             "watchdog required"],
            fill=state_fill)
    # Dashed border to indicate future
    c.setStrokeColorRGB(*LGRAY)
    c.setDash(4, 3)
    c.setLineWidth(0.5)
    c.rect(auto_x - 2*mm, auto_y - 2*mm,
           bw + 19*mm, bh + 4*mm)
    c.setDash()
    c.setFont(FONT, 6)
    c.setFillColorRGB(*MGRAY)
    c.drawString(auto_x, auto_y - 6*mm, "V2+ feature")

    # ARMED_MANUAL -> ARMED_AUTO
    d.arrow_v(man_x + bw/2 + 15*mm, man_y, auto_y + bh,
              label="AUTO request/future", right=True)

    # ARMED_AUTO -> ARMED_MANUAL (fallback)
    d.line_h(auto_x, auto_y + bh/2,
             auto_x - 15*mm)
    d.line_v(auto_x - 15*mm, auto_y + bh/2, man_y + 5*mm)
    d.arrow_h(auto_x - 15*mm, man_y + 5*mm,
              man_x + bw + 15*mm)
    c.setFont(FONT, 6)
    c.setFillColorRGB(*DGRAY)
    c.drawString(auto_x - 14*mm, man_y + 1*mm, "Pi timeout / manual")

    # ── FAULT ──
    fault_x = dis_x + 15*mm
    fault_y = dis_y - 55*mm
    d.block(fault_x, fault_y, bw, bh, "FAULT", "STATE",
            ["PWM=0", "manual reset", "diagnostics"],
            fill=state_fill, line_w=1.2)

    # DISARMED -> FAULT
    d.arrow_v(dis_x + 20*mm, dis_y, fault_y + bh,
              label="fault", right=False)

    # ARMED_MANUAL -> FAULT
    d.line_v(man_x + 30*mm, man_y, fault_y + bh + 3*mm)
    d.line_h(man_x + 30*mm, fault_y + bh + 3*mm,
             fault_x + bw/2)
    d.arrow_v(fault_x + bw/2, fault_y + bh + 3*mm, fault_y + bh)
    c.setFont(FONT, 6)
    c.setFillColorRGB(*DGRAY)
    c.drawString(man_x - 10*mm, fault_y + bh + 5*mm, "fault")

    # ARMED_AUTO -> FAULT
    d.line_h(auto_x + bw/2, auto_y,
             fault_x + bw - 5*mm)
    d.arrow_v(fault_x + bw - 5*mm, auto_y, fault_y + bh)

    # FAULT -> DISARMED (reset path)
    d.line_h(fault_x, fault_y + bh/2,
             fault_x - 15*mm)
    d.line_v(fault_x - 15*mm, fault_y + bh/2,
             dis_y + 5*mm)
    d.arrow_h(fault_x - 15*mm, dis_y + 5*mm, dis_x)
    c.setFont(FONT, 6)
    c.setFillColorRGB(*DGRAY)
    c.drawString(fault_x - 40*mm, fault_y + bh/2 + 3*mm,
                 "after diagnose")

    # ── ESTOP ──
    estop_x = man_x + 15*mm
    estop_y = fault_y - 10*mm
    d.block(estop_x, estop_y, bw, bh, "ESTOP", "STATE",
            ["motor power open", "logic alive",
             "reset required"],
            line_w=1.5)

    # Any armed -> ESTOP
    c.setFont(FONT, 6)
    c.setFillColorRGB(*DGRAY)
    d.line_v(man_x + bw + 20*mm, man_y, estop_y + bh)
    c.drawString(man_x + bw + 22*mm, estop_y + bh + 4*mm, "E-stop")
    d.arrow_h(man_x + bw + 20*mm, estop_y + bh/2, estop_x + bw)

    # ESTOP -> FAULT
    d.arrow_h(estop_x, estop_y + bh/2,
              fault_x + bw, label="recover after E-stop reset")

    # ── Fault sources ──
    d.notes_block(DRAW_LEFT + 10*mm, DRAW_BOTTOM + 50*mm, 55*mm,
                  "Fault Sources", [
        "RC loss",
        "battery undervoltage",
        "Pi timeout in AUTO",
        "invalid command",
        "driver/thermal future",
    ], "F")

    # ── Reset conditions ──
    d.notes_block(DRAW_RIGHT - 70*mm, DRAW_BOTTOM + 30*mm, 60*mm,
                  "Reset Conditions", [
        "E-stop released",
        "arm switch OFF->ON",
        "fault latch cleared",
        "operator present",
    ], "R")

    # ── Safety priority ──
    d.notes_block(DRAW_LEFT + 10*mm, DRAW_BOTTOM + 8*mm, 100*mm,
                  "Safety Priority Order", [
        "1. Hardware E-stop opens motor power path.",
        "2. STM32 fault logic disables PWM/STOP/BRAKE commands.",
        "3. RC manual override has priority over Pi.",
        "4. Future Pi autonomy is accepted only when AUTO mode",
        "   and watchdog are valid.",
    ])

    # ── Transition guards ──
    d.notes_block(DRAW_LEFT + 120*mm, DRAW_BOTTOM + 8*mm, 100*mm,
                  "Transition Guards", [
        "- RC loss in manual mode: stop immediately.",
        "- Pi command timeout in auto mode: command = zero,",
        "  return to manual or fault according to switch.",
        "- Direction change: ramp PWM to zero, wait,",
        "  change DIR, ramp up.",
        "- Startup default: motor STOP active and PWM disabled",
        "  until explicitly armed.",
    ])


# ════════════════════════════════════════════════════════════════════
#  SHEET 6: Interface Control Diagram
# ════════════════════════════════════════════════════════════════════

def draw_sheet_06(c):
    d = EEDrawing(c)
    d.draw_border()
    d.draw_page_title(
        "Interface Control Diagram",
        "Clear electrical interfaces between receiver, STM32, "
        "motor drivers, power rails, and companion computer"
    )
    d.draw_title_block("AgriBot UGV", "AGB-EE-DRW-001", "06", "08",
                       "A", "Interface Control Diagram",
                       "PRELIMINARY / ENGINEERING CONCEPT", "2026-05-23")

    top = DRAW_TOP - 28*mm

    # ── STM32 center block with internal functions ──
    stm_x = DRAW_LEFT + 130*mm
    stm_y = top - 115*mm
    stm_w = 90*mm
    stm_h = 105*mm

    # Dashed zone around STM32
    d.dashed_zone(stm_x - 3*mm, stm_y - 3*mm,
                  stm_w + 6*mm, stm_h + 6*mm, "VCU")

    c.setFont(FONT_B, 10)
    c.setFillColorRGB(*BLACK)
    c.drawCentredString(stm_x + stm_w/2, stm_y + stm_h - 7*mm,
                        "STM32F767 Nucleo")

    # Internal blocks (2 columns)
    ibw = 38*mm
    ibh = 14*mm
    col_a = stm_x + 4*mm
    col_b = stm_x + stm_w/2 + 2*mm

    # Row 1
    r1y = stm_y + stm_h - 25*mm
    d.block(col_a, r1y, ibw, ibh, "Timer input", "",
            ["capture"], bold_label=False, line_w=0.4)
    d.block(col_b, r1y, ibw, ibh, "RC validity", "",
            ["watchdog"], bold_label=False, line_w=0.4)

    # Row 2
    r2y = r1y - 20*mm
    d.block(col_a, r2y, ibw, ibh, "Motor PWM", "",
            ["timers"], bold_label=False, line_w=0.4)
    d.block(col_b, r2y, ibw, ibh, "GPIO safety", "",
            ["outputs"], bold_label=False, line_w=0.4)

    # Row 3
    r3y = r2y - 20*mm
    d.block(col_a, r3y, ibw, ibh, "ADC + filters", "",
            ["battery"], bold_label=False, line_w=0.4)
    d.block(col_b, r3y, ibw, ibh, "Serial packet", "",
            ["bridge"], bold_label=False, line_w=0.4)

    # Row 4
    r4y = r3y - 20*mm
    d.block(col_a + ibw/2, r4y, ibw, ibh, "State machine", "",
            ["command mux"], bold_label=False, line_w=0.4)

    # ── Input devices (left) ──
    # FlySky
    inp_x = DRAW_LEFT + 15*mm
    fs_y = r1y + 5*mm
    d.block(inp_x, fs_y, 55*mm, 28*mm,
            "FlySky Receiver", "",
            ["5 V logic rail", "CH1 / CH2 / CH5 / CH6"])
    c.setFont(FONT_B, 7)
    c.setFillColorRGB(*BLACK)
    c.drawString(inp_x + 2*mm, fs_y + 28*mm + 2*mm, "INPUT")

    d.arrow_h(inp_x + 55*mm, fs_y + 14*mm,
              stm_x, label="RC channels")

    # E-stop
    es_y = r2y - 5*mm
    d.block(inp_x, es_y, 55*mm, 24*mm,
            "E-stop Input", "",
            ["normally-closed loop", "logic sense only"])
    c.setFont(FONT_B, 7)
    c.setFillColorRGB(*BLACK)
    c.drawString(inp_x + 2*mm, es_y + 24*mm + 2*mm, "SAFETY")

    d.arrow_h(inp_x + 55*mm, es_y + 12*mm,
              stm_x, label="E-stop sense")

    # Battery sense
    bat_y = r3y - 10*mm
    d.block(inp_x, bat_y, 55*mm, 24*mm,
            "Battery Sense", "",
            ["resistor divider", "42 V max < 3.0 V ADC"])
    c.setFont(FONT_B, 7)
    c.setFillColorRGB(*BLACK)
    c.drawString(inp_x + 2*mm, bat_y + 24*mm + 2*mm, "ADC")

    d.arrow_h(inp_x + 55*mm, bat_y + 12*mm,
              stm_x, label="ADC")

    # ── Output devices (right) ──
    out_x = DRAW_LEFT + 295*mm

    # Left ZS-X11H
    lz_y = r1y
    d.block(out_x, lz_y, 62*mm, 28*mm,
            "Left ZS-X11H", "",
            ["PWM speed", "DIR", "STOP / EN",
             "BRAKE optional"])
    c.setFont(FONT_B, 7)
    c.setFillColorRGB(*BLACK)
    c.drawString(out_x + 2*mm, lz_y + 28*mm + 2*mm, "OUTPUT")

    d.arrow_h(stm_x + stm_w, lz_y + 20*mm,
              out_x, label="left controls")

    # Right ZS-X11H
    rz_y = r2y - 5*mm
    d.block(out_x, rz_y, 62*mm, 28*mm,
            "Right ZS-X11H", "",
            ["PWM speed", "DIR", "STOP / EN",
             "BRAKE optional"])
    c.setFont(FONT_B, 7)
    c.setFillColorRGB(*BLACK)
    c.drawString(out_x + 2*mm, rz_y + 28*mm + 2*mm, "OUTPUT")

    d.arrow_h(stm_x + stm_w, rz_y + 15*mm,
              out_x, label="right controls")

    # Pi
    pi_y = r3y - 5*mm
    d.block(out_x, pi_y, 62*mm, 22*mm,
            "Raspberry Pi 5", "",
            ["logs / camera / autonomy"])
    c.setFont(FONT_B, 7)
    c.setFillColorRGB(*BLACK)
    c.drawString(out_x + 2*mm, pi_y + 22*mm + 2*mm, "LINK")

    d.arrow_h(stm_x + stm_w, pi_y + 11*mm,
              out_x, label="telemetry/cmd later")

    # ── Interface notes ──
    d.notes_block(DRAW_LEFT + 10*mm, DRAW_BOTTOM + 8*mm, 110*mm,
                  "Interface Notes", [
        "1. Do not power the Pi from the ZS-X11H 5 V pin.",
        "2. The STM32 output default must keep STOP active",
        "   and PWM at zero.",
        "3. Use common logic ground, but do not let motor",
        "   current return through signal wiring.",
        "4. Label every connector with voltage, signal",
        "   direction, and fuse rating.",
    ])


# ════════════════════════════════════════════════════════════════════
#  SHEET 7: Serial Protocol Specification
# ════════════════════════════════════════════════════════════════════

def draw_sheet_07(c):
    d = EEDrawing(c)
    d.draw_border()
    d.draw_page_title(
        "Serial Communication Protocol",
        "Pi <-> STM32 packet format, message definitions, timing"
    )
    d.draw_title_block("AgriBot UGV", "AGB-EE-DRW-001", "07", "08",
                       "A", "Serial Communication Protocol",
                       "PRELIMINARY / ENGINEERING CONCEPT", "2026-05-23")

    top = DRAW_TOP - 30*mm
    lm = DRAW_LEFT + 10*mm

    # ── Physical layer ──
    c.setFont(FONT_B, 10)
    c.setFillColorRGB(*BLACK)
    c.drawString(lm, top, "1. Physical Layer")
    c.setFont(FONT, 8)
    c.setFillColorRGB(*DGRAY)
    c.drawString(lm + 5*mm, top - 10, "Interface: USB Serial (Nucleo USB) or dedicated UART")
    c.drawString(lm + 5*mm, top - 20, "Baud rate: 115200    Data: 8N1    Flow control: none")
    c.drawString(lm + 5*mm, top - 30, "Cable: USB-A to micro-USB, < 1 m recommended")

    # ── Packet format ──
    pf_y = top - 50
    c.setFont(FONT_B, 10)
    c.setFillColorRGB(*BLACK)
    c.drawString(lm, pf_y, "2. Packet Format")

    # Draw packet structure as boxes
    py = pf_y - 25
    fields = [
        ("START1", "0xAA", 22*mm),
        ("START2", "0x55", 22*mm),
        ("LENGTH", "N", 22*mm),
        ("MSG_ID", "ID", 22*mm),
        ("SEQ", "n", 18*mm),
        ("PAYLOAD", "N bytes", 55*mm),
        ("CRC16_H", "", 22*mm),
        ("CRC16_L", "", 22*mm),
    ]

    fx = lm + 5*mm
    fh = 12*mm
    for name, val, fw in fields:
        c.setLineWidth(0.6)
        c.setStrokeColorRGB(*BLACK)
        c.rect(fx, py, fw, fh)
        c.setFont(FONT_B, 7)
        c.setFillColorRGB(*BLACK)
        c.drawCentredString(fx + fw/2, py + fh - 4*mm, name)
        if val:
            c.setFont(FONT, 6)
            c.setFillColorRGB(*DGRAY)
            c.drawCentredString(fx + fw/2, py + 2*mm, val)
        fx += fw

    c.setFont(FONT, 7)
    c.setFillColorRGB(*DGRAY)
    c.drawString(lm + 5*mm, py - 5*mm,
                 "CRC-16/CCITT-FALSE over bytes START1..PAYLOAD")

    # ── Message table: Pi -> STM32 ──
    tbl_y = py - 22*mm
    c.setFont(FONT_B, 10)
    c.setFillColorRGB(*BLACK)
    c.drawString(lm, tbl_y, "3. Messages: Pi -> STM32")

    # Table header
    th_y = tbl_y - 12
    cols = [lm + 5*mm, lm + 30*mm, lm + 70*mm, lm + 155*mm, lm + 195*mm]
    headers = ["MSG_ID", "Name", "Payload", "Rate", "Notes"]
    c.setFont(FONT_B, 7)
    c.setFillColorRGB(*BLACK)
    for col, hdr in zip(cols, headers):
        c.drawString(col, th_y, hdr)
    c.setLineWidth(0.4)
    c.line(lm + 3*mm, th_y - 3, lm + 230*mm, th_y - 3)

    # Table rows
    rows_pi = [
        ("0x01", "HEARTBEAT", "timestamp (4B uint32)", "10 Hz",
         "watchdog keepalive"),
        ("0x02", "CMD_VEL", "linear_vel (float32), angular_vel (float32)",
         "20 Hz", "V2+ only"),
        ("0x03", "SET_MODE", "mode (1B): 0=MANUAL, 1=AUTO",
         "on change", "V2+ only"),
    ]
    c.setFont(FONT, 7)
    c.setFillColorRGB(*DGRAY)
    for i, row in enumerate(rows_pi):
        ry = th_y - 14 - i * 12
        for col, val in zip(cols, row):
            c.drawString(col, ry, val)

    # ── Message table: STM32 -> Pi ──
    tbl2_y = th_y - 14 - len(rows_pi) * 12 - 18
    c.setFont(FONT_B, 10)
    c.setFillColorRGB(*BLACK)
    c.drawString(lm, tbl2_y, "4. Messages: STM32 -> Pi")

    th2_y = tbl2_y - 12
    c.setFont(FONT_B, 7)
    c.setFillColorRGB(*BLACK)
    for col, hdr in zip(cols, headers):
        c.drawString(col, th2_y, hdr)
    c.setLineWidth(0.4)
    c.line(lm + 3*mm, th2_y - 3, lm + 230*mm, th2_y - 3)

    rows_stm = [
        ("0x81", "STATUS", "state(1B) faults(2B) batt_mv(2B) rc_ok(1B)",
         "10 Hz", "always sent"),
        ("0x82", "MOTOR_FB",
         "left_duty(i16) right_duty(i16) left_dir(1B) right_dir(1B)",
         "20 Hz", "when armed"),
        ("0x83", "RC_CHANNELS", "ch1..ch6 (uint16 x 6, little-endian)",
         "20 Hz", "always sent"),
    ]
    c.setFont(FONT, 7)
    c.setFillColorRGB(*DGRAY)
    for i, row in enumerate(rows_stm):
        ry = th2_y - 14 - i * 12
        for col, val in zip(cols, row):
            c.drawString(col, ry, val)

    # ── Timing and safety ──
    tbl3_y = th2_y - 14 - len(rows_stm) * 12 - 18
    c.setFont(FONT_B, 10)
    c.setFillColorRGB(*BLACK)
    c.drawString(lm, tbl3_y, "5. Safety Rules")

    c.setFont(FONT, 8)
    c.setFillColorRGB(*DGRAY)
    rules = [
        "- STM32 stops motors if no valid HEARTBEAT from Pi for 250 ms.",
        "- CRC mismatch: discard packet silently, increment error counter.",
        "- RC input always has priority in MANUAL mode.",
        "- STM32 never accepts CMD_VEL unless in ARMED_AUTO state.",
        "- Pi should monitor STATUS messages; if absent for 500 ms, "
        "alert operator.",
        "- Sequence number wraps 0-255; receiver uses it for "
        "packet loss detection.",
    ]
    for i, rule in enumerate(rules):
        c.drawString(lm + 5*mm, tbl3_y - 14 - i * 12, rule)


# ════════════════════════════════════════════════════════════════════
#  SHEET 8: Pin Allocation Table
# ════════════════════════════════════════════════════════════════════

def draw_sheet_08(c):
    d = EEDrawing(c)
    d.draw_border()
    d.draw_page_title(
        "STM32 Pin Allocation and Wiring Table",
        "Preliminary assignment - finalize after CubeMX configuration"
    )
    d.draw_title_block("AgriBot UGV", "AGB-EE-DRW-001", "08", "08",
                       "A", "STM32 Pin Allocation and Wiring Table",
                       "PRELIMINARY / ENGINEERING CONCEPT", "2026-05-23")

    top = DRAW_TOP - 28*mm
    lm = DRAW_LEFT + 10*mm

    # ── Table header ──
    col_widths = [35*mm, 30*mm, 25*mm, 40*mm, 30*mm, 50*mm, 60*mm]
    headers = ["Function", "STM32 Pin", "Periph", "Signal",
               "Direction", "Destination", "Notes"]
    total_w = sum(col_widths)

    th_y = top - 5
    c.setFont(FONT_B, 7)
    c.setFillColorRGB(*BLACK)
    cx = lm
    for hdr, cw in zip(headers, col_widths):
        c.drawString(cx + 1*mm, th_y, hdr)
        cx += cw

    c.setLineWidth(0.6)
    c.line(lm, th_y - 3, lm + total_w, th_y - 3)

    # ── Table rows ──
    rows = [
        # Motor left
        ("Left PWM", "PA8 (TBD)", "TIM1_CH1", "PWM 2kHz",
         "OUT", "Q1 ZS-X11H speed", "0-100% duty"),
        ("Left DIR", "PB0 (TBD)", "GPIO", "Digital",
         "OUT", "Q1 ZS-X11H DIR", "level TBD"),
        ("Left STOP", "PB1 (TBD)", "GPIO", "Digital",
         "OUT", "Q1 ZS-X11H STOP", "default=disabled"),
        ("Left BRAKE", "PB2 (TBD)", "GPIO", "Digital",
         "OUT", "Q1 ZS-X11H BRAKE", "optional"),
        # sep
        ("", "", "", "", "", "", ""),
        # Motor right
        ("Right PWM", "PA9 (TBD)", "TIM1_CH2", "PWM 2kHz",
         "OUT", "Q2 ZS-X11H speed", "0-100% duty"),
        ("Right DIR", "PC0 (TBD)", "GPIO", "Digital",
         "OUT", "Q2 ZS-X11H DIR", "level TBD"),
        ("Right STOP", "PC1 (TBD)", "GPIO", "Digital",
         "OUT", "Q2 ZS-X11H STOP", "default=disabled"),
        ("Right BRAKE", "PC2 (TBD)", "GPIO", "Digital",
         "OUT", "Q2 ZS-X11H BRAKE", "optional"),
        # sep
        ("", "", "", "", "", "", ""),
        # RC input
        ("RC iBUS", "PD6 (TBD)", "USART2_RX", "iBUS 115200",
         "IN", "A1 FlySky RX", "single wire all CH"),
        ("RC CH1 alt", "PA0 (TBD)", "TIM2_CH1", "PWM capture",
         "IN", "A1 CH1 steering", "if PWM mode"),
        ("RC CH2 alt", "PA1 (TBD)", "TIM2_CH2", "PWM capture",
         "IN", "A1 CH2 throttle", "if PWM mode"),
        ("RC CH5 alt", "PA2 (TBD)", "TIM2_CH3", "PWM capture",
         "IN", "A1 CH5 arm", "if PWM mode"),
        # sep
        ("", "", "", "", "", "", ""),
        # Safety
        ("E-stop sense", "PE0 (TBD)", "GPIO", "Digital",
         "IN", "S0 NC contact", "pull-up, active LOW"),
        ("Battery ADC", "PA3 (TBD)", "ADC1_IN3", "Analog",
         "IN", "VBAT divider", "120k/10k, cap filter"),
        # sep
        ("", "", "", "", "", "", ""),
        # Communication
        ("Pi UART TX", "PD5 (TBD)", "USART2_TX", "Serial 115200",
         "OUT", "A3 Pi 5", "telemetry"),
        ("Pi UART RX", "PD6 (TBD)", "USART2_RX", "Serial 115200",
         "IN", "A3 Pi 5", "cmd_vel (V2+)"),
        ("USB debug", "USB", "USB OTG", "Serial",
         "BIDIR", "PC / Pi", "Nucleo USB"),
        # sep
        ("", "", "", "", "", "", ""),
        # Status
        ("Status LED", "PB7 (TBD)", "GPIO", "Digital",
         "OUT", "LED", "onboard or external"),
        ("Buzzer", "PB8 (TBD)", "TIM/GPIO", "PWM/Digital",
         "OUT", "Piezo buzzer", "fault/arm indication"),
    ]

    c.setFont(FONT, 6.5)
    c.setFillColorRGB(*DGRAY)
    row_h = 10
    for i, row in enumerate(rows):
        ry = th_y - 14 - i * row_h
        if ry < DRAW_BOTTOM + 15*mm:
            break
        cx = lm
        if row[0] == "":
            # separator
            c.setStrokeColorRGB(*LGRAY)
            c.setLineWidth(0.3)
            c.line(lm, ry + 3, lm + total_w, ry + 3)
            continue
        for val, cw in zip(row, col_widths):
            c.drawString(cx + 1*mm, ry, val)
            cx += cw

    # Bottom note
    note_y = DRAW_BOTTOM + 8*mm
    d.notes_block(lm, note_y, 130*mm,
                  "Pin Assignment Notes", [
        "All pins marked (TBD) - finalize in STM32CubeMX.",
        "Prefer 5V-tolerant pins for ZS-X11H interface.",
        "Use internal pull-downs on PWM/STOP/BRAKE outputs.",
        "Battery ADC: verify divider ratio against actual",
        "  battery voltage range before first power-on.",
        "iBUS and Pi UART may share USART2 - allocate",
        "  separate UARTs if both are used simultaneously.",
    ])

    d.notes_block(lm + 140*mm, note_y, 100*mm,
                  "Wire Gauge Reference", [
        "Motor phase wires: use original hoverboard gauge",
        "Motor control signals: 24-26 AWG",
        "Power to Pi: 18 AWG minimum",
        "Power to STM32/logic: 22 AWG",
        "RC receiver: 24-26 AWG",
        "E-stop loop: 22 AWG",
    ])


# ════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════

def main():
    c = canvas.Canvas(OUTPUT, pagesize=landscape(A3))
    c.setTitle("AgriBot UGV - EE Drawing Pack")
    c.setAuthor("AgriBot Engineering")
    c.setSubject("Industrial EE Documentation - V1 Teleoperation")

    sheets = [
        draw_sheet_01,
        draw_sheet_02,
        draw_sheet_03,
        draw_sheet_04,
        draw_sheet_05,
        draw_sheet_06,
        draw_sheet_07,
        draw_sheet_08,
    ]

    for i, draw_fn in enumerate(sheets):
        draw_fn(c)
        if i < len(sheets) - 1:
            c.showPage()

    c.save()
    print(f"Generated: {OUTPUT}")
    print(f"  {len(sheets)} sheets, A3 landscape")


if __name__ == "__main__":
    main()
