import os
import json
from timeit import default_timer as timer

def find(name, path):
  for root, dirs, files in os.walk(path):
    if name in files:
      return os.path.join(root, name)

run_inference_path = find("run_inference.py", "/")
check_point_path = find("newmodel.ckpt-2000000","/")
vocabulary_path = find("word_counts.txt"."/")
print(run_inference_path)

# Run run_inference.py
os.system("python /container/workspace/im2txt/run_inference.py --checkpoint_path /container/workspace/im2txt/model/newmodel.ckpt-2000000 --vocab_file /container/workspace/im2txt/data/word_counts.txt --input_files /container/workspace/im2txt/data/images/image.jpg")

def generateCaption(image_name):
  # The caption data will be written to /container/captionData/captions.txt
  # we read the content of caption.txt in captionData and return it here
  caption_json_path = "/container/workspace/captionData/captionFile.txt"
  captions = ""
  with open(caption_json_path) as json_file:
    caption_string_restored = json.load(json_file)
    print("caption_string_restored: " + caption_string_restored)
    caption_json = json.loads(caption_string_restored)
    captions += caption_json['caption0']
    captions += " "
    captions += caption_json['caption1']
    captions += " "
    captions += caption_json['caption2']
  return captions

def predict(resized_image_path):
  start = timer()
  generated_caption = generateCaption(resized_image_path)
  end = timer()
  time_elapsed = end - start
  return generated_caption, time_elapsed
