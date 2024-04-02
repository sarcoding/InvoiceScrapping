# Invoice Data Extraction Project README

## Overview
This project focuses on utilizing computer vision techniques to extract data from invoice images. It employs the Tesseract OCR engine via Pytesseract to extract text from images, which is then segmented into lines and blocks for further processing. The extracted text is then passed through regular expressions (regex) to identify and extract key information such as billing address (To), total amount, and GSTIN.

## Project Structure
- `ui.py`: This script creates a user interface using Gradio, allowing users to upload images or select example images from a dropdown menu for processing.
- `extract_text.py`: Contains functions for text extraction, segmentation into lines and blocks, and keyword-based extraction of invoice data using regex.

## Installation
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required packages using the `requirements.txt` file by running the following command:
   
   ```bash
   pip install -r requirements.txt
   
This command will install all the necessary dependencies, including Gradio, OpenCV (opencv-python), Pytesseract (pytesseract), Regex (regex), and NumPy (numpy).

## Running the Project
1. Run `ui.py` to start the user interface. This will create a local server accessible at http://127.0.0.1:7860/.
    ```bash
    python ui.py
    ```
2. Access the user interface in your web browser and follow the instructions provided in the interface or refer to the detailed instructions below.

## Detailed Instructions
1. **Opening the User Interface:**
- Open your web browser and navigate to http://127.0.0.1:7860/ after running `ui.py`.

2. **Selecting an Example Image:**
- Choose an example image from the dropdown menu labeled "Select Example" in the user interface.
- Example images are provided for demonstration purposes and can be selected to test the functionality.

3. **Submitting the Example Image:**
- After selecting an example image, click the "Submit" button on the user interface.
- Wait for the processing to complete. The output will be displayed, including the processed image with annotations (if applicable) and the extracted invoice data.

4. **Alternatively, Uploading an Image:**
- To upload your own image, click on the "Upload Image" button in the user interface.
- Select the image file from your device. Note that due to a current issue, you may need to click the "Clear" button once before uploading the image.

## Invoice Data Extraction
The invoice data extraction process involves the following steps:
1. Image Upload/Selection: The user uploads an invoice image or selects an example image for processing.
2. Text Extraction: Pytesseract is used to extract text from the image, which is segmented into lines and blocks.
3. Regex Processing: The extracted text is passed through regex patterns to identify variations of keywords related to billing address (To), total amount, and GSTIN.
4. Data Extraction: Relevant information such as the billing address, total amount, and GSTIN is extracted based on the identified keywords.

## Customization
- **Adding Keywords:** If specific keywords relevant to your invoice format are not extracted, you can add them to the `keywords` dictionary in the `extract_text.py` file for improved extraction accuracy.

## Dependencies
Ensure that you have the following packages installed:
- Gradio
- OpenCV (opencv-python)
- Pytesseract (pytesseract)
- Regex (regex)
- NumPy (numpy)

## Feedback and Issues
If you encounter any issues or have feedback regarding this project, please feel free to open an issue or reach out for assistance.
