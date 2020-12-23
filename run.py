def detect_text(path):
    # https://cloud.google.com/vision/docs/ocr#vision_text_detection-python
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    arr = []
    for text in texts:
        arr.append(text.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return arr

def isDate(text):
    count = 0
    for i in range(len(text)):
        if (text[i] == '-'): count += 1
    return (count == 2)

def refine(texts):
    arr = []
    i = 0
    for text in texts:
        if (isDate(text) or text[0] == '$'):
            arr.append(text)
        i += 1
    return arr

def createHeaders(workbook):
    col = 0
    titles = [chr(i) for i in range(ord('a'),ord('z')+1)]
    titles[0] = "date"
    for title in titles:
        worksheet.write(0, col, title)
        col += 1  

def excel(arr, workbook, row):
    col = 0
    for stuff in arr:
        worksheet.write(row, col, stuff)
        col += 1
    

if __name__ == '__main__':
    import argparse
    import xlsxwriter
    import glob

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', help='The name for excel file.')
    args = parser.parse_args()
    
    # create excel sheet
    workbook = xlsxwriter.Workbook(args.file_name + ".xlsx")
    worksheet = workbook.add_worksheet()
    createHeaders(workbook)

    # find all images
    print(glob.glob("./receipts/*.jpg"))
    receipts = glob.glob("./receipts/*.jpg")
    size = len(receipts) + 1
    
    for i in range(1, size):
        arr = detect_text(receipts[i-1])
        arr = refine(arr)
        print(arr)
        excel(arr, workbook, i)
    workbook.close()