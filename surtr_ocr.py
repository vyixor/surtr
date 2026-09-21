import pytesseract
import cv2  # OpenCV - for image processing
import sys
import os
import numpy as np
from collections import defaultdict
from PIL import Image,ImageGrab,ImageDraw

def screenread(language, ocr_path, desktop_path):
    try:
        pytesseract.pytesseract.tesseract_cmd = ocr_path
        # Load the image using OpenCV
        img = cv2.imread(desktop_path)
        # Convert image to grayscale for better OCR results
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        data = pytesseract.image_to_data(gray,lang=language, output_type=pytesseract.Output.DICT)
        return data
    
    except Exception as e:
          raise type(e)("Text OCR error")
          
              
def readimage(options="image",path=None,language=None, ocr_path=None ,itype=""):
  
  if options == "languages":
      lan = pytesseract.get_languages(config='')
      return lan
  
          
  elif options == "image":
    pytesseract.pytesseract.tesseract_cmd = ocr_path 
    img = path  
    if itype == "useBlackWhite":
      im_gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
      (thresh, im_bw) = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
      thresh = 127
      im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
      cv2.imwrite('imgedit.png', im_bw)

    elif (itype == "useGray"):
        image_file = Image.open(img) # opens image  
        image_file = image_file.convert('LA') # converts to grayscale w/ alpha
        image_file.save('imgedit.png') # saves image result into new file
    else:
        img = cv2.imread(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        data = pytesseract.image_to_data(gray,lang=language, output_type=pytesseract.Output.DICT)
        return data
    
    data = pytesseract.image_to_data(Image.open('imgedit.png'),lang=language, output_type=pytesseract.Output.DICT)                  
    return data




def read_screen_sentence(language="eng", ocr_path = None, desktop_path = None):
  try:  
    pytesseract.pytesseract.tesseract_cmd = ocr_path  # Set your tesseract path
    img = cv2.imread(desktop_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_data(gray,lang=language, output_type=pytesseract.Output.DICT)

    return [img,data]
  
  except Exception as e:
    raise type(e)("Text OCR error")
     
  
  
def textloop(language="eng",ocr_path=None, desktop_path=None):
  try:
    pytesseract.pytesseract.tesseract_cmd = ocr_path
    img = cv2.imread(desktop_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_data(gray, lang=language, output_type=pytesseract.Output.DICT)
    return data
    
  except Exception as e:
    raise type(e)("Text OCR error")    

  
  
  


# Adjust this path to where Tesseract is installed on your system


def reconstruct_text_layout(
    image_path,
    ocr_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    lang="eng",
    min_conf=35,
    transform="gray",
    char_width=7.8,
    line_height=18,
    psm=6,
    save_txt=None,
    print_result=True
):
    """
    Reconstructs text layout from an image and:
      - prints it to console (if print_result=True)
      - optionally saves it to a text file (if save_txt is provided)

    Parameters:
    -----------
    image_path : str
        Path to the input image
    lang : str
        Language code for Tesseract (default: "eng")
    min_conf : int
        Minimum confidence level for detected words (0-100)
    char_width : float
        Approximate width of one character in pixels (tune for your font/size)
    line_height : float
        Approximate height of one text line in pixels
    psm : int
        Page segmentation mode (Tesseract flag)
        Common useful values:
          3  → Fully automatic page segmentation (default)
          4  → Assume a single column of text
          6  → Assume a single uniform block of text (often good for receipts/forms)
    save_txt : str or None
        If provided, saves the reconstructed layout to this text file
    print_result : bool
        Whether to print the reconstructed layout to console (default: True)

    Returns:
    --------
    list of str
        List of reconstructed lines (with spacing)
    """
    pytesseract.pytesseract.tesseract_cmd = ocr_path

    # ─── Load & preprocess ─────────────────────────────────────────────────
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot load image: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Decide what image Tesseract should see
    ocr_input = gray
    if transform == "bw":
      # Apply Otsu binarization (change to black and white)
      _, ocr_input = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
      )
        
    # ─── OCR with position information ─────────────────────────────────────
    config = f"--oem 3 --psm {psm} -c preserve_interword_spaces=1"
    data = pytesseract.image_to_data(
        ocr_input,
        lang=lang,
        config=config,
        output_type=pytesseract.Output.DICT
    )

    # ─── Group words by approximate line ───────────────────────────────────
    lines = defaultdict(list)  # line_key → list of (column, word)

    for i in range(len(data["text"])):
        word = data["text"][i].strip()
        if not word:
            continue
        if int(data["conf"][i]) < min_conf:
            continue

        left = data["left"][i]
        top = data["top"][i]

        # Bucket into approximate lines
        line_key = round(top / line_height) * line_height
        # Approximate column in character units
        col = round(left / char_width)

        lines[line_key].append((col, word))

    # ─── Build final layout lines ──────────────────────────────────────────
    layout_lines = []

    for _, words in sorted(lines.items()):
        # Sort words left to right
        words.sort(key=lambda x: x[0])

        line = ""
        last_col = 0

        for col, word in words:
            gap = col - last_col - len(line)
            if gap > 0:
                line += " " * gap
            line += word
            last_col = col + len(word)

        layout_lines.append(line.rstrip())

    # ─── Output ────────────────────────────────────────────────────────────
    if print_result and layout_lines:
        print("\nReconstructed text layout:\n" + "─" * 100)
        for line in layout_lines:
            print(line)
        print("─" * 100)

    # ─── Optional save to file ─────────────────────────────────────────────
    if save_txt and layout_lines:
        try:
            with open(save_txt, "w", encoding="utf-8") as f:
                f.write(f"Reconstructed layout from: {image_path}\n")
                f.write("═" * 80 + "\n")
                for line in layout_lines:
                    f.write(line + "\n")
                f.write("═" * 80 + "\n")
            print(f"Saved layout to: {save_txt}")
        except Exception as e:
            raise type(e)(f"Failed to save file: {e}")

    return layout_lines


  