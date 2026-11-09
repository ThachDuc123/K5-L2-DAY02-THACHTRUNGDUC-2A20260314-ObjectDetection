# Mini guideline — bài làm cá nhân

> Điền nội dung này trước khi bắt đầu gán nhãn. Giữ lại các quyết định sau khi self-QC.

## Định nghĩa lớp

| Lớp | Định nghĩa của bạn | Ví dụ/điểm phân biệt |
| --- | --- | --- |
| `car` | Xe con 4 bánh chở người: sedan, hatchback, SUV, taxi, xe bán tải | Thân ngắn, khoang lái + khoang hành khách; bán tải có thùng hàng nhỏ nhưng vẫn là `car` |
| `truck` | Xe tải chở hàng có thùng/khòa hàng riêng, xe đầu kéo | Thân dài, khoang hàng lớn tách biệt cabin; đầu kéo có bánh xe lớn + chân kết nối |
| `bus` | Xe buýt, minibus chở khách, thân liền khối cao lớn | Dài và cao hơn van, nhiều hàng ghế/số cửa sổ dọc thân, hàng khách |
| `van` | Xe van/minivan chở hàng hoặc chở người, thân liền khối nhỏ | Nhỏ hơn bus (thấp, ngắn), to hơn car thông thường; mũi ngắn, khoang liền |
| Mô tô/xe máy, xe đạp, người đi bộ | Không thuộc schema — không gán | Chỉ 4 lớp car/truck/bus/van được gán nhãn |

## Quy tắc chung

- Box bám sát vật thể nghĩa là: bốn cạnh box chạm đúng rìa phần thân xe nhìn thấy được; không lấy thêm mặt đường, bầu trời, xe bên cạnh hay khoảng trống.
- Vật thể bị che khuất: vẫn vẽ box quanh phần nhìn thấy nếu còn nhận diện được lớp; không đoán phần bị che.
- Vật thể bị cắt bởi rìa ảnh: box chạm đúng rìa ảnh, không đoán phần nằm ngoài.
- Vật thể rất nhỏ/mơ hồ: nếu còn nhìn ra rõ là xe và xác định được lớp thì vẫn gán; không xác định được lớp chắc chắn thì không gán và ghi vào bảng dưới.

## Ghi lại quyết định cho ít nhất ba ca mơ hồ

| Ảnh | Tình huống | Quyết định cuối | Lý do theo schema |
| --- | --- | --- | --- |
| `drive_008`, `drive_028`, `drive_042`-`drive_044` | Xe con ở xa, box rất nhỏ (~0.06-0.09% diện tích ảnh, khoảng 15-30 px) | Vẫn gán `car` | Còn nhìn rõ dạng xe con, nhận diện được lớp; schema không đặt ngưỡng kích thước tối thiểu |
| `drive_012`, `drive_033` | Box cao/hẹp bất thường (h/w ≈ 4-5): xe chỉ ló một phần đầu/đuôi ở rìa ảnh | Giữ box, chạm rìa ảnh theo phần nhìn thấy | Quy tắc cắt khung: box bám phần nhìn thấy, không đoán phần ngoài ảnh |
| `drive_008`, `drive_031` | Xe thân liền khối nhỏ khó phân biệt `van` / `bus` / `car` | Gán theo kích thước tương đối trong cảnh: nhỏ hơn bus rõ rệt và cao/to hơn car thường thì `van` | Schema: van là minivan chở hàng/người; bus là xe buýt/minibus chở khách lớn; nếu còn mơ hồ sẽ hỏi giảng viên |
