import gradio as gr
import cv2
from extract_text import extract_info

def process_image(example_image=None, img=None):

    if img is not None:
        img = img[:, :, ::-1]
    if example_image is not None:
        example_image = cv2.imread(example_image)
    processed_image, info = extract_info(img=img, example_image=example_image)
    processed_image = processed_image[:, :, ::-1]
    return info, processed_image

examples = ["Example1.jpg", "Example2.jpg", "Example3.png"]
dropdown = gr.Dropdown(choices=examples, label="Select an example image")
image = gr.Image(label="Upload your own image")
output_image = gr.Image(label="Processed Image")
output_text = gr.Textbox(label="Extracted Information")

iface = gr.Interface(fn=process_image, inputs=[dropdown, image], outputs=[output_text, output_image], title="Image Processing")

iface.launch()