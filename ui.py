import gradio as gr
import cv2
from extract_text import extract_info
import os

def process_image(example_image=None, img=None):
    print(")"*29)
    print(example_image)
    print(img)
    print(type(img))
    print(type(example_image))
    if img is not None:
        img = img[:, :, ::-1]
    if example_image is not None and example_image !=[]:
        print("^"*13)
        print(os.path.join(os.path.dirname(os.path.abspath(__file__)), example_image))
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), example_image)
        img = cv2.imread(path)
    processed_image, info = extract_info(img=img)
    processed_image = processed_image[:, :, ::-1]
    return info, processed_image

examples = ["Example1.jpg", "Example2.jpg", "Example3.png"]
dropdown = gr.Dropdown(choices=examples, label="Select an example image")
image = gr.Image(label="Upload your own image")
output_image = gr.Image(label="Processed Image")#, value=None)
output_text = gr.Textbox(label="Extracted Information")

iface = gr.Interface(fn=process_image, inputs=[dropdown, image], outputs=[output_text, output_image], title="Image Processing")

iface.launch()