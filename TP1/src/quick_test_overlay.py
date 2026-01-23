# TP1/src/quick_test_overlay.py (à créer) ou exécuter dans un python interactif
import numpy as np
import cv2
from pathlib import Path

from sam_utils import load_sam_predictor, predict_mask_from_box
from geom_utils import mask_area, mask_bbox, mask_perimeter
from viz_utils import render_overlay

img_path = next(Path("TP1/data/images").glob("jonathan-borba-af7c0GwLsGU-unsplash.jpg"))  # adaptez si besoin
bgr = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

ckpt = "TP1/models/sam_vit_h_4b8939.pth"
pred = load_sam_predictor(ckpt, model_type="vit_h")

# box = np.array([50, 50, 250, 250], dtype=np.int32)  # adaptez

H, W, _ = rgb.shape

box = np.array([
    int(0.25 * W),  # x1
    int(0.15 * H),  # y1
    int(0.75 * W),  # x2
    int(0.85 * H),  # y2
], dtype=np.int32)


mask, score = predict_mask_from_box(pred, rgb, box, multimask=True)

m_area = mask_area(mask)
m_bbox = mask_bbox(mask)
m_per = mask_perimeter(mask)

overlay = render_overlay(rgb, mask, box, alpha=0.5)

out_dir = Path("TP1/outputs/overlays")
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / f"overlay_{img_path.stem}.png"

# Sauvegarde via OpenCV (BGR)
cv2.imwrite(str(out_path), cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))

print("score", score, "area", m_area, "bbox", m_bbox, "perimeter", m_per)
print("saved:", out_path)