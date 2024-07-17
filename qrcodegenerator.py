# Script which accepts a list of strings that can be then encoded onto a 4x5 grid of QR codes.
# 4 strings per page
# can run without arguments, with list of strings passed in the qr_codes variable
# or run with arguments, such as: python qrcodegenerator.py 5000,5001,5002,5003...
# uses Avery 1.5" square labels 4x5 grid (not print to the edge type)
# prints should be done with windows photo viewer, with thin borders and 'fit to page' setting enabled
# alignment may need tweaking depending on printer/print settings
def split(list, chunkSize):
    for i in range(0, len(list), chunkSize):
        yield list[i:i + chunkSize]

from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter
#import qrcode
import segno
import io
import sys

### CONFIG
qr_codes = ['5000', '5001', '5002', '5003', '5004']
if sys.argv[1]:
    qr_codes = sys.argv[1].split(',')
CHUNK_SIZE = 4
print(qr_codes)
#qr = qrcode.QRCode(
#    version=1,
#    error_correction=qrcode.constants.ERROR_CORRECT_L,
#    border=0,
#    box_size=21
#)

### END CONFIG

# chunk qr code list into lists of 4
qr_codes_chunked = split(qr_codes, CHUNK_SIZE)

# iterate over list of chunks
for i, k in enumerate(qr_codes_chunked):
    # for ever list, create a qr code printout page
    # create canvas
    cf = 3.125
    x = 2550
    y = 3300
    img = Image.new(mode="RGBA", size=(x,y), color='white') # multiply inkscape values by 3.125

    # load background image
    backgr = img.copy()
    
    # for each qr code, paste it
    for j, qrcode in enumerate(k):
        # paste qr codes to background image
        # initialize temp storage of qr code
        out = io.BytesIO()

        # generate qr code, save to outstream, and load it into PIL
        qr = segno.make(f'{qrcode}', micro=False)
        qr.save(out, scale=19, kind='png', border=0)
        im1 = Image.open(out)
        
        # paste qr onto 
        #backgr.paste(im1,(int((j*199.86+41)*cf),int((53.73)*cf)))
        #backgr.paste(im1,(int((j*199.86+41)*cf),int((1*204.22+53.73)*cf)))
        #backgr.paste(im1,(int((j*199.86+41)*cf),int((2*204.22+53.73)*cf)))
        #backgr.paste(im1,(int((j*199.86+41)*cf),int((3*204.22+53.73)*cf)))
        #backgr.paste(im1,(int((j*199.86+41)*cf),int((4*204.22+53.73)*cf)))
        # IF statement used to avoid generating a QR code of value "" for blank inputs
        if qrcode:
            backgr.paste(im1,(int((j*2.08+0.41)*x/8.5),int((4.8/8)*y/11)))
            backgr.paste(im1,(int((j*2.08+0.41)*x/8.5),int((1*(1.565+9/16)+4.8/8)*y/11)))
            backgr.paste(im1,(int((j*2.08+0.41)*x/8.5),int((2*(1.565+9/16)+4.8/8)*y/11)))
            backgr.paste(im1,(int((j*2.08+0.41)*x/8.5),int((3*(1.565+9/16)+4.8/8)*y/11)))
            backgr.paste(im1,(int((j*2.08+0.41)*x/8.5),int((4*(1.565+9/16)+4.8/8)*y/11)))
            
        # initialize draw text 
        draw = ImageDraw.Draw(backgr)

        # draw line separator between each qr code set
        draw.line([((j*200+20)*cf,0), ((j*200+20)*cf,y)], width=4, fill='black')

        # add text headers at specific locations
        font = ImageFont.truetype('Arial.ttf', 32)
        draw.text(((j*199.86+141)*cf, 30*cf), f'{qrcode}', fill='black', font=font)

        # draw instructions at bottom of page
        draw.text(((141)*cf, 3160), f'open up image and hit CTRL+P to print', fill='black', font=font)



    backgr.save(f'QR_CODES_PRINT_ME_{i}.png')
    #backgr.show()
print('done')
