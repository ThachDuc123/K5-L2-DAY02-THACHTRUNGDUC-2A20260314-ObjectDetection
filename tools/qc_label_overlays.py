"""Vẽ nhãn YOLO của bạn lên ảnh để rà soát nội dung (self-QC CP3).

Cách dùng (chạy từ thư mục gốc repo):
    python tools/qc_label_overlays.py                # 10 ảnh ngẫu nhiên
    python tools/qc_label_overlays.py --image drive_003
    python tools/qc_label_overlays.py --all          # cả 50 ảnh

Ảnh overlay lưu ở outputs/label_qc/<ten_anh>.jpg.
Màu box theo class: car=xanh lá, truck=cam, bus=đỏ, van=xanh dương.
"""

import argparse
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "dataset" / "images" / "train"
LABELS_DIR = REPO_ROOT / "dataset" / "labels" / "train"
OUT_DIR = REPO_ROOT / "outputs" / "label_qc"

CLASS_NAMES = {0: "car", 1: "truck", 2: "bus", 3: "van"}
CLASS_COLORS = {
    0: (60, 200, 60),    # car - xanh lá (BGR)
    1: (30, 150, 255),   # truck - cam
    2: (60, 60, 230),    # bus - đỏ
    3: (230, 150, 60),   # van - xanh dương
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", default=None, help="rà soát một ảnh cụ thể, vd drive_003")
    parser.add_argument("--count", type=int, default=10, help="số ảnh ngẫu nhiên (mặc định 10)")
    parser.add_argument("--all", action="store_true", help="vẽ overlay cho cả 50 ảnh")
    args = parser.parse_args()

    import cv2

    images = sorted(IMAGES_DIR.glob("*.jpg"))
    if not images:
        sys.exit(f"Không tìm thấy ảnh trong {IMAGES_DIR}")
    if args.image:
        images = [p for p in images if p.stem == args.image]
        if not images:
            sys.exit(f"Không tìm thấy ảnh {args.image}.jpg")
    elif not args.all:
        random.seed()  # mẫu ngẫu nhiên mỗi lần chạy
        images = random.sample(images, min(args.count, len(images)))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = []
    for img_path in images:
        image = cv2.imread(str(img_path))
        if image is None:
            print(f"Bỏ qua (đọc được không?): {img_path.name}")
            continue
        h, w = image.shape[:2]
        label_path = LABELS_DIR / f"{img_path.stem}.txt"
        boxes = []
        if label_path.exists():
            for line in label_path.read_text().splitlines():
                parts = line.split()
                if len(parts) != 5:
                    continue
                boxes.append([float(p) for p in parts])
        for cls, xc, yc, bw, bh in boxes:
            x1, y1 = int((xc - bw / 2) * w), int((yc - bh / 2) * h)
            x2, y2 = int((xc + bw / 2) * w), int((yc + bh / 2) * h)
            color = CLASS_COLORS.get(int(cls), (255, 255, 255))
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                image,
                CLASS_NAMES.get(int(cls), str(cls)),
                (x1, max(14, y1 - 5)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                color,
                1,
            )
        out_path = OUT_DIR / f"{img_path.stem}.jpg"
        cv2.imwrite(str(out_path), image)
        counts = {CLASS_NAMES[int(c)]: 0 for c in set(b[0] for b in boxes)}
        for cls, *_ in boxes:
            counts[CLASS_NAMES[int(cls)]] += 1
        summary.append((img_path.name, len(boxes), counts, str(out_path)))

    print(f"Đã vẽ {len(summary)} ảnh overlay vào {OUT_DIR}:\n")
    for name, n, counts, path in summary:
        detail = ", ".join(f"{k}={v}" for k, v in counts.items()) or "không có box"
        print(f"  {name}: {n} box ({detail})")


if __name__ == "__main__":
    main()
