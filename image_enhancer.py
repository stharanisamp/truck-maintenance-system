import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

def check_image_quality(image_bgr):
    """
    Evaluates image quality metrics:
    - Blur score using Laplacian variance (lower = blurrier)
    - Brightness and contrast statistics
    Returns a dict with quality health assessment.
    """
    if image_bgr is None:
        return {"is_blurry": True, "blur_score": 0.0, "is_dark": True, "warning": "Image could not be loaded."}
    
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    brightness = float(np.mean(gray))
    contrast = float(np.std(gray))

    is_blurry = blur_score < 60.0
    is_dark = brightness < 45.0
    is_washed_out = brightness > 235.0 and contrast < 25.0

    warning = None
    if is_blurry:
        warning = "Image appears blurry. Text recognition accuracy may be reduced."
    elif is_dark:
        warning = "Image is very dark. Automatic illumination boost applied."
    elif is_washed_out:
        warning = "Image has high glare/washout. Contrast enhancement applied."

    return {
        "is_blurry": is_blurry,
        "blur_score": round(blur_score, 2),
        "brightness": round(brightness, 1),
        "contrast": round(contrast, 1),
        "is_dark": is_dark,
        "warning": warning
    }

def remove_shadows_and_normalize(image_bgr):
    """
    Removes harsh phone camera shadows, flash gradients, and uneven lighting
    using morphological background division.
    """
    lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    # Morphological closing with large structuring element to capture background gradient
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    background = cv2.morphologyEx(l_channel, cv2.MORPH_DILATE, kernel)
    background = cv2.GaussianBlur(background, (21, 21), 0)

    # Division to eliminate background illumination variance
    diff = 255 - cv2.subtract(background, l_channel)
    normalized_l = cv2.normalize(diff, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    merged_lab = cv2.merge((normalized_l, a_channel, b_channel))
    result_bgr = cv2.cvtColor(merged_lab, cv2.COLOR_LAB2BGR)
    return result_bgr

def order_points(pts):
    """Orders 4 points in [top-left, top-right, bottom-right, bottom-left] order."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def correct_perspective_and_crop(image_bgr):
    """
    Attempts to locate the rectangular boundary of a paper memo on a table/dashboard
    and warps perspective to a clean flat view. Falls back to deskew if boundary not found.
    """
    h, w = image_bgr.shape[:2]
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200)

    # Find contours
    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        area = cv2.contourArea(approx)

        # Memo must occupy at least 35% of the total frame to be considered a document boundary
        if len(approx) == 4 and area > (0.35 * w * h):
            pts = approx.reshape(4, 2)
            rect = order_points(pts)
            (tl, tr, br, bl) = rect

            width_a = np.linalg.norm(br - bl)
            width_b = np.linalg.norm(tr - tl)
            max_w = max(int(width_a), int(width_b))

            height_a = np.linalg.norm(tr - br)
            height_b = np.linalg.norm(tl - bl)
            max_h = max(int(height_a), int(height_b))

            dst = np.array([
                [0, 0],
                [max_w - 1, 0],
                [max_w - 1, max_h - 1],
                [0, max_h - 1]
            ], dtype="float32")

            m = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(image_bgr, m, (max_w, max_h), flags=cv2.INTER_CUBIC)
            return warped

    return auto_deskew(image_bgr)

def auto_deskew(image_bgr):
    """
    Detects document orientation angle using edge detection and Hough lines or minAreaRect,
    and rotates the image horizontally.
    """
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 8
    )

    coords = np.column_stack(np.where(thresh > 0))
    if len(coords) < 50:
        return image_bgr

    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    elif angle > 45:
        angle = 90 - angle

    if 0.5 < abs(angle) < 30.0:
        (h, w) = image_bgr.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image_bgr, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
        )
        return rotated

    return image_bgr

def enhance_handwriting_contrast(image_bgr):
    """
    Applies CLAHE (Contrast Limited Adaptive Histogram Equalization)
    and unsharp masking to enhance faint ballpoint pen, pencil, and carbon-copy strokes.
    """
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    smooth = cv2.bilateralFilter(gray, d=7, sigmaColor=50, sigmaSpace=50)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(smooth)

    gaussian = cv2.GaussianBlur(enhanced_gray, (0, 0), 2.0)
    sharpened = cv2.addWeighted(enhanced_gray, 1.6, gaussian, -0.6, 0)
    return sharpened

def create_binarized_handwriting(enhanced_gray):
    """
    Produces high-contrast adaptive binarized black-and-white image
    specifically tuned for handwriting character segmentation.
    """
    binarized = cv2.adaptiveThreshold(
        enhanced_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 21, 10
    )
    return binarized

def detect_handwriting_regions(enhanced_gray):
    """
    Detects rectangular regions corresponding to text and handwriting blocks.
    Returns normalized bounding boxes [ymin, xmin, ymax, xmax] between 0.0 and 1.0.
    """
    h, w = enhanced_gray.shape[:2]
    # Invert threshold
    _, thresh = cv2.threshold(enhanced_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Morphological gradient to connect nearby words
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
    connected = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(connected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for c in contours:
        x, y, bw, bh = cv2.boundingRect(c)
        # Filter tiny noise or huge frame-spanning rectangles
        if 20 < bw < (w * 0.95) and 10 < bh < (h * 0.3):
            boxes.append({
                "ymin": round(y / h, 4),
                "xmin": round(x / w, 4),
                "ymax": round((y + bh) / h, 4),
                "xmax": round((x + bw) / w, 4),
                "width": bw,
                "height": bh
            })
    return boxes

class PreprocessedResult(tuple):
    """
    Backwards-compatible tuple (enhanced_path, binarized_path)
    with object attributes for quality and regions.
    """
    def __new__(cls, enhanced_path, binarized_path, quality=None, regions=None):
        instance = super(PreprocessedResult, cls).__new__(cls, (enhanced_path, binarized_path))
        instance.enhanced_path = enhanced_path
        instance.binarized_path = binarized_path
        instance.quality = quality or {}
        instance.regions = regions or []
        return instance

def detect_and_auto_orient(image_bgr, user_rotation=0):
    """
    Detects if the document was photographed sideways (90° or 270°) or upside-down (180°),
    and rotates it so that text lines run horizontally and the header is at the top.
    
    If user_rotation is specified (90, 180, 270), applies that explicit rotation.
    """
    if user_rotation in [90, 180, 270]:
        if user_rotation == 90:
            return 90, cv2.rotate(image_bgr, cv2.ROTATE_90_CLOCKWISE)
        elif user_rotation == 180:
            return 180, cv2.rotate(image_bgr, cv2.ROTATE_180)
        elif user_rotation == 270:
            return 270, cv2.rotate(image_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)

    h, w = image_bgr.shape[:2]
    
    def get_line_projection_ratio(img):
        rh, rw = img.shape[:2]
        scale = 400.0 / rh
        small = cv2.resize(img, (int(rw * scale), 400))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY) if len(small.shape) == 3 else small
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        h_proj = np.sum(morphed, axis=1)
        v_proj = np.sum(morphed, axis=0)
        return float(np.var(h_proj) / (np.var(v_proj) + 1e-5))
    
    base_ratio = get_line_projection_ratio(image_bgr)
    rot_90 = cv2.rotate(image_bgr, cv2.ROTATE_90_CLOCKWISE)
    rot_90_ratio = get_line_projection_ratio(rot_90)
    
    # If rot_90 horizontal variance is significantly higher, the image was photographed sideways!
    if rot_90_ratio > base_ratio * 1.25:
        rot_270 = cv2.rotate(image_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        # Count text blobs in top 25% of both 90 and 270
        crop_90 = rot_90[:int(rot_90.shape[0] * 0.25), :]
        crop_270 = rot_270[:int(rot_270.shape[0] * 0.25), :]
        
        def count_text_blobs(crop_img):
            g = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            _, th = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            return len([c for c in cnts if 15 < cv2.contourArea(c) < 5000])
        
        blobs_90 = count_text_blobs(crop_90)
        blobs_270 = count_text_blobs(crop_270)
        
        if blobs_270 >= blobs_90:
            return 270, rot_270
        else:
            return 90, rot_90
            
    # Check if vertical image is upside-down (180°)
    crop_top = image_bgr[:int(h * 0.25), :]
    crop_bot = image_bgr[int(h * 0.75):, :]
    def count_blobs(crop_img):
        g = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        _, th = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return len([c for c in cnts if 15 < cv2.contourArea(c) < 5000])
        
    top_blobs = count_blobs(crop_top)
    bot_blobs = count_blobs(crop_bot)
    if bot_blobs > top_blobs * 2.0 and bot_blobs > 30:
        return 180, cv2.rotate(image_bgr, cv2.ROTATE_180)
        
    return 0, image_bgr

def preprocess_memo_image(input_path, output_dir=None, user_rotation=0):
    """
    Full automated enhancement pipeline:
    1. Reads original image with EXIF orientation correction
    2. Automatically detects and rectifies 90°/180°/270° sideways photos
    3. Quality check (blur, brightness, contrast)
    4. Perspective warp / auto-deskew fine angles
    5. Removes shadows and uneven illumination
    6. Enhances faint handwriting with CLAHE and stroke sharpening
    7. Saves and returns enhanced and binarized image paths + quality metadata
    """
    if not os.path.exists(input_path):
        return PreprocessedResult(input_path, input_path)

    # 1. EXIF orientation handling using PIL
    try:
        with Image.open(input_path) as pil_img:
            transposed = ImageOps.exif_transpose(pil_img)
            transposed.save(input_path)
    except Exception as e:
        pass

    img = cv2.imread(input_path)
    if img is None:
        return PreprocessedResult(input_path, input_path)

    # 2. Automated 4-Way Orientation Detection & Rectification
    rot_angle, img = detect_and_auto_orient(img, user_rotation=user_rotation)
    if rot_angle != 0 or user_rotation != 0:
        # Overwrite input_path with upright image so UI preview and downstream OCR match
        cv2.imwrite(input_path, img)

    # 3. Quality Assessment
    quality = check_image_quality(img)

    # 4. Resize to optimal OCR resolution (1100px max for ultra-fast, accurate CPU inference)
    h, w = img.shape[:2]
    max_dim = max(h, w)
    if max_dim > 1100:
        scale = 1100.0 / max_dim
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    elif max_dim < 800:
        scale = 1000.0 / max_dim
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

    # 5. Perspective warp or fine deskew
    oriented = correct_perspective_and_crop(img)

    # 6. Remove shadows & balance illumination
    no_shadows = remove_shadows_and_normalize(oriented)

    # 7. Enhance handwriting contrast
    enhanced_gray = enhance_handwriting_contrast(no_shadows)

    # 8. Detect text candidate regions
    regions = detect_handwriting_regions(enhanced_gray)

    # Save enhanced outputs in writable directory
    import tempfile
    dir_name = output_dir or os.path.dirname(input_path)
    if not dir_name or not os.path.exists(dir_name) or not os.access(dir_name, os.W_OK):
        dir_name = "/tmp" if os.path.exists("/tmp") else tempfile.gettempdir()

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    enhanced_path = os.path.join(dir_name, f"{base_name}_enhanced.png")
    binarized_path = os.path.join(dir_name, f"{base_name}_binarized.png")

    try:
        enhanced_bgr = cv2.cvtColor(enhanced_gray, cv2.COLOR_GRAY2BGR)
        cv2.imwrite(enhanced_path, enhanced_bgr)
    except Exception:
        enhanced_path = input_path

    try:
        binarized = create_binarized_handwriting(enhanced_gray)
        cv2.imwrite(binarized_path, binarized)
    except Exception:
        binarized_path = input_path

    return PreprocessedResult(enhanced_path, binarized_path, quality=quality, regions=regions)

