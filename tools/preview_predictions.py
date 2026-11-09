"""Chạy YOLO26n pretrained trên ảnh train và so sánh với nhãn CP2 của bạn.

Mục đích: xem thử model pretrained nhận được gì trên ảnh của bộ dữ liệu,
để tham khảo khi tự gán nhãn (không thay thế việc gán nhãn thủ công).

Cách dùng (chạy từ thư mục gốc repo):
    python tools/preview_predictions.py                     # 1 ảnh đầu tiên
    python tools/preview_predictions.py --image drive_003   # ảnh cụ thể
    python tools/preview_predictions.py --count 5           # 5 ảnh đầu tiên

Kết quả lưu ở outputs/preview/: ảnh vẽ box prediction (màu đỏ) và
box nhãn CP2 (màu xanh lá, nếu file nhãn đã tồn tại).
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "dataset" / "images" / "train"
LABELS_DIR = REPO_ROOT / "dataset" / "labels" / "train"
OUT_DIR = REPO_ROOT / "outputs" / "preview"

CLASS_NAMES = {0: "car", 1: "truck", 2: "bus", 3: "van"}

# Model pretrained học trên COCO; map tên class COCO sang schema của bài.
# COCO không có class "van", nên không có prediction nào được nhận là van.
COCO_TO_SCHEMA = {"car": "car", "truck": "truck", "bus": "bus"}


def draw_gt_boxes(image, label_path):
    """Vẽ box nhãn CP2 (xanh lá) từ file YOLO label, nếu có."""
    if not label_path.exists():
        return image, 0
    import cv2

    h, w = image.shape[:2]
    count = 0
    for line in label_path.read_text().splitlines():
        parts = line.split()
        if len(parts) != 5:
            continue
        cls, xc, yc, bw, bh = (float(p) for p in parts)
        x1 = int((xc - bw / 2) * w)
        y1 = int((yc - bh / 2) * h)
        x2 = int((xc + bw / 2) * w)
        y2 = int((yc + bh / 2) * h)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 200, 0), 2)
        cv2.putText(
            image,
            f"GT {CLASS_NAMES.get(int(cls), cls)}",
            (x1, max(12, y1 - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 200, 0),
            1,
        )
        count += 1
    return image, count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", default=None, help="tên ảnh không đuôi, vd drive_003")
    parser.add_argument("--count", type=int, default=1, help="số ảnh xử lý (mặc định 1)")
    parser.add_argument("--conf", type=float, default=0.25, help="ngưỡng confidence")
    args = parser.parse_args()

    images = sorted(IMAGES_DIR.glob("*.jpg"))
    if not images:
        sys.exit(f"Không tìm thấy ảnh trong {IMAGES_DIR}")

    if args.image:
        images = [p for p in images if p.stem == args.image]
        if not images:
            sys.exit(f"Không tìm thấy ảnh {args.image}.jpg")

    images = images[: args.count]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    import cv2
    from ultralytics import YOLO

    model = YOLO("yolo26n.pt")  # model pretrained, chỉ để tham khảo

    for img_path in images:
        image = cv2.imread(str(img_path))
        if image is None:
            print(f"Bỏ qua (đọc được không?): {img_path.name}")
            continue

        results = model(img_path, conf=args.conf, verbose=False)
        pred = results[0]

        # Vẽ prediction của model (đỏ) — map tên class COCO về schema
        pred_count = 0
        for box in pred.boxes:
            coco_name = pred.names[int(box.cls.item())]
            if coco_name not in COCO_TO_SCHEMA:
                continue  # bỏ person, motorcycle, bicycle... không thuộc schema
            schema_name = COCO_TO_SCHEMA[coco_name]
            x1, y1, x2, y2 = (int(v) for v in box.xyxy[0].tolist())
            conf = box.conf.item()
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 230), 2)
            cv2.putText(
                image,
                f"pred {schema_name} {conf:.2f}",
                (x1, max(24, y2 + 16)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 230),
                1,
            )
            pred_count += 1

        # Vẽ nhãn CP2 của bạn (xanh lá) nếu file nhãn đã có
        image, gt_count = draw_gt_boxes(image, LABELS_DIR / f"{img_path.stem}.txt")

        out_path = OUT_DIR / f"{img_path.stem}_preview.jpg"
        cv2.imwrite(str(out_path), image)
        print(
            f"{img_path.name}: model tìm {pred_count} box (đỏ), "
            f"nhãn CP2 của bạn có {gt_count} box (xanh lá) -> {out_path}"
        )

    print("\nGhi nhớ: prediction chỉ để tham khảo. Nhãn CP2 phải do bạn tự gán.")
    print("Legend: đỏ = prediction model, xanh lá = nhãn CP2 của bạn.")


if __name__ == "__main__":
    main()
