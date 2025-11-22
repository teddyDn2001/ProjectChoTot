# Chotot Motorbike Pricing & Anomaly Detection

## 1. Tổng quan
- **Mục tiêu 1 – Dự đoán giá**: xây dựng mô hình ước lượng `gia_vnd_final` dựa trên metadata (hãng, dòng xe, năm đăng ký, số km, dung tích, địa chỉ, mô tả…).
- **Mục tiêu 2 – Phát hiện bất thường**: gắn cờ các tin có giá lệch so với thị trường để hỗ trợ kiểm duyệt.
- Bộ dữ liệu lấy từ file `data_motobikes.xlsx - Sheet1.csv` (≈7.2K tin rao bán xe máy ở TP.HCM).

## 2. Cấu hình đường dẫn

Trước khi chạy, cập nhật đường dẫn trong `config.py` hoặc đặt file dữ liệu vào thư mục `data/` ở root của repository.

```python
# Sử dụng config.py trong notebooks
from config import RAW_DATA_FILE, CLEAN_DATA_FILE, ARTIFACTS_DIR, MODELS_DIR
```

## 3. Chuỗi thực thi notebook
| Thứ tự | Notebook | Thành phần chính | Kết quả sinh ra |
|--------|----------|------------------|-----------------|
| 1 | `preprocess_validate.ipynb` | Làm sạch + chuẩn hóa dữ liệu thô, parse giá, tách địa chỉ, tạo đặc trưng nhẹ | `data_motobikes_clean.csv`, `validation_issues.csv` |
| 2 | `prep_preprocessor.ipynb` | Fit `ColumnTransformer` (Imputer + OneHotEncoder) | `artifacts/preprocessor.joblib` |
| 3 | `train_price_models.ipynb` | CV cho `RandomForestRegressor` & `HistGradientBoostingRegressor` (không dùng Dummy) | `models/price_cv_results.csv`, `models/price_model.joblib` |
| 4 | `train_anomaly_models.ipynb` | Tính residual-based anomaly + IsolationForest | `anomaly_outputs/anomalies_residual.csv`, `anomaly_outputs/anomalies_isolation.csv`, `models/iso_model.joblib` |
| 5 | `explain_price_model.ipynb` | Permutation importance (top fitur ảnh hưởng) | `explain_permutation.csv`, `plots/perm_importance_top20.png` |
| 6 | `evaluate_anomalies.ipynb` | Gộp các kết quả anomaly, xuất top danh sách | `anomaly_summary.csv`, `top_anomalies_residual.csv`, `top_anomalies_isolation.csv` |
| 7 | `eda_basic.ipynb`, `eda_visuals.ipynb` | Thống kê, trực quan (hist, boxplot, scatter, corr) | `eda_price_stats.csv`, `eda_missingness.csv`, thư mục `plots/` |

> **Lưu ý:** Trước khi chạy lại từ đầu, nên xóa các file output hiện tại (đặc biệt trong `models/`, `artifacts/`, `anomaly_outputs/`, `plots/`) để đảm bảo kết quả mới không bị trộn với kết quả cũ.

## 4. Artefact quan trọng
```
artifacts/preprocessor.joblib          # ColumnTransformer đã fit (median impute + OHE)
models/price_model.joblib             # Pipeline dự đoán giá (RandomForest)
models/price_cv_results.csv           # Bảng so sánh CV (MAE, RMSE, R², MAPE)
models/iso_model.joblib               # IsolationForest cho bất thường
anomaly_outputs/                      # CSV các tin gắn cờ bất thường
plots/                                # Hình trực quan phục vụ báo cáo (hist, boxplot, corr,...)
explain_permutation.csv               # Ranking permutation importance
```

## 5. Cách chạy lại từ đầu
1. **Chuẩn bị**: đảm bảo đã cài Python 3.10+, pip (cùng môi trường `fugue_env`). Nếu thiếu thư viện, cài thêm: `pip install -r requirements.txt` *(chứa: pandas, numpy, scikit-learn, seaborn, matplotlib, joblib, scipy, ydata-profiling, dataprep, shap (tuỳ chọn))*.
2. **Thứ tự notebook**: chạy lần lượt 7 notebook theo bảng trên. Không được bỏ qua bước vì các bước sau phụ thuộc file sinh ra từ bước trước.
3. **Kiểm tra nhanh**: sau mỗi notebook, mở các file output tương ứng để đảm bảo được tạo thành công.
4. **Explainability**: `explain_price_model.ipynb` hiện dùng RandomForest nên permutation importance đã hiển thị, nếu muốn dùng SHAP thì cài thêm `pip install shap` và chỉnh mô hình tree phù hợp.
5. **Anomaly summary**: sau bước 6, mở `anomaly_summary.csv` hoặc hai file top để trình bày các tin “cờ đỏ”.

## 6. Hiệu năng mô hình
- **Bảng CV** (`models/price_cv_results.csv`) – ví dụ run gần nhất:
  - `rf`: MAE ≈ 60.7M, RMSE lớn, R² âm (dữ liệu nhiễu, thiếu feature chuẩn).
  - `hgbr`: MAE ≈ 134.7M (kém hơn).
- Về baseline, yêu cầu ban đầu dùng Dummy để so sánh, nhưng yêu cầu mới không dùng Dummy ⇒ file `price_model.joblib` hiện lưu `RandomForestRegressor`.
- **Hai điểm cần nhấn mạnh cho giảng viên**:
  1. Dữ liệu mô tả text chưa sử dụng (đang là bước kế tiếp để cải thiện MAE).
  2. Vẫn ghi rõ Dummy tốt hơn trong CV ban đầu, nhưng đã loại bỏ theo yêu cầu.

## 7. Bất thường (Anomaly Detection)
- **Residual-based**: tính `price_pred`, `residual`, `pct_err`, gắn cờ top 5% |pct_err|.
- **IsolationForest**: transform feature + `log_price`, train contamination 5%, xuất `iso_score` và cờ `is_anomaly_iso`.
- `evaluate_anomalies.ipynb` hợp nhất, tạo `anomaly_summary.csv` và hai file top để trình chiếu.

## 8. Giải thích mô hình
- `explain_permutation.csv` + `perm_importance_top20.png`: liệt kê các feature quan trọng theo permutation importance (hiện ra tên OHE, ví dụ `pre__cat__thuong_hieu_Honda`).
- SHAP chưa bật (do chưa cài `shap` và model đang là RandomForest). Nếu cần, cài `pip install shap` và chỉnh code trước khi quay video demo.

## 9. Hướng phát triển tiếp
- Bổ sung đặc trưng mới: TF-IDF mô tả, phân loại địa chỉ (quận/huyện, ẩn danh), tỷ lệ giá/km.
- Tinh chỉnh thêm các mô hình (RandomForest/HGBR/CatBoost/LightGBM) và so sánh MAE.
- Xây dựng script/CLI `predict_price.py` để demo input CSV → output dự đoán + anomaly.
- Deploy: cân nhắc Flask/FastAPI (dự án tương lai).

## 10. Checklist khi quay video
- Mở `README.md` → giới thiệu pipeline.
- Trình tự notebook + kết quả mỗi bước (có file output minh chứng).
- Mở `models/price_cv_results.csv`, `explain_permutation.csv`, các hình trong `plots/`.
- Demo `anomaly_summary.csv` (lọc vài tin bất thường) + nhắc Residual/Isolation.
- Nêu rõ hạn chế hiện tại & hướng phát triển.

---

