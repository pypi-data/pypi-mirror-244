import os
from dataclasses import dataclass

import numpy as np
import supervision as sv
from autodistill.detection import CaptionOntology, DetectionBaseModel
from PIL import Image
from transformers import AltCLIPModel, AltCLIPProcessor
from autodistill.helpers import load_image
import torch

HOME = os.path.expanduser("~")


@dataclass
class AltCLIP(DetectionBaseModel):
    ontology: CaptionOntology

    def __init__(self, ontology: CaptionOntology):
        self.ontology = ontology
        self.model = AltCLIPModel.from_pretrained("BAAI/AltCLIP")
        self.processor = AltCLIPProcessor.from_pretrained("BAAI/AltCLIP")

    def predict(self, input: str, confidence: int = 0.5) -> sv.Classifications:
        image = load_image(input, return_format="PIL")

        prompts = ["a photo of" + prompt for prompt in self.ontology.prompts()]

        inputs = self.processor(
            text=prompts, images=image, return_tensors="pt", padding=True
        )

        outputs = self.model(**inputs)
        logits_per_image = (
            outputs.logits_per_image
        )  # this is the image-text similarity score
        probs = logits_per_image.softmax(dim=1).tolist()

        # drop prompts which have confidence less than the threshold
        probs = list(zip(prompts, probs[0]))

        # filter out prompts with confidence less than the threshold
        probs = [i for i in probs if i[1] > confidence]

        return sv.Classifications(
            class_id=np.array([prompts.index(i[0]) for i in probs]),
            confidence=np.array([i[1] for i in probs]),
        )
    
    def embed_text(self, input: str) -> np.ndarray:
        with torch.no_grad():
            inputs = self.processor(text=input, return_tensors="pt")
            text_features = self.model.get_text_features(**inputs)

            return text_features.cpu().numpy()
    
    def embed_image(self, input: str) -> np.ndarray:
        image = Image.open(input)
        with torch.no_grad():
            inputs = self.processor(images=image, return_tensors="pt")
            image_features = self.model.get_image_features(**inputs)

            return image_features.cpu().numpy()