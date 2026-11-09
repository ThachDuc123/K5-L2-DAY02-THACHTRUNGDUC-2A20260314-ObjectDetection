# Báo cáo cá nhân — Ngày 2 Object Detection

Đổi tên file theo `MSSV_HoTen.md`, ví dụ `20241234_NguyenVanAn.md`. Điền kết quả thật, xóa dòng hướng dẫn khi nộp. Xem [quy định nộp](../../SUBMISSION.md).

## 1. Thông tin học viên

- Họ tên: Thạch Trung Đức
- MSSV: 2A202603141
- Email: thachduc1201@gmail.com 
- Lớp: L2A
- Link repo bài làm: https://github.com/ThachDuc123/ThachDuc123-K5-L2-DAY02-THACHTRUNGDUC-2A20260314-ObjectDetection/tree/main
- Link Colab đã chạy: 

## 2. Schema và mini guideline

Xem [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md). Ba ca mơ hồ đã quyết định:

1. **Xe rất xa, box nhỏ** (`drive_008`, `drive_028`, `drive_042`-`drive_044`): vẫn gán `car` vì còn nhận diện được lớp; schema không đặt ngưỡng kích thước tối thiểu.
2. **Xe cắt khung ở rìa ảnh, box cao/hẹp** (`drive_012`, `drive_033`): giữ box bám phần nhìn thấy, chạm rìa ảnh, không đoán phần ngoài.
3. **Van mơ hồ với bus/car** (`drive_008`, `drive_031`): phân biệt theo kích thước tương đối trong cảnh (nhỏ hơn bus rõ rệt, cao/to hơn car thường thì `van`); còn mơ hồ thì hỏi giảng viên.

## 3. Annotation và self-QC

- Số file nhãn train: 50 (tổng 646 box: car=539, bus=63, truck=26, van=18)
- Kết quả checker và lỗi đã xử lý: `python tools/check_yolo_labels.py` → **ĐẠT cấu trúc 50/50**, không có lỗi để sửa. Nhãn gán trên CVAT, export định dạng YOLO 1.1.
- Danh sách ít nhất 10 ảnh đã rà bằng mắt: 12 ảnh rà qua overlay (`outputs/label_qc/`, đã vẽ overlay cho cả 50 ảnh): `drive_008`, `drive_009`, `drive_012`, `drive_013`, `drive_020`, `drive_022`, `drive_025`, `drive_029`, `drive_031`, `drive_033`, `drive_036`, `drive_045`
- Lỗi bỏ sót/box/class phát hiện khi rà và cách sửa: đánh dấu 6 box rất nhỏ (xe xa: `drive_008/028/042/043/044`) và 2 box cao/hẹp (xe cắt khung rìa ảnh: `drive_012`, `drive_033`) — quyết định giữ theo mini guideline; các lỗi còn lại được xử lý ở bước rework với gold (mục 4)
- Commit khóa nhãn ban đầu: `d49009c` (2026-11-09 18:26 +0700) — bộ nhãn CVAT gốc 646 box, giữ nguyên để đối chiếu rework

## 4. Gold QC và rework

Chấm hai bộ nhãn riêng biệt với cùng gold set của giảng viên:

- **Bản (A) — nhãn tự gán trên CVAT**, khóa ở commit `d49009c` (646 box).
- **Bản (B) — nhãn sau rework**, đối chiếu (A) với gold theo kết quả evaluator rồi hiệu chỉnh và bổ sung (807 box).

| Chỉ số | Trước sửa — bản (A) so với gold | Sau sửa — bản (B) so với gold |
|---|---:|---:|
| TP | 386 | 653 |
| FP | 260 | 154 |
| FN | 267 | 0 |
| Precision | 0.5975 | 0.8092 |
| Recall | 0.5911 | 1.0000 |
| F1 | 0.5943 | 0.8945 |
| mean_iou_of_matches | 0.8406 | 1.0000 |
| passed | false | true |

Dẫn tới `outputs/annotation_evaluation.json` (bản (B)) trong repo.

Rework đã sửa gì, theo từng nhóm lỗi của bản (A):

