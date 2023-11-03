from huggingface_hub import hf_hub_download
import re
import os

url = r'D:\data\ranking\Kinga_Wytrychiewicz_2.pdf'
from pdf2image import convert_from_path, convert_from_bytes
pages = convert_from_path(url)
file_name = url.strip('.pdf').split('\\')[-1]
png_url = r'D:\data\ranking\png'



if not os.path.exists(os.path.join(png_url, file_name)):
    os.makedirs(os.path.join(png_url, file_name))

for idx, page in enumerate(pages):
    page.save(os.path.join(png_url, file_name, f'{idx}.png'), 'PNG')


from transformers import NougatProcessor, VisionEncoderDecoderModel
import torch

processor = NougatProcessor.from_pretrained("facebook/nougat-base")
model = VisionEncoderDecoderModel.from_pretrained("facebook/nougat-base")
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
image_path = r"D:\data\ranking\png\Kinga_Wytrychiewicz_2\0.png"
model.to(device)
# prepare PDF image for the model
image = Image.open(image_path)
pixel_values = processor(image, return_tensors="pt", data_format="channels_first").pixel_values

# generate transcription (here we only generate 30 tokens)
outputs = model.generate(
    pixel_values.to(device),
    min_length=1,
    max_new_tokens=3000,
    bad_words_ids=[[processor.tokenizer.unk_token_id]],
)

sequence = processor.batch_decode(outputs, skip_special_tokens=True)[0]
sequence = processor.post_process_generation(sequence, fix_markdown=False)