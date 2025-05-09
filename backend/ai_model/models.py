import torch, torchvision, random, os
from torchvision import transforms
from PIL import Image, ImageDraw

class FasterRCNN_Resnet50_FPN_nonpretrain_epoch19():
    def __init__(self):
        self.class_names = [
            "Bacterial_Leaf_Blight",
            "Brown_Spot",
            "HealthyLeaf",
            "Leaf_Blast",
            "Leaf_Scald",
            "Narrow_Brown_Leaf_Spot",
            "Neck_Blast",
            "Rice_Hispa",
        ]
        self.device = ("cuda" if torch.cuda.is_available() else "cpu")
        self.transform = transforms.Compose([transforms.ToTensor()])
        
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn()
        in_features = self.model.roi_heads.box_predictor.cls_score.in_features
        self.model.roi_heads.box_predictor = torchvision.models.detection.faster_rcnn.FastRCNNPredictor(in_features, len(self.class_names))
        self.model.eval()
        model_file_path = os.path.join(os.path.dirname(__file__), "fasterrcnn_resnet50_fpn_v2_nonpretrain_19epochs.pth")
        self.model.load_state_dict(torch.load(model_file_path, map_location=self.device))
        self.model.to(self.device)


    def predict(self, image_path, save_to_path=None, confidence_threshold=0.5):
        img = Image.open(image_path).convert("RGB")
        img_tensor = self.transform(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            predictions = self.model(img_tensor)[0]
        results = []
        draw = ImageDraw.Draw(img)
        label_colors = {label: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for label in range(len(self.class_names))}
        for box, label, score in zip(predictions["boxes"], predictions["labels"], predictions["scores"]):
            if score >= confidence_threshold:
                box = box.tolist()
                label_name = self.class_names[label.item()]
                if (label_name == "HealthyLeaf"):
                    continue

                color = label_colors[label.item()]
                results.append(
                    {
                        "score": score.item(),
                        "label": label_name,
                        "box": box
                    }
                )
                draw.rectangle(box, outline=color, width=3)
                draw.text((box[0], box[1] - 15), f"{label_name}: {score:.2f}", fill='red', stroke_fill="white", stroke_width=1)
        if save_to_path:
            img.save(save_to_path)
        return results


Model = FasterRCNN_Resnet50_FPN_nonpretrain_epoch19()
