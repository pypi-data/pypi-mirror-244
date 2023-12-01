from .enums import *
from .rect import Rect
from .size import Size


def get_rect_with_margins(r: Rect, margin_top: float, margin_right: float, margin_bottom: float, margin_left: float) -> Rect:
    rect = Rect(other=r)
    rect.left += margin_left
    rect.top += margin_top
    rect.right -= margin_right
    rect.bottom -= margin_bottom
    return rect


def check_rect(r1: Rect, r2: Rect) -> Rect:
    rect = Rect(other=r2)
    if rect.right > r1.right:
        rect.right -= (rect.right - r1.right)
    if rect.bottom > r1.bottom:
        rect.bottom -= (rect.bottom - r1.bottom)
    return rect


def get_rect_with_size_and_align(r: Rect, size: Size = None, h_align: HAlign = HAlign.LEFT, v_align: VAlign = VAlign.TOP, text_align: TextAlign = None) -> Rect:
    if size is not None:
        width = size.width
        height = size.height
        upper_left_x = 0.0
        upper_left_y = 0.0

        match h_align:
            case HAlign.LEFT:
                upper_left_x = r.left
            case HAlign.RIGHT:
                upper_left_x = r.right - width
            case HAlign.CENTER:
                upper_left_x = r.left + (r.get_width() - width) / 2

        # TextAlign overrides horizontal alignment if set
        if text_align is not None:
            match text_align:
                case TextAlign.LEFT:
                    upper_left_x = r.left
                case TextAlign.RIGHT:
                    upper_left_x = r.right - width
                case TextAlign.CENTER:
                    upper_left_x = r.left + (r.get_width() - width) / 2

        match v_align:
            case VAlign.TOP:
                upper_left_y = r.top
            case VAlign.BOTTOM:
                upper_left_y = r.bottom - height
            case VAlign.MIDDLE:
                upper_left_y = r.top + (r.get_height() - height) / 2

        rect = Rect(upper_left_x, upper_left_y, upper_left_x + width, upper_left_y + height)
    else:
        size = r.get_size()
        rect = Rect(r.left, r.top, r.left + size.width, r.top + size.height)

    return check_rect(r, rect)
