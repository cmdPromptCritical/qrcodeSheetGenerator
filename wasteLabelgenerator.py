# Script which accepts a list of dictionaries that can be then encoded onto a 4x5 grid of labels.
# 4 labels per page
# can run without arguments, with list of dictionaries passed in the labels variable
# or run with arguments, such as: python labelgenerator.py '[{"drumID": 3344334, "volume": "334 mL", ...}, {...}]'
# uses Avery 1.5" square labels 4x5 grid (not print to the edge type)
# prints should be done with windows photo viewer, with thin borders and 'fit to page' setting enabled
# alignment may need tweaking depending on printer/print settings

import json
from PIL import Image, ImageDraw, ImageFont
import sys

def split(list, chunkSize):
    for i in range(0, len(list), chunkSize):
        yield list[i:i + chunkSize]

### CONFIG
labels = [
    {"drumID": '', "volume": "", "samplePurpose": "", "sampleNumber": '', "samplesTotal": '', "sampleDate": "", "sampledBy": ""},
    {"drumID": '', "volume": "", "samplePurpose": "", "sampleNumber": '', "samplesTotal": '', "sampleDate": "", "sampledBy": ""},
    {"drumID": '', "volume": "", "samplePurpose": "", "sampleNumber": '', "samplesTotal": '', "sampleDate": "", "sampledBy": ""},
    {"drumID": '', "volume": "", "samplePurpose": "", "sampleNumber": '', "samplesTotal": '', "sampleDate": "", "sampledBy": ""}
    #{"drumID": '', "volume": "335 mL", "samplePurpose": "testing", "sampleNumber": 2, "samplesTotal": 4, "sampleDate": "2024-05-01", "sampledBy": "John"},
    # Add more dictionaries as needed
]

if len(sys.argv) > 1:
    labels = json.loads(sys.argv[1])

CHUNK_SIZE = 4
print(labels)
### END CONFIG

# Load the 1.5" square image template
template = Image.open("template.png")  # Make sure to have this file in the same directory
template = template.resize((390,390))

# chunk label list into lists of 4
labels_chunked = list(split(labels, CHUNK_SIZE))

# iterate over list of chunks
for i, chunk in enumerate(labels_chunked):
    # for every list, create a label printout page
    # create canvas
    cf = 3.125
    x = 2550
    y = 3300
    img = Image.new(mode="RGBA", size=(x,y), color='white')

    # load background image
    backgr = img.copy()
    
    # for each label, paste it
    for j, label in enumerate(chunk):
        # Calculate positions
        positions = [
            (int((j*2.08+0.41)*x/8.5), int((4.8/8)*y/11)),
            (int((j*2.08+0.41)*x/8.5), int((1*(1.565+9/16)+4.8/8)*y/11)),
            (int((j*2.08+0.41)*x/8.5), int((2*(1.565+9/16)+4.8/8)*y/11)),
            (int((j*2.08+0.41)*x/8.5), int((3*(1.565+9/16)+4.8/8)*y/11)),
            (int((j*2.08+0.41)*x/8.5), int((4*(1.565+9/16)+4.8/8)*y/11))
        ]
        
        for pos in positions:
            # Paste the template
            backgr.paste(template, pos, template)

            draw = ImageDraw.Draw(backgr)
            font = ImageFont.truetype('Arial.ttf', 20)

            # add text details
            draw.text((pos[0]+240, pos[1]+65), f"{label['drumID']}", fill='black', font=font)
            draw.text((pos[0]+240, pos[1]+110), f"{label['volume']}", fill='black', font=font)
            draw.text((pos[0]+240, pos[1]+155), f"{label['samplePurpose']}", fill='black', font=font)
            draw.text((pos[0]+150, pos[1]+205), f"{label['sampleNumber']}", fill='black', font=font)
            draw.text((pos[0]+250, pos[1]+205), f"{label['samplesTotal']}", fill='black', font=font)
            draw.text((pos[0]+200, pos[1]+295), f"{label['sampleDate']}", fill='black', font=font)
            draw.text((pos[0]+200, pos[1]+340), f"{label['sampledBy']}", fill='black', font=font)
        
        # initialize draw text 
        draw = ImageDraw.Draw(backgr)

        # draw line separator between each image set
        draw.line([((j*200+20)*cf,0), ((j*200+20)*cf,y)], width=4, fill='black')

        # add text headers at specific locations
        font = ImageFont.truetype('Arial.ttf', 32)
        draw.text(((j*199.86+141)*cf, 30*cf), f"Drum {label['drumID']}", fill='black', font=font)

    # draw instructions at bottom of page
    draw.text((141*cf, 3160), f'open up image and hit CTRL+P to print', fill='black', font=font)

    backgr.save(f'LABELS_PRINT_ME_{i}.png')
    #backgr.show()
print('done')