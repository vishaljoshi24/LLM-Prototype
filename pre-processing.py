import os
import pdfplumber
import camelot
import cv2
import numpy as np
import pdf2image

#This is the path to the folder containing the character sheets
folder_path = 'C:/Users/we19383/OneDrive - University of Bristol/GitHub/LLM-Prototype/Premade Character Sheets'

#Iterating through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.pdf'):
        #Full path to the PDF file
        pdf_file_path = os.path.join(folder_path, filename)

        #Open the PDF file
        with pdfplumber.open(pdf_file_path) as pdf:
            #Iterate through each page in the PDF
            for page in pdf.pages:
                #Extract text from the page
                page_text = page.extract_text()
                # Print or process the extracted text
                # print(page_text)

        # Extract tables from the PDF
        tables = camelot.read_pdf(pdf_file_path, flavor='stream')

        # Process each table
        # for i, table in enumerate(tables):
        #     print(f"Table {i+1} from {filename}:")
        #     print(table.df)
        #     print("\n")

        #Convert PDF to images
        images = pdf2image.convert_from_path(pdf_file_path)

        # Process each page image
        for i, pil_image in enumerate(images):
            # Convert PIL Image to NumPy array
            image = np.array(pil_image)

            gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

            #Apply thresholding to segment the image
            _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            #Find contours in the binary image
            contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # Iterate through each contour
            for contour in contours:
                # Compute the area of the contour
                area = cv2.contourArea(contour)

                # Filter contours based on area (adjust threshold as needed)
                if area > 1000:
                    # Draw contour on the original image (for visualization)
                    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

                    # Extract the bounding box of the contour
                    x, y, w, h = cv2.boundingRect(contour)

                    # Extract the chart region from the original image
                    chart_region = image[y:y+h, x:x+w]

                    # Save the chart region as an image
                    # chart_filename = f"{filename}_page_{i+1}_chart_{len(contours)}.jpg"
                    # chart_path = os.path.join(folder_path, chart_filename)
                    # cv2.imwrite(chart_path, chart_region)

                    # Optionally, perform further processing or analysis on the chart region

            # Display or save the original image with contours drawn (for visualization)
            # cv2.imshow('Image with Contours', image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()










