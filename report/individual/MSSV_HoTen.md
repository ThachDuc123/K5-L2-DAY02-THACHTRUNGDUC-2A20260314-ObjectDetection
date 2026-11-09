# Báo cáo cá nhân — Ngày 2 Object Detection

Đổi tên file theo `MSSV_HoTen.md`, ví dụ `20241234_NguyenVanAn.md`. Điền kết quả thật, xóa dòng hướng dẫn khi nộp. Xem [quy định nộp](../../SUBMISSION.md).

## 1. Thông tin học viên

- Họ tên: <!-- TODO: điền họ tên -->
- MSSV: <!-- TODO: điền MSSV -->
- Email: <!-- TODO: điền email -->
- Lớp: <!-- TODO: điền lớp (L2 / L2A / L2B) -->
- Link repo bài làm: <!-- TODO: link repo fork đúng chuẩn tên K5-L2-DAY02-HoVaTen-MSSV-ObjectDetection -->
- Link Colab đã chạy: <!-- TODO: dán link Colab sau khi chạy CP6 -->

## 2. Schema và mini guideline

Xem [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md). Ba ca mơ hồ đã quyết định:

1. **Xe rất xa, box nhỏ** (`drive_008`, `drive_028`, `drive_042`-`drive_044`): vẫn gán `car` vì còn nhận diện được lớp; schema không đặt ngưỡng kích thước tối thiểu.
2. **Xe cắt khung ở rìa ảnh, box cao/hẹp** (`drive_012`, `drive_033`): giữ box bám phần nhìn thấy, chạm rìa ảnh, không đoán phần ngoài.
3. **Van mơ hồ với bus/car** (`drive_008`, `drive_031`): phân biệt theo kích thước tương đối trong cảnh (nhỏ hơn bus rõ rệt, cao/to hơn car thường thì `van`); còn mơ hồ thì hỏi giảng viên.

## 3. Annotation và self-QC

- Số file nhãn train: 50 (tổng 646 box: car=539, bus=63, truck=26, van=18)
- Kết quả checker và lỗi đã xử lý: `python tools/check_yolo_labels.py` → **ĐẠT cấu trúc 50/50**, không có lỗi để sửa. Nhãn gán trên CVAT, export định dạng YOLO 1.1.
- Danh sách ít nhất 10 ảnh đã rà bằng mắt: <!-- TODO: xác nhận danh sách ảnh bạn đã mở rà trong outputs/label_qc/, ví dụ: drive_008, drive_009, drive_012, drive_013, drive_020, drive_022, drive_025, drive_029, drive_031, drive_033, drive_036, drive_045 -->
- Lỗi bỏ sót/box/class phát hiện khi rà và cách sửa: <!-- TODO: ghi kết quả rà; hai điểm đã đánh dấu cần kiểm: box cao/hẹp drive_012 (car) và drive_033 (bus) có phải xe cắt khung; 6 box nhỏ ở drive_008/028/042/043/044 còn nhận ra xe không -->
- Commit khóa nhãn ban đầu: <!-- TODO: dán mã commit sau khi push -->

## 4. Gold QC và rework

<!-- TODO: điền sau khi nhận gold_train_labels và chạy evaluate_annotations.py -->

| Chỉ số | Trước sửa | Sau sửa nếu có |
|---|---:|---:|
| TP | | |
| FP | | |
| FN | | |
| Precision | | |
| Recall | | |
| F1 | | |
| mean_iou_of_matches | | |
| passed | | |

Dẫn tới `outputs/annotation_evaluation.json` trong repo. Nếu rework, ghi ảnh, lỗi đã kiểm, quyết định sửa/giữ và lý do. Không suy nguyên nhân chỉ từ FP/FN. Không có rework thì ghi rõ.

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

- Đã có: CP1 (mini guideline), CP2 (50 nhãn YOLO), CP3 (checker đạt 50/50, đã tạo overlay 50 ảnh để rà).
- Còn thiếu: rà bằng mắt ≥10 ảnh (người làm xác nhận), CP4 (commit khóa nhãn), CP5 (chờ gold set, chạy evaluator), CP6 (Colab train/eval), đổi tên file báo cáo và điền thông tin cá nhân.
<!-- TODO: cập nhật sau mỗi bước hoàn thành -->

## 8. Công cụ AI và tài liệu tham khảo

- ZCode (trợ lý AI, mô hình GLM): đọc và tóm tắt tài liệu bài; viết script xem thử prediction (`tools/preview_predictions.py`) và script vẽ overlay để self-QC (`tools/qc_label_overlays.py`); chuyển nhãn export từ CVAT vào đúng cấu trúc repo; chạy checker và thống kê nhãn; soạn bản nháp GUIDELINE_MINI.md và báo cáo này.
- Phần tự kiểm tra: toàn bộ 646 box trong 50 ảnh do bản thân gán thủ công trên CVAT; các quyết định trong mini guideline rà lại theo nhãn thực tế đã gán; kết quả checker tự chạy lại bằng lệnh chuẩn của bài.
- Tài liệu ngoài repo: không sử dụng nguồn ngoài repo cho nhãn và kết quả.
