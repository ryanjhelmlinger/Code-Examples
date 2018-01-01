#import Image
from PIL import Image
#from tesseract import image_to_string
import pytesseract
import io



pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
#pytesseract.pytesseract.tesseract_cmd = 'C:/Users/Ryan/AppData/Local/Programs/Python/Python36/Lib/site-packages/tesseract'
#pytesseract.pytesseract.tesseract_cmd = 'C:'
print("here")

#print image_to_string(Image.open('test.png'))
#with io.open('crosswordTest.png','r',encoding='utf8') as f: 
#	text = f.read()
#print("here2")
#inputFile = open(('crosswordTest.JPG', encoding="utf8"), "r")
#print(pytesseract.image_to_string(Image.open(text)))
print(pytesseract.image_to_string(Image.open('test.jpg')))