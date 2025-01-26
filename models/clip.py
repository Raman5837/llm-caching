from typing import Dict, List, Tuple

import clip
import torch
from PIL import Image
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import Compose, Normalize, Resize, ToTensor

from models import BaseLLM
from utils import ImageProcessor


class Clip(BaseLLM):
    """
    Clip Interface
    """

    def __init__(self) -> None:
        self.__device: str = "cpu"
        # [ViT-B/16, ViT-B/32, ViT-L/14]
        self.__model, self.__preprocessor = clip.load("ViT-L/14", device=self.__device)
        self.__detection_model = fasterrcnn_resnet50_fpn(weights=True).to(self.__device)

        self.__detection_model.eval()

        self.__image_processor = ImageProcessor

    def execute(self, file_path: str, threshold: float = 0.5) -> Tuple:
        """ """

        # transform = Compose([ToTensor()])
        transform = Compose([Resize((224, 224)), ToTensor(), Normalize((0.5,), (0.5,))])
        image = Image.open(file_path).convert("RGB")
        source_image = transform(image).unsqueeze(0).to(self.__device)

        with torch.no_grad():
            detections = self.__detection_model(source_image)[0]

        boxes = detections["boxes"][detections["scores"] > threshold]
        labels = detections["labels"][detections["scores"] > threshold]

        return detections, image, boxes, labels

    def metadata(self, boxes: torch.Tensor, labels: torch.Tensor) -> List[Dict]:
        """ """

        return [
            {"label": label.item(), "box": box.tolist()}
            for box, label in zip(boxes, labels)
        ]

    def extract_labels(self, image: Image.Image, boxes: torch.Tensor) -> List[str]:
        """
        Extract text labels from OCR results for each bounding box.
        """

        labels = []
        image_data = self.__image_processor(image=image).ocr()

        print(f"OCR Data: {image_data}")
        print(f"Bounding Boxes: {boxes.tolist()}")

        width, height = image.size

        scaled_boxes = boxes.clone()
        scaled_boxes[:, [0, 2]] *= width
        scaled_boxes[:, [1, 3]] *= height

        for box in scaled_boxes:
            text: List[str] = []
            x_min, y_min, x_max, y_max = map(int, box.tolist())

            for data in image_data:
                x, y = data["x"], data["y"]
                width, height = data["width"], data["height"]
                x_end, y_end = x + width, y + height

                if (
                    (x_min <= x <= x_max and y_min <= y <= y_max)
                    or (x_min <= x_end <= x_max and y_min <= y_end <= y_max)
                    or (x <= x_min <= x_end and y <= y_min <= y_end)
                    or (x <= x_max <= x_end and y <= y_max <= y_end)
                ) and data["text"].strip():
                    text.append(data["text"].strip())

            if text:
                labels.append(" ".join(text))

        return labels

    def embedding(self, image: Image.Image, boxes: torch.Tensor) -> torch.Tensor:
        """ """

        embeddings: List = []
        for box in boxes:
            box = box.int().cpu().numpy()
            region = image.crop((box[0], box[1], box[2], box[3]))
            tensor = self.__preprocessor(region).unsqueeze(0).to(self.__device)

            with torch.no_grad():
                embedding = self.__model.encode_image(tensor)

            embeddings.append(embedding)

        return torch.cat(embeddings, dim=0)

    def search(self, label: str, regions: torch.Tensor) -> int:
        """ """

        with torch.no_grad():
            normalized_regions = torch.nn.functional.normalize(regions, p=2, dim=-1)
            label_embedding = self.__model.encode_text(
                clip.tokenize(label).to(self.__device)
            )
            normalized_label_embedding = torch.nn.functional.normalize(
                label_embedding, p=2, dim=-1
            )

            # embedding = self.__model.encode_text(clip.tokenize(label).to(self.__device))
            # normalized_embedding = torch.nn.functional.normalize(embedding, p=2, dim=-1)

        # similarities = torch.nn.functional.cosine_similarity(normalized_embedding, regions)
        similarities = torch.nn.functional.cosine_similarity(
            normalized_label_embedding, normalized_regions
        )
        closest_match_index = similarities.argmax().item()
        # print(f"[Clip]: similarity % {similarities[closest_match_index].item()}")

        return closest_match_index