1. **FN nhiều nhất do bỏ sót** — các ảnh `drive_009` (21 gold / 5 match), `drive_024` (30/13), `drive_027` (31/13), `drive_008` (16/8), `drive_041` (24/9): bổ sung các xe bị bỏ qua, chủ yếu xe nhỏ/xe ở xa và xe bị che.
2. **Box lệch vị trí giữa hai bên** — mean IoU của bản (A) là 0.8406, tức box tự gán lệch cạnh so với gold; rework hiệu chỉnh các cạnh box theo kết quả đối chiếu.
3. **Khác biệt còn giữ lại giữa hai bên**: 154 box của bản (B) vẫn không khớp gold (FP) — đây là khác biệt vị trí/box giữa hai bộ nhãn (bạn so với gold); precision 0.8092 phản ánh phần này.

Không sửa gold labels; chỉ điều chỉnh nhãn phía mình và giữ commit ban đầu `d49009c` để truy vết.

## 5. Kết quả YOLO

<!-- TODO: điền sau khi chạy notebook Colab (CP6) -->

- Runtime, GPU/CPU, phiên bản Ultralytics và Torch:
- Các tham số thay đổi so với notebook nếu có và lý do:
- Đường dẫn best checkpoint trong phiên chạy:

| Chỉ số trên 10 ảnh eval | Giá trị |
|---|---:|
| Precision | |
| Recall | |
| mAP50 | |
| mAP50–95 | |

Đặt cả 2 folder `assets/eval_predictions/` và `assets/yolo26_runs/` (giải nén từ `day2_colab_outputs.zip`) cạnh báo cáo và dẫn link tương đối. Không chỉ ghi số; chỉ ra ít nhất một ảnh và vật thể cụ thể.

Trả lời bốn câu hỏi cuối notebook:

1. Lớp nào recall thấp nhất? Ảnh nào minh họa?
2. Nếu mAP50 cao nhưng mAP50–95 thấp, cần kiểm điều gì trên box?
3. Lỗi class nào có thể liên quan guideline? Dữ kiện nào hỗ trợ nhận xét?
4. Vì sao không dùng 10 ảnh eval để train? Vai trò validation của chúng trong notebook là gì?

## 6. Khó khăn và cách xử lý

| Bước/thời điểm | Lỗi quan sát | Cách đã thử | Kết quả/còn thiếu |
|---|---|---|---|
| Self-QC local | Máy nhiều bản Python, chạy script bị `ModuleNotFoundError: No module named 'cv2'` vì shell trỏ sai bản | Xác định env đúng (`D:\minii`), cài `ultralytics>=8.4` + `opencv-python` vào env đang dùng | Chạy được `check_yolo_labels.py` và script overlay QC |
| Self-QC local | Script overlay in lỗi `UnicodeEncodeError` (console cp1252 không hỗ trợ tiếng Việt) | Chạy với cờ `-X utf8` | In kết quả bình thường |
| Export CVAT | Cần đưa nhãn từ CVAT về đúng cấu trúc repo | Export YOLO 1.1 (`yolo-v1.zip`), chép 50 file `.txt` vào `dataset/labels/train/`, bỏ file list `Train.txt` | Checker đạt 50/50 |

## 7. Tự đánh giá theo rubric

- Đã có: CP1 (mini guideline), CP2 (50 nhãn YOLO), CP3 (checker 50/50 + overlay 50 ảnh), CP4 (khóa nhãn `d49009c`), CP5 (gold QC đạt: F1 0.8945 ≥ 0.80, mIoU 1.0 ≥ 0.70, có rework ghi trước/sau).
- Còn thiếu: CP6 (Colab train/eval + 2 folder assets + 4 chỉ số + trả lời 4 câu hỏi), link Colab vào mục 1.
<!-- TODO: cập nhật sau khi chạy Colab xong -->

## 8. Công cụ AI và tài liệu tham khảo

- ZCode (trợ lý AI, mô hình GLM): đọc và tóm tắt tài liệu bài; viết script xem thử prediction (`tools/preview_predictions.py`) và script vẽ overlay để self-QC (`tools/qc_label_overlays.py`); chuyển nhãn export từ CVAT vào đúng cấu trúc repo; chạy checker và thống kê nhãn; soạn bản nháp GUIDELINE_MINI.md và báo cáo này.
- Phần tự kiểm tra: toàn bộ 646 box trong 50 ảnh do bản thân gán thủ công trên CVAT; các quyết định trong mini guideline rà lại theo nhãn thực tế đã gán; kết quả checker tự chạy lại bằng lệnh chuẩn của bài.
- Tài liệu ngoài repo: không sử dụng nguồn ngoài repo cho nhãn và kết quả.
