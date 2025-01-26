from typing import Dict, List, Tuple, Union

from PIL import Image, ImageFile

BoxT = Dict[str, Union[int, float]]
CoordsT = Tuple[int, int, int, int]


class BoxUtility:
    """
    Contains utility methods related to boxes and coordinates
    """

    def format(self, box: BoxT) -> CoordsT:
        """
        Returns box coordinates in the form of a tuple (x_min, y_min, x_max, y_max)
        """

        return (
            int(box["x_min"]),
            int(box["y_min"]),
            int(box["x_max"]),
            int(box["y_max"]),
        )

    def absolute_pixels(self, path: str, box: BoxT) -> CoordsT:
        """
        Converts normalized coordinates to absolute pixel values based on image dimensions.
        """

        image: ImageFile.ImageFile = Image.open(path)
        width, height = image.size

        x_min = int(box["x_min"] * width)
        y_min = int(box["y_min"] * height)
        x_max = int(box["x_max"] * width)
        y_max = int(box["y_max"] * height)

        return (x_min, y_min, x_max, y_max)

    def IOU(self, box1: CoordsT, box2: CoordsT) -> float:
        """
        Calculate Intersection over Union (IoU) between two bounding boxes.
        """

        print(f"[BoxUtility]: {box1=} and {box2=}")

        # Intersection coordinates
        x_min_inter = max(box1[0], box2[0])
        y_min_inter = max(box1[1], box2[1])
        x_max_inter = min(box1[2], box2[2])
        y_max_inter = min(box1[3], box2[3])

        # Width and height of the intersection
        inter_width = max(0, x_max_inter - x_min_inter)
        inter_height = max(0, y_max_inter - y_min_inter)

        # Area of intersection
        inter_area = inter_width * inter_height
        print(f"[BoxUtility]: {inter_area=}")

        # Area of both boxes
        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

        # Area of union
        union_area = box1_area + box2_area - inter_area
        print(f"[BoxUtility]: {union_area=}")

        return inter_area / union_area if union_area > 0 else 0

    def merge_boxes(
        self, path: str, boxes: List[BoxT], iou_threshold: float = 0.5
    ) -> List[CoordsT]:
        """
        Merge overlapping bounding boxes based on IoU.
        Converts normalized boxes to absolute pixels and returns merged absolute pixel boxes.
        """

        absolute_boxes: List[CoordsT] = [
            self.absolute_pixels(path, box) for box in boxes
        ]

        merged: List[CoordsT] = []

        while absolute_boxes:
            current_box = absolute_boxes.pop(0)
            overlapping_boxes = []

            for box in absolute_boxes:
                iou = self.IOU(current_box, box)

                if iou > iou_threshold:
                    current_box = (
                        min(current_box[0], box[0]),
                        min(current_box[1], box[1]),
                        max(current_box[2], box[2]),
                        max(current_box[3], box[3]),
                    )
                else:
                    overlapping_boxes.append(box)

            merged.append(current_box)
            absolute_boxes = overlapping_boxes

        print(f"[BoxUtility]: Merged Boxes (Absolute Pixels): {merged}")
        return merged
