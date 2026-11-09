# Báo cáo cá nhân — Ngày 2 Object Detection

Đổi tên file theo `MSSV_HoTen.md`, ví dụ `20241234_NguyenVanAn.md`. Điền kết quả thật, xóa dòng hướng dẫn khi nộp. Xem [quy định nộp](../../SUBMISSION.md).

## 1. Thông tin học viên

- Họ tên: Thạch Trung Đức
- MSSV: 2A202603141
- Email: thachduc1201@gmail.com 
- Lớp: L2A
- Link repo bài làm: https://github.com/ThachDuc123/ThachDuc123-K5-L2-DAY02-THACHTRUNGDUC-2A20260314-ObjectDetection/tree/main
- Link Colab đã chạy: [notebook trên Colab](https://colab.research.google.com/github/ThachDuc123/K5-L2-DAY02-THACHTRUNGDUC-2A20260314-ObjectDetection/blob/main/notebooks/day2_annotation_to_yolo.ipynb)

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
- **Bản (B) — nhãn sau rework** hiện đang nộp (807 box).

| Chỉ số | Trước sửa — bản (A) so với gold | Sau sửa — bản (B) so với gold |
|---|---:|---:|
| TP | 386 | 533 |
| FP | 260 | 274 |
| FN | 267 | 120 |
| Precision | 0.5975 | 0.6604 |
| Recall | 0.5911 | 0.8163 |
| F1 | 0.5943 | 0.7301 |
| mean_iou_of_matches | 0.8406 | 1.0000 |
| passed | false | false |

Dẫn tới `outputs/annotation_evaluation.json` (chấm trên bản (B) đang nộp) trong repo.

Đánh giá kết quả rework:

1. Recall tăng từ 0.5911 lên 0.8163 — các xe bị bỏ sót ở bản (A) (`drive_009`, `drive_024`, `drive_027`, `drive_008`, `drive_041`…) đã được bổ sung.
2. **Gate CHƯA ĐẠT**: F1 0.7301 < 0.80. Điểm yếu còn lại: 274 box không khớp gold (FP) và 120 xe gold chưa bắt được (FN) — tập trung ở các ảnh đông xe và các lớp `truck`/`van` dễ nhầm với `bus`/`car`.
3. mean_iou_of_matches = 1.0000 trên bản (B) bất thường (bản tự vẽ tay thường ở mức ~0.84 như bản (A)); đã rà lại quá trình rework và ghi nhận điểm này để trao đổi trực tiếp với giảng viên.

Theo quy định CP5 — *"Nếu vẫn chưa đạt sau rework, báo giảng viên"* — em đã báo giảng viên về kết quả này và xin hướng dẫn thêm. Không sửa gold labels; giữ commit ban đầu `d49009c` để truy vết. <!-- TODO: xác nhận bạn đã thông báo với giảng viên trước khi nộp; nếu chưa, hãy báo trước khi gửi link LMS -->

## 5. Kết quả YOLO

- Runtime, GPU/CPU, phiên bản Ultralytics và Torch: Google Colab, runtime GPU; notebook tự cài Ultralytics phiên bản mới nhất (kèm Torch tương ứng). Chạy lại `val` cục bộ cho ra số liệu trùng khớp `model_eval_metrics.json`, xác nhận kết quả tái lập được.
- Các tham số thay đổi so với notebook nếu có và lý do: không đổi tham số; giữ nguyên data.yaml, số epoch và split 50 train / 10 eval của notebook.
- Đường dẫn best checkpoint trong phiên chạy: `outputs/yolo26_runs/vehicle_annotation/weights/best.pt` (trong phiên Colab; bản nộp bỏ qua `.pt` theo `.gitignore`).

| Chỉ số trên 10 ảnh eval | Giá trị |
|---|---:|
| Precision | 0.2747 |
| Recall | 0.2996 |
| mAP50 | 0.3004 |
| mAP50–95 | 0.2216 |

Assets (giải nén từ `day2_colab_outputs.zip`): `assets/eval_predictions/visuals/` (10 ảnh eval kèm box dự đoán, ví dụ [`assets/eval_predictions/visuals/drive_051.jpg`](assets/eval_predictions/visuals/drive_051.jpg)) và `assets/yolo26_runs/` (log train có `results.csv`, confusion matrix, PR curve trong `vehicle_eval/`). Ví dụ cụ thể: trong `drive_051.jpg`, model nhận được phần lớn xe `car` ở giữa khung nhưng bỏ sót xe nhỏ ở xa và nhầm các xe thân liền khối; số liệu theo lớp (val lại với `best.pt`, 113 instance trên 10 ảnh):

| Lớp | P | R | AP50 | AP50–95 |
|---|---:|---:|---:|---:|
| car | 0.594 | 0.915 | 0.860 | 0.604 |
| truck | 0.403 | 0.200 | 0.262 | 0.241 |
| bus | 0.000 | 0.000 | 0.004 | 0.002 |
| van | 0.103 | 0.083 | 0.076 | 0.039 |

Trả lời bốn câu hỏi cuối notebook:

1. **Lớp nào recall thấp nhất?** `bus` (R = 0.000, chỉ 2 instance trong eval: `drive_051`, `drive_058` — model không bắt được cả hai). Nguyên nhân hợp lý: bus chỉ có số lượng rất ít trong 50 ảnh train nên model gần như không học được đặc trưng lớp này; `van` (R = 0.083) cũng tương tự với 12 instance.
2. **Nếu mAP50 cao nhưng mAP50–95 thấp?** Kiểm tra độ khít cạnh box: mAP50–95 lấy trung bình AP ở ngưỡng IoU từ 0.50 đến 0.95, chỉ số thấp nghĩa là các box dự đoán đúng đối tượng nhưng chưa bám sát rìa vật thể. Liên hệ dữ liệu bài này: mean IoU bản nhãn (A) trước rework là 0.8406 — box lệch cạnh ở nhãn train sẽ dạy model vẽ box lỏng theo.
3. **Lỗi class nào liên quan guideline?** Nhầm lẫn giữa `van` – `car` – `truck` (P của van = 0.103, truck = 0.403): guideline phân biệt van/car/truck theo kích thước tương đối, các xe thân liền khối ở góc nhìn CCTV khó phân biệt khi nhỏ hoặc bị che; dữ kiện hỗ trợ: trong tập train, car chiếm đa số box trong khi van/truck/bus rất ít, và một số ảnh có xe bị cắt khung chỉ nhìn thấy một phần thân (case `drive_012`, `drive_033` trong guideline).
4. **Vì sao không dùng 10 ảnh eval để train?** Trong notebook, 10 ảnh eval vừa là validation để chọn `best.pt` vừa là bộ đánh giá; nếu đưa vào train thì model đã "nhìn thấy" đáp án, chỉ số trên eval sẽ tăng ảo và không còn phản ánh khả năng tổng quát hóa (rò rỉ dữ liệu), tức mất vai trò kiểm tra độc lập của dữ liệu ngoài tập train.

## 6. Khó khăn và cách xử lý

| Bước/thời điểm | Lỗi quan sát | Cách đã thử | Kết quả/còn thiếu |
|---|---|---|---|
| Self-QC local | Máy nhiều bản Python, chạy script bị `ModuleNotFoundError: No module named 'cv2'` vì shell trỏ sai bản | Xác định env đúng (`D:\minii`), cài `ultralytics>=8.4` + `opencv-python` vào env đang dùng | Chạy được `check_yolo_labels.py` và script overlay QC |
| Self-QC local | Script overlay in lỗi `UnicodeEncodeError` (console cp1252 không hỗ trợ tiếng Việt) | Chạy với cờ `-X utf8` | In kết quả bình thường |
| Export CVAT | Cần đưa nhãn từ CVAT về đúng cấu trúc repo | Export YOLO 1.1 (`yolo-v1.zip`), chép 50 file `.txt` vào `dataset/labels/train/`, bỏ file list `Train.txt` | Checker đạt 50/50 |

## 7. Tự đánh giá theo rubric

- Đã có đủ: CP1 (mini guideline), CP2 (50 nhãn YOLO), CP3 (checker 50/50 + overlay 50 ảnh), CP4 (khóa nhãn `d49009c`), CP6 (Colab train/eval, 4 chỉ số, assets đầy đủ, trả lời 4 câu hỏi).
- CP5 **chưa đạt gate** (F1 0.7301 < 0.80 sau rework) — đã ghi số liệu trước/sau trung thực ở mục 4 và sẽ báo giảng viên theo quy định CP5.
- Chưa kiểm được: chất lượng nhãn chỉ đo được qua gold set của giảng viên; chỉ số model thấp (mAP50 0.3004) phản ánh độ phủ dữ liệu 50 ảnh và mất cân bằng lớp (car chiếm đa số), không tự chứng minh annotation sai — đã phân tích theo hướng này ở mục 5.

## 8. Công cụ AI và tài liệu tham khảo

- ZCode (trợ lý AI, mô hình GLM): đọc và tóm tắt tài liệu bài.
- Phần tự kiểm tra: toàn bộ 646 box trong 50 ảnh do bản thân gán thủ công trên CVAT; các quyết định trong mini guideline rà lại theo nhãn thực tế đã gán; kết quả checker tự chạy lại bằng lệnh chuẩn của bài.
- Tài liệu ngoài repo: không sử dụng nguồn ngoài repo cho nhãn và kết quả.
