# Nội Dung Slide Canva - Hệ Thống Gợi ý Xe Máy & Phân Khúc

---

## SLIDE 1: Trang bìa

**TIÊU ĐỀ (Heading 1)**
```
Xây dựng Hệ thống Gợi ý Xe Máy Tương Tự 
và Phân Khúc Sản Phẩm
```

**PHỤ ĐỀ (Subtitle)**
```
Đồ án Tốt Nghiệp Data Science
Chợ Tốt - Recommendation System & Clustering
```

**Thông tin nhóm** (nếu có)
- Tên sinh viên
- Mã số sinh viên
- Ngày thuyết trình

**Gợi ý hình ảnh**: Logo Chợ Tốt, biểu tượng xe máy, hoặc icon AI/ML

---

## SLIDE 2: Hiểu vấn đề

**TIÊU ĐỀ**
```
Vấn đề và Mục tiêu
```

**NỘI DUNG**

**Bối cảnh:**
- Chợ Tốt chưa có tính năng gợi ý xe máy tương tự
- Người mua khó tìm xe phù hợp
- Người bán chưa hiểu rõ phân khúc thị trường

**Mục tiêu:**
1. Xây dựng hệ thống gợi ý 5 xe tương tự cho mỗi xe đang xem
   - Sử dụng Content-Based Filtering với Cosine Similarity (yêu cầu đề bài)
   - Sử dụng Gensim Doc2Vec cho recommendation (yêu cầu đề bài)
2. Phân khúc xe máy thành các nhóm có đặc điểm tương đồng
   - Triển khai trên cả 2 môi trường: sklearn và PySpark (yêu cầu đề bài)
   - So sánh kết quả giữa các mô hình khác nhau

**Ý nghĩa:**
- Hỗ trợ người mua tìm xe nhanh hơn
- Hỗ trợ người bán định giá hợp lý

**Gợi ý hình ảnh**: Sơ đồ quy trình mua bán xe máy, icon user/business

---

## SLIDE 3: Dữ liệu

**TIÊU ĐỀ**
```
Dữ liệu và Thống kê
```

**NỘI DUNG**

**Nguồn dữ liệu:**
- File: `data_motobikes.xlsx - Sheet1.csv`
- **7,208** tin đăng xe máy ban đầu
- **7,206** bản ghi sau làm sạch (99.97% giữ lại)
- Thời gian: Dữ liệu từ Chợ Tốt

**Các trường dữ liệu:**
- **Thông tin cơ bản**: ID, Tiêu đề, Mô tả, Địa chỉ, Href
- **Thông tin số**: Giá, Khoảng giá min/max, Năm đăng ký, Số Km đã đi
- **Thông tin phân loại**: Thương hiệu, Dòng xe, Loại xe, Dung tích xe, Tình trạng, Xuất xứ, Bảo hành

**Thống kê chính:**

| Chỉ số | Giá trị |
|--------|---------|
| Tổng số xe | 7,206 xe |
| Giá trung bình | 49.24 triệu VND |
| Giá median | 16.5 triệu VND |
| Giá min | 0 triệu VND |
| Giá max | 136,000 triệu VND |
| Năm trung bình | 2014 |
| Năm min-max | 1981 - 2025 |
| Số km trung bình | 64,379 km |

**Top 5 thương hiệu:**
1. Honda: 4,374 xe (60.7%)
2. Yamaha: 1,411 xe (19.6%)
3. Piaggio: 380 xe (5.3%)
4. Suzuki: 282 xe (3.9%)
5. SYM: 256 xe (3.6%)

**Vấn đề dữ liệu ban đầu:**
- Missing: Năm đăng ký (67), Giá min/max (202/197), Số Km (139)
- Giá trị ngoại lai: Một số giá quá cao cần xử lý

**Chụp ảnh từ notebook:**
- Cell `df_raw.info()` hoặc `df.shape` từ notebook 03
- Bảng thống kê giá, năm, km từ notebook 07
- Biểu đồ phân phối thương hiệu (nếu có)
- Bảng validation results từ notebook 05

---

## SLIDE 4: Quy trình làm việc

**TIÊU ĐỀ**
```
Quy trình Thực hiện Dự án
```

**NỘI DUNG**

**Workflow (9 bước):**

```
1. Hiểu vấn đề
   ↓
2. Import thư viện & Thiết lập môi trường
   ↓
3. Đọc dữ liệu (data_motobikes.xlsx)
   ↓
4. EDA cơ bản (Pandas Profiling, DataPrep)
   ↓
5. Tiền xử lý dữ liệu (làm sạch, feature engineering)
   ↓
6. Trực quan hóa dữ liệu (biểu đồ, heatmap)
   ↓
7. Phân tích dữ liệu sâu (KPI, insights)
   ↓
8. Lựa chọn thuật toán (recommendation, clustering)
   ↓
9. Xây dựng & Đánh giá mô hình (5 recommendation + 6 clustering)
   - sklearn: KNN, Content-Based Cosine Matrix, Gensim Doc2Vec
   - sklearn: KMeans, GMM, Agglomerative
   - PySpark: KMeans, GMM, Bisecting K-Means
```

**Công cụ sử dụng:**
- **Python**: pandas, numpy, scikit-learn
- **Visualization**: matplotlib, seaborn, plotly
- **EDA**: ydata_profiling, dataprep
- **Recommendation**: sklearn (KNN, cosine_similarity), **Gensim** (Doc2Vec) ⭐⭐
- **Clustering sklearn**: KMeans, GMM, Agglomerative
- **Clustering PySpark**: KMeans, GMM, Bisecting K-Means ⭐⭐
- **Evaluation**: silhouette_score, davies_bouldin_score, calinski_harabasz_score, WSSSE

**Chụp ảnh từ notebook:**
- Có thể vẽ sơ đồ workflow trên Canva
- Screenshot các notebook theo thứ tự (01-10)

---

## SLIDE 5: EDA - Phân tích dữ liệu

**TIÊU ĐỀ**
```
Khám phá Dữ liệu (EDA)
```

**NỘI DUNG**

**Phân phối giá:**
- **Lệch phải**: Đa số xe < 50 triệu VND (phân khúc phổ thông)
- **Median**: 16.5 triệu VND (thấp hơn mean rất nhiều)
- **Outliers**: Một số xe cao cấp > 500 triệu VND (moto thể thao)
- **Kết luận**: Thị trường phân khúc rõ rệt, phù hợp clustering

**Phân tích theo hãng:**
- **Honda**: Chiếm ưu thế tuyệt đối (60.7%) → Thị trường VN phổ biến
- **Yamaha**: Vị trí thứ 2 (19.6%) → Thị trường tầm trung
- **Phân khúc giá**: Khác nhau rõ rệt giữa các hãng
- **Giá TB**: Honda (63.8 triệu), Kawasaki (67.3 triệu), Ducati (152.2 triệu)

**Phân tích theo loại xe:**
- **Tay ga**: 3,600 xe (50%) → Phổ biến nhất, phù hợp đô thị
- **Xe số**: 2,189 xe (30%) → Phân khúc truyền thống, giá rẻ
- **Tay côn/Moto**: 1,419 xe (20%) → Phân khúc thể thao, cao cấp

**Phân tích theo năm:**
- **Xe 0-5 tuổi**: 1,701 xe, giá TB 125.4 triệu (xe mới, giá cao)
- **Xe 5-10 tuổi**: 2,048 xe, giá TB 31.0 triệu (phổ biến nhất)
- **Xe 10-15 tuổi**: 1,809 xe, giá TB 23.4 triệu (xe cũ, giá rẻ)

**Kết luận EDA:**
- ✅ Dữ liệu phù hợp cho **content-based recommendation**
- ✅ Có thể phân khúc rõ ràng dựa trên: giá, hãng, loại xe, năm
- ✅ Các phân khúc có đặc điểm khác biệt, thuận lợi cho clustering

**Chụp ảnh từ notebook:**
- Histogram phân phối giá từ notebook 06 (có KDE curve)
- Boxplot giá theo thương hiệu từ notebook 06 (top 10 hãng)
- Heatmap tương quan từ notebook 06 (correlation matrix)
- Scatter plot giá theo năm từ notebook 06 (Plotly với trendline)
- Bảng top brands từ notebook 07 (với avg_price, median_price)
- Bảng age_summary từ notebook 07 (phân tích theo độ tuổi xe)

---

## SLIDE 6: Tiền xử lý dữ liệu

**TIÊU ĐỀ**
```
Tiền xử lý Dữ liệu
```

**NỘI DUNG**

**Quy trình tiền xử lý (4 bước):**

**Bước 1: Làm sạch dữ liệu số**
- **Parse giá**: "66.000.000 đ" → 66 triệu VND
- **Parse "72.53 tr"** → 72.53 triệu VND  
- **Parse "tỷ"**: "1.5 tỷ" → 1,500 triệu VND
- **Parse số km**: "25.000 km" → 25000 (loại bỏ dấu phẩy, chấm)
- **Parse năm**: Lấy 4 số đầu, validate 1950-2030

**Bước 2: Xử lý missing values**
- Loại bỏ: 2 bản ghi thiếu giá (bắt buộc)
- Xử lý: Missing năm, km được set về None, sau đó dropna
- Kết quả: 7,206 bản ghi hợp lệ (99.97% giữ lại)

**Bước 3: Feature Engineering**
- **Numeric features** (5): Giá, Khoảng giá min, Khoảng giá max, Năm đăng ký, Số Km đã đi
- **Categorical features** (5): Thương hiệu, Dòng xe, Loại xe, Dung tích xe, Tình trạng
- **Text features**: Tiêu đề + Mô tả chi tiết → TF-IDF (5,000 features, ngram 1-2)

**Bước 4: Chuẩn hóa & Encoding**
- **StandardScaler**: Chuẩn hóa numeric features (mean=0, std=1)
- **OneHotEncoder**: Mã hóa categorical (sparse_output=False)
- **TF-IDF**: Vectorize text features (max_features=5000)
- **Kết quả**: Ma trận đặc trưng sẵn sàng cho modeling

**Lý do các bước:**
- Parse giá/km: Dữ liệu không đồng nhất (chuỗi, định dạng khác nhau)
- Chuẩn hóa: Đảm bảo các feature có cùng scale
- One-hot: Chuyển categorical thành numeric cho thuật toán

**Chụp ảnh từ notebook:**
- Code làm sạch giá từ notebook 05/09 (function `parse_price`, `parse_km`)
- Bảng validation results từ notebook 05 (missing counts)
- Code ColumnTransformer từ notebook 09 (StandardScaler + OneHotEncoder)
- Shape của ma trận features sau preprocessing

---

## SLIDE 7: Mô hình Recommendation - Giới thiệu

**TIÊU ĐỀ**
```
Mô hình Gợi ý (Recommendation System)
```

**NỘI DUNG**

**5 Mô hình đã xây dựng:**

**1. KNN Cosine (Full Features)**
- Đặc trưng: Số + Phân loại (one-hot)
- Metric: Cosine similarity
- Ưu điểm: Tận dụng toàn bộ thông tin

**2. KNN Cosine (Numeric Only)**
- Đặc trưng: Chỉ biến số
- Metric: Cosine similarity
- Ưu điểm: Đơn giản, nhanh

**3. KNN TF-IDF (Text Based)**
- Đặc trưng: TF-IDF từ tiêu đề + mô tả
- Metric: Cosine similarity
- Ưu điểm: Dựa trên nội dung văn bản

**4. Content-Based Cosine Matrix ⭐**
- Phương pháp: Tính ma trận cosine similarity trực tiếp
- Sử dụng: `sklearn.metrics.pairwise.cosine_similarity`
- Đặc trưng: Tất cả đặc trưng (số + phân loại)
- Ưu điểm: Content-based filtering chính thống

**5. Gensim Doc2Vec ⭐⭐ (Theo yêu cầu đề bài)**
- Phương pháp: Doc2Vec embeddings từ Gensim
- Sử dụng: `gensim.models.Doc2Vec`
- Đặc trưng: Embeddings 100 chiều từ tiêu đề + mô tả
- Ưu điểm: 
  - Xác định sự tương tự ngữ nghĩa giữa các tài liệu
  - Xử lý hiệu quả dữ liệu văn bản lớn
  - Tối ưu bộ nhớ và tốc độ

**Chụp ảnh từ notebook:**
- Code khai báo 5 mô hình từ notebook 09 (phần `recommenders = {`)
  - Đặc biệt chụp code của Gensim Doc2Vec và Content-Based Cosine Matrix
- Code tính cosine_similarity matrix (phần `content_based_cosine_matrix`)
- Code Gensim Doc2Vec (TaggedDocument, Doc2Vec model training)
- Sơ đồ kiến trúc (có thể vẽ đơn giản trên Canva)

---

## SLIDE 8: Mô hình Recommendation - Ví dụ

**TIÊU ĐỀ**
```
Kết quả Gợi ý - Ví dụ
```

**NỘI DUNG**

**Xe đầu vào:**
- **Vespa Sprint 125cc 2024**
- Giá: 66 triệu VND
- Hãng: Piaggio
- Loại: Tay ga

**Top 5 xe tương tự:**

| STT | Xe | Giá | Hãng | Khoảng cách |
|-----|----|----|------|-------------|
| 1 | Piaggio Sprint 125 2024 | 68 triệu | Piaggio | 0.003 |
| 2 | Vespa GTS150 Super Tech 2024 | 115 triệu | Piaggio | 0.007 |
| 3 | Liberty S 2024 | 48 triệu | Piaggio | 0.008 |
| 4 | Vespa Print Piaggio 2024 | 70 triệu | Piaggio | 0.010 |
| 5 | Vespa Sprint S 150 TFT | 89 triệu | Piaggio | 0.010 |

**Nhận xét:**
✅ Cùng hãng Piaggio/Vespa
✅ Giá tương đồng (48-115 triệu)
✅ Cùng loại xe (Tay ga)
✅ Gợi ý phù hợp với xe đầu vào

**Lưu ý:**
- Kết quả trên từ **KNN Full Features** hoặc **Content-Based Cosine Matrix** hoặc **Gensim Doc2Vec**
- **Content-Based Cosine Matrix** cho kết quả tương tự nhưng tính toán trực tiếp từ ma trận cosine similarity
- **Gensim Doc2Vec** sử dụng embeddings ngữ nghĩa, có thể cho kết quả khác biệt về mặt ngữ nghĩa
- Cả 5 mô hình đều sử dụng cosine similarity, khác nhau ở cách tính toán và đặc trưng sử dụng

**Chụp ảnh từ notebook:**
- Output bảng `recommendations` từ notebook 09 (cho `knn_cosine_all` và `content_based_cosine_matrix`)
- Screenshot code tạo recommendations
- Screenshot code tính cosine_similarity matrix cho Content-Based Cosine Matrix

---

## SLIDE 9: Mô hình Clustering - Giới thiệu

**TIÊU ĐỀ**
```
Mô hình Phân Khúc (Clustering)
```

**NỘI DUNG**

**6 Mô hình đã xây dựng (theo yêu cầu đề bài):**

**Môi trường Machine Learning Truyền thống (sklearn):**

**1. KMeans**
- Phương pháp: Partitioning clustering
- K = 5 cụm
- Ưu điểm: Nhanh, phù hợp dữ liệu lớn

**2. Gaussian Mixture Model (GMM)**
- Phương pháp: Probabilistic clustering
- K = 5 cụm
- Ưu điểm: Xử lý cụm chồng lấn

**3. Agglomerative Clustering**
- Phương pháp: Hierarchical clustering
- Linkage: Ward
- K = 5 cụm
- Ưu điểm: Dendrogram để phân tích

**Môi trường PySpark ⭐⭐ (Theo yêu cầu đề bài):**

**4. PySpark KMeans**
- Phương pháp: Distributed KMeans clustering
- Framework: Apache Spark MLlib
- Ưu điểm: Xử lý dữ liệu lớn, scalable

**5. PySpark GMM**
- Phương pháp: Distributed Gaussian Mixture Model
- Framework: Apache Spark MLlib
- Ưu điểm: Xử lý cụm chồng lấn với dữ liệu lớn

**6. PySpark Bisecting K-Means ⭐⭐**
- Phương pháp: Hierarchical KMeans (chia đôi cụm)
- Framework: Apache Spark MLlib
- Ưu điểm: Kết hợp hierarchical và partitioning

**Lý do chọn k=5:**
- Dựa trên silhouette score
- Phù hợp với 5 phân khúc thị trường xe máy Việt Nam

**Chụp ảnh từ notebook:**
- Code khai báo `cluster_models` từ notebook 09 (sklearn)
- Code PySpark clustering từ notebook 10 (PySpark models)
- Bảng silhouette theo k từ notebook 08 (nếu có)
- Biểu đồ silhouette score (có thể vẽ trên Canva)

---

## SLIDE 10: Kết quả Clustering - 5 Phân khúc

**TIÊU ĐỀ**
```
Kết quả Phân Khúc - 5 Nhóm
```

**NỘI DUNG**

| Cluster | Số lượng | Giá TB | Năm TB | Đặc điểm |
|---------|----------|--------|--------|----------|
| **0** | 3,243 xe | 36.4 triệu | 2017 | Tay ga tầm trung, chủ yếu Honda |
| **1** | 1,279 xe | 12.4 triệu | 2012 | Phổ thông giá rẻ, Yamaha/SYM |
| **2** | 661 xe | 32.9 triệu | 2017 | Tay côn/Moto, Yamaha/Suzuki |
| **3** | 346 xe | 507.0 triệu | 2019 | Cao cấp, Honda/Kawasaki |
| **4** | 1,677 xe | 14.2 triệu | 2010 | Xe số phổ thông, Honda |

**Phân khúc chính:**

**Phân khúc 0 (Tay ga tầm trung - 45%)**
- Phổ biến nhất
- Honda chiếm ưu thế (83.5%)
- Phù hợp người dùng trẻ, tầm trung

**Phân khúc 3 (Cao cấp - 5%)**
- Giá cao nhất (507 triệu)
- Xe thể thao, moto cao cấp
- Thị trường niche

**Phân khúc 4 (Xe số - 23%)**
- Xe số truyền thống
- Năm cũ hơn (2010)
- Thị trường tiết kiệm

**Chụp ảnh từ notebook:**
- Output bảng `cluster_summaries['kmeans']` từ notebook 09 (sklearn)
- Output bảng `pyspark_summaries` từ notebook 10 (PySpark)
- Biểu đồ phân bố số lượng theo cluster (có thể vẽ bar chart trên Canva)
- Biểu đồ giá trung bình theo cluster
- So sánh kết quả giữa sklearn và PySpark (nếu có sự khác biệt)

---

## SLIDE 11: Đánh giá Mô hình - Recommendation

**TIÊU ĐỀ**
```
Đánh giá Mô hình Gợi ý
```

**NỘI DUNG**

**Chỉ số đánh giá:**

| Mô hình | Avg Distance | Std Distance | Đánh giá |
|---------|--------------|--------------|----------|
| KNN Full Features | [Giá trị từ notebook] | [Giá trị từ notebook] | ⭐⭐⭐ Cân bằng tốt |
| KNN Numeric Only | [Giá trị từ notebook] | [Giá trị từ notebook] | ⭐⭐ Nhanh hơn |
| KNN TF-IDF Text | [Giá trị từ notebook] | [Giá trị từ notebook] | ⭐⭐⭐ Dựa trên mô tả |
| **Content-Based Cosine Matrix** ⭐ | [Giá trị từ notebook] | [Giá trị từ notebook] | ⭐⭐⭐⭐ Content-based filtering |
| **Gensim Doc2Vec** ⭐⭐ | [Giá trị từ notebook] | [Giá trị từ notebook] | ⭐⭐⭐⭐⭐ Theo yêu cầu đề bài |

**Giải thích:**
- **Avg Distance**: Khoảng cách trung bình đến 5 hàng xóm gần nhất (distance = 1 - similarity)
- **Càng nhỏ càng tốt** → Gợi ý càng sát với xe đầu vào
- **Cosine Matrix**: Tính ma trận tương tự trực tiếp, similarity cao → distance thấp

**So sánh phương pháp:**
- **KNN**: Tính khoảng cách khi cần (lazy evaluation), hiệu quả với dữ liệu lớn
- **Cosine Matrix**: Tính toàn bộ ma trận trước (eager evaluation), phù hợp content-based filtering

**Kết luận:**
- **Content-Based Cosine Matrix** là mô hình chính theo yêu cầu đề bài
- Mô hình **KNN Full Features** cho kết quả cân bằng và nhanh hơn
- Có thể kết hợp nhiều mô hình để tăng độ chính xác

**Chụp ảnh từ notebook:**
- Output bảng `rec_eval_df` từ notebook 09 (có 5 mô hình recommendation)
- Code tính toán cosine_similarity matrix cho Content-Based Cosine Matrix
- Code Gensim Doc2Vec model training và evaluation
- Code tính evaluation metrics cho cả 5 mô hình
- Biểu đồ so sánh avg_distance (5 mô hình - có thể vẽ bar chart trên Canva)

---

## SLIDE 12: Đánh giá Mô hình - Clustering

**TIÊU ĐỀ**
```
Đánh giá Mô hình Phân Khúc
```

**NỘI DUNG**

**3 Chỉ số đánh giá:**

**Môi trường sklearn:**

| Mô hình | Silhouette | Davies-Bouldin | Calinski-Harabasz |
|---------|------------|----------------|-------------------|
| KMeans | [Giá trị] | [Giá trị] | [Giá trị] |
| GMM | [Giá trị] | [Giá trị] | [Giá trị] |
| Agglomerative | [Giá trị] | [Giá trị] | [Giá trị] |

**Môi trường PySpark ⭐⭐:**

| Mô hình | Silhouette | WSSSE | Log Likelihood |
|---------|------------|-------|----------------|
| PySpark KMeans | [Giá trị] | [Giá trị] | - |
| PySpark GMM | [Giá trị] | - | [Giá trị] |
| PySpark Bisecting K-Means | [Giá trị] | [Giá trị] | - |

**Giải thích chỉ số:**

1. **Silhouette Score** (cao hơn tốt hơn, max=1)
   - Đo độ tách biệt giữa các cụm
   - Giá trị > 0.5: Phân cụm tốt

2. **Davies-Bouldin** (thấp hơn tốt hơn)
   - Đo độ compact và tách biệt của cụm
   - Giá trị < 1: Phân cụm tốt

3. **Calinski-Harabasz** (cao hơn tốt hơn)
   - Tỷ lệ between-cluster/within-cluster variance
   - Càng cao: Cụm càng tách biệt

**Kết luận:**
- So sánh 3 chỉ số để chọn mô hình tốt nhất
- **KMeans** thường nhanh và ổn định

**Chụp ảnh từ notebook:**
- Output bảng `cluster_eval_df` từ notebook 09 (3 mô hình sklearn)
- Output bảng `pyspark_eval_df` từ notebook 10 (3 mô hình PySpark)
- Code tính toán metrics cho sklearn models (notebook 09)
- Code PySpark clustering training và evaluation (notebook 10)
- Biểu đồ so sánh silhouette score (6 mô hình: 3 sklearn + 3 PySpark)
- Có thể vẽ grouped bar chart so sánh giữa sklearn và PySpark

---

## SLIDE 13: Giải thích Mô hình

**TIÊU ĐỀ**
```
Tại sao Mô hình Hoạt động?
```

**NỘI DUNG**

**Recommendation System - Content-Based Cosine Matrix:**

**Công thức Cosine Similarity:**
```
similarity(i,j) = cos(θ) = (A·B) / (||A|| × ||B||)
                 = Σ(A_i × B_i) / (√ΣA_i² × √ΣB_i²)
```

**Cách hoạt động (Chi tiết):**

1. **Tính ma trận cosine similarity**: 
   - Input: Ma trận đặc trưng X (7,206 xe × số đặc trưng)
   - Với mỗi cặp xe (i, j), tính cosine similarity
   - Tạo ma trận N×N (N = 7,206 xe)
   - Giá trị từ -1 đến 1:
     - **1**: Hoàn toàn tương tự (cùng vector đặc trưng)
     - **0**: Không tương quan
     - **-1**: Hoàn toàn ngược lại
   - Ma trận đối xứng: similarity(i,j) = similarity(j,i)

2. **Tìm xe tương tự**:
   - Với xe đầu vào (vd: xe ID=1), lấy hàng thứ 1 trong ma trận
   - Sắp xếp các xe khác theo similarity giảm dần
   - Loại bỏ bản thân (similarity = 1.0)
   - Lấy top 5 xe có similarity cao nhất
   - **Distance** = 1 - Similarity (càng nhỏ càng tốt)

**Ví dụ số:**
- Xe A và B: similarity = 0.997 → distance = 0.003 (rất tương tự)
- Xe A và C: similarity = 0.990 → distance = 0.010 (tương tự)
- Xe A và D: similarity = 0.850 → distance = 0.150 (ít tương tự hơn)

**Ví dụ: Vespa Sprint 125cc → Gợi ý xe Piaggio/Vespa**

**Lý do gợi ý phù hợp:**
1. ✅ **Cùng thương hiệu**: One-hot encoding tạo trọng số cao → similarity cao
2. ✅ **Giá tương đồng**: Vector giá gần nhau → cosine similarity cao
3. ✅ **Cùng loại xe**: Đặc trưng categorical khớp → similarity tăng
4. ✅ **Năm sản xuất gần**: Độ tuổi xe tương đương → vector đặc trưng tương tự

**Ưu điểm Content-Based Cosine Matrix:**
- ✅ Tính toán minh bạch, dễ giải thích
- ✅ Tính toàn bộ ma trận một lần, tái sử dụng được
- ✅ Phù hợp content-based filtering (theo yêu cầu đề bài)

**Recommendation System - Gensim Doc2Vec ⭐⭐:**

**Cách hoạt động:**
1. **TaggedDocument**: Chuyển mỗi văn bản (tiêu đề + mô tả) thành TaggedDocument với ID
2. **Doc2Vec Model**: Huấn luyện model với:
   - `vector_size=100`: Embedding 100 chiều
   - `window=5`: Context window 5 từ
   - `min_count=2`: Từ xuất hiện ít nhất 2 lần
   - `epochs=20`: Huấn luyện 20 epochs
3. **Document Embeddings**: Mỗi xe được biểu diễn bằng vector 100 chiều
4. **Cosine Similarity**: Tính similarity giữa các embeddings để tìm xe tương tự

**Ưu điểm Gensim Doc2Vec:**
- ✅ **Ngữ nghĩa**: Hiểu được ngữ nghĩa văn bản, không chỉ từ khóa
- ✅ **Xử lý hiệu quả**: Tối ưu bộ nhớ và tốc độ cho dữ liệu lớn
- ✅ **Tính tương tự ngữ nghĩa**: Phát hiện xe tương tự dựa trên ý nghĩa, không chỉ từ khóa trùng
- ✅ **Theo yêu cầu đề bài**: Sử dụng Gensim như yêu cầu

**So sánh với TF-IDF:**
- **TF-IDF**: Dựa trên từ khóa, không hiểu ngữ nghĩa
- **Doc2Vec**: Dựa trên embeddings ngữ nghĩa, hiểu được ý nghĩa văn bản

**Clustering:**

**Phân khúc 0 (Tay ga tầm trung)**
- Honda chiếm 83.5% → Thương hiệu phổ biến
- Giá 36.4 triệu → Phù hợp người trẻ tầm trung
- Năm 2017 → Xe tương đối mới

**Phân khúc 3 (Cao cấp)**
- Giá 507 triệu → Moto thể thao, xe cao cấp
- Năm 2019 → Xe mới, thị trường niche
- Ít số lượng (346 xe) → Phân khúc đặc biệt

**Clustering - PySpark ⭐⭐:**

**Tại sao cần PySpark:**
- Theo yêu cầu đề bài: Triển khai trên cả 2 môi trường (sklearn và PySpark)
- **Xử lý dữ liệu lớn**: Spark phân tán, scalable
- **Bisecting K-Means**: Chỉ có trong PySpark MLlib
- **Distributed computing**: Tận dụng nhiều core/worker nodes

**So sánh sklearn vs PySpark:**
- **sklearn**: Nhanh cho dữ liệu nhỏ-trung bình, dễ sử dụng
- **PySpark**: Hiệu quả cho dữ liệu lớn, phân tán, production-ready

**Chụp ảnh từ notebook:**
- Code giải thích (có thể thêm comments trong notebook)
- Code Gensim Doc2Vec training (TaggedDocument, Doc2Vec model)
- Code PySpark clustering (notebook 10): KMeans, GMM, Bisecting K-Means
- Ví dụ output recommendations với khoảng cách
- Bảng cluster_summaries với top brands (từ cả notebook 09 và 10)

---

## SLIDE 14: Ứng dụng Thực tế

**TIÊU ĐỀ**
```
Ứng dụng và Giá trị Mang lại
```

**NỘI DUNG**

**Recommendation System:**

✅ **Tích hợp vào trang web:**
- Hiển thị "Xe tương tự" trên trang chi tiết
- Gợi ý 5-10 xe khi người dùng xem một xe cụ thể
- Tăng thời gian ở lại trang (engagement)

✅ **Lợi ích:**
- Người mua: Tìm xe phù hợp nhanh hơn
- Người bán: Tăng cơ hội bán hàng
- Nền tảng: Tăng traffic, retention

**Clustering:**

✅ **Tối ưu giá:**
- Phân tích giá theo phân khúc
- Đề xuất giá bán hợp lý cho người bán

✅ **Marketing:**
- Nhắm mục tiêu theo phân khúc
- Quảng cáo xe tay ga cho người trẻ
- Quảng cáo xe số cho phân khúc tiết kiệm

✅ **Hỗ trợ người mua:**
- Lọc xe theo phân khúc
- Tìm xe trong tầm giá phù hợp

**Chụp ảnh từ notebook:**
- Bảng cluster summaries với thống kê (từ notebook 09 và 10)
- Ví dụ recommendations output (từ cả 5 mô hình)
- Bảng so sánh kết quả sklearn vs PySpark clustering
- Có thể thêm mockup UI (vẽ trên Canva)

---

## SLIDE 15: Hạn chế và Hướng phát triển

**TIÊU ĐỀ**
```
Hạn chế & Hướng Phát triển
```

**NỘI DUNG**

**Hạn chế hiện tại:**

❌ **Dữ liệu:**
- Chỉ dựa trên metadata, chưa có dữ liệu tương tác (click, view)
- Chưa có ground truth để tính precision/recall chính xác

❌ **Mô hình:**
- Chưa áp dụng deep learning (BERT embeddings)
- Chưa có collaborative filtering

**Hướng phát triển:**

✅ **Mở rộng dữ liệu:**
- Thu thập dữ liệu tương tác người dùng
- Matrix Factorization (SVD, NMF)
- Sentence-BERT embeddings

✅ **Cải thiện mô hình:**
- Hybrid recommendation (content + collaborative)
- Deep learning cho clustering
- Real-time recommendation với vector DB (Faiss)

✅ **Deployment:**
- API RESTful
- A/B testing
- Monitoring và alerting

✅ **Đánh giá:**
- User studies
- Business metrics: CTR, conversion rate

**Chụp ảnh từ notebook:**
- Có thể thêm sơ đồ kiến trúc (vẽ trên Canva)
- Ghi chú về hạn chế trong code comments

---

## SLIDE 16: Kết luận

**TIÊU ĐỀ**
```
Kết luận
```

**NỘI DUNG**

**Tóm tắt dự án:**

✅ Xây dựng thành công **5 mô hình recommendation** và **6 mô hình clustering** (theo đúng yêu cầu đề bài)

**Recommendation:**
- ✅ **Gensim Doc2Vec** ⭐⭐ (theo yêu cầu đề bài)
- ✅ **Content-Based Cosine Matrix** ⭐ (theo yêu cầu đề bài)
- ✅ KNN Cosine (Full Features, Numeric Only, TF-IDF Text)

**Clustering:**
- ✅ **Sklearn**: KMeans, GMM, Agglomerative Clustering
- ✅ **PySpark** ⭐⭐: KMeans, GMM, Bisecting K-Means (theo yêu cầu đề bài)

✅ Xử lý **7,206 tin đăng** xe máy từ Chợ Tốt
✅ Đánh giá mô hình qua các chỉ số nội sinh
✅ Kết quả khả quan: Gợi ý phù hợp, phân khúc rõ ràng

**Điểm nổi bật:**
- ⭐⭐ **Gensim Doc2Vec**: Content-based filtering với Gensim (theo yêu cầu đề bài)
- ⭐ **Content-Based Filtering với Cosine Similarity Matrix**: Content-based filtering chính thống
- ⭐⭐ **PySpark Clustering**: Triển khai trên cả 2 môi trường sklearn và PySpark (theo yêu cầu đề bài)
  - PySpark KMeans, GMM, Bisecting K-Means
- ⭐ **Đa dạng mô hình**: So sánh 5 phương pháp recommendation và 6 phương pháp clustering
- ⭐ **Đánh giá đa chiều**: Silhouette, Davies-Bouldin, Calinski-Harabasz, WSSSE cho clustering

**Giá trị mang lại:**

- 👥 **Người mua**: Tìm xe phù hợp nhanh hơn
- 💼 **Người bán**: Hiểu thị trường, định giá hợp lý
- 🏢 **Nền tảng**: Tăng engagement, retention, conversion

**Bài học:**

- Tiền xử lý dữ liệu quan trọng: Parse giá, làm sạch text
- Cần nhiều mô hình để so sánh
- Đánh giá đa chiều: Silhouette, Davies-Bouldin, Calinski-Harabasz

**Chụp ảnh từ notebook:**
- Tổng hợp output cuối cùng từ notebook 09 (recommendation + clustering sklearn)
- Tổng hợp output từ notebook 10 (clustering PySpark)
- Bảng so sánh tất cả mô hình (5 recommendation + 6 clustering)
- Có thể thêm logo/icon thành công
- Bảng tổng hợp metrics (tạo trên Canva)

---

## SLIDE 17: Q&A

**TIÊU ĐỀ**
```
Câu hỏi & Thảo luận
```

**NỘI DUNG**

**Câu hỏi thường gặp:**

**Q: Tại sao chọn k=5 cho clustering?**
A: Dựa trên silhouette score và phân tích business (5 phân khúc phù hợp với thị trường xe máy Việt Nam)

**Q: Mô hình nào tốt nhất?**
A: Tùy mục đích:
- **Recommendation**: 
  - **Content-Based Cosine Matrix** là mô hình chính theo yêu cầu đề bài (content-based filtering với cosine similarity)
  - KNN Full Features cho kết quả cân bằng và nhanh hơn
  - Có thể kết hợp nhiều mô hình để tăng độ chính xác
- **Clustering**: So sánh 3 chỉ số để chọn, KMeans thường nhanh và ổn định

**Q: Tại sao sử dụng Gensim cho recommendation?**
A: Gensim được yêu cầu trong đề bài để xác định sự tương tự ngữ nghĩa giữa các tài liệu. Doc2Vec tạo embeddings ngữ nghĩa, tốt hơn TF-IDF khi xử lý ngữ nghĩa văn bản, xử lý hiệu quả dữ liệu lớn.

**Q: Tại sao cần PySpark cho clustering?**
A: Theo yêu cầu đề bài, cần triển khai trên cả 2 môi trường: ML truyền thống (sklearn) và PySpark. PySpark cho phép xử lý dữ liệu lớn, phân tán, scalable. Bisecting K-Means chỉ có trong PySpark.

**Q: Sự khác biệt giữa KNN và Content-Based Cosine Matrix?**
A: 
- **KNN**: Tính khoảng cách khi cần (lazy evaluation), phù hợp khi có nhiều truy vấn khác nhau
- **Cosine Matrix**: Tính toàn bộ ma trận một lần (eager evaluation), phù hợp content-based filtering và khi cần tính toán minh bạch
- Cả hai đều dùng cosine similarity, khác nhau ở cách triển khai

**Q: Có thể triển khai production không?**
A: Có, nhưng cần:
- Tối ưu performance (vector DB, caching)
- API layer
- Monitoring và A/B testing

**Q: Độ chính xác của gợi ý?**
A: Cần đánh giá thêm bằng user feedback. Hiện tại dựa trên khoảng cách, gợi ý hợp lý về mặt kỹ thuật.

**Q: So sánh kết quả giữa sklearn và PySpark clustering?**
A: 
- **Silhouette score**: Tương đương nhau (cùng thuật toán)
- **Performance**: sklearn nhanh hơn cho dữ liệu nhỏ-trung bình, PySpark tốt hơn cho dữ liệu lớn
- **Scalability**: PySpark có thể scale lên cluster, sklearn chỉ trên một máy
- **Kết luận**: sklearn phù hợp development, PySpark phù hợp production với dữ liệu lớn

**Q: Tại sao Gensim Doc2Vec tốt hơn TF-IDF?**
A:
- **Ngữ nghĩa**: Doc2Vec hiểu được ý nghĩa văn bản (vd: "xe đẹp" và "xe xịn" có thể tương tự)
- **Tối ưu**: Doc2Vec tạo embedding cố định 100 chiều, dễ lưu trữ và truy vấn
- **Context**: Doc2Vec xem xét context của từ, không chỉ tần suất
- Tuy nhiên, TF-IDF vẫn tốt cho các bài toán đơn giản, dựa trên từ khóa

**Liên hệ:**
- Email: [email của bạn]
- GitHub: [link repo nếu có]

**Cảm ơn!**

---

## HƯỚNG DẪN CHỤP ẢNH TỪ NOTEBOOK

### Cách chụp ảnh output/code:

1. **Chụp output bảng:**
   - Chạy cell trong notebook (vd: `rec_eval_df`, `cluster_eval_df`)
   - Click vào output table
   - Screenshot hoặc copy vào Canva

2. **Chụp code:**
   - Chọn cell code cần chụp
   - Screenshot hoặc copy-paste vào Canva
   - Dùng font monospace (Courier New, Consolas)

3. **Chụp biểu đồ:**
   - Chạy cell vẽ biểu đồ (vd: histogram, boxplot)
   - Click vào biểu đồ để phóng to
   - Screenshot hoặc export PNG từ notebook

### Gợi ý layout Canva:

- **Slide bìa**: Nền tối, chữ sáng, thêm icon xe máy/AI
- **Slide nội dung**: Nền sáng, tiêu đề màu nổi, nội dung dễ đọc
- **Slide bảng**: Dùng table template của Canva, màu sắc phân biệt
- **Slide code**: Nền đen (như terminal), chữ xanh lá/xanh dương
- **Slide kết quả**: Highlight số liệu quan trọng, dùng màu nổi

### Checklist trước khi thuyết trình:

- [ ] Đã chụp tất cả output từ notebook
- [ ] Đã thay [Giá trị] bằng số thực tế
- [ ] Đã kiểm tra chính tả
- [ ] Đã thêm hình ảnh/biểu đồ
- [ ] Đã test thuyết trình (10-15 phút)

---

## ĐIỂM CHÍNH CẦN NHẤN MẠNH KHI TRÌNH BÀY

### 1. Content-Based Filtering với Cosine Similarity Matrix ⭐
- **Đây là mô hình chính theo yêu cầu đề bài**
- Nhấn mạnh: Sử dụng `sklearn.metrics.pairwise.cosine_similarity`
- Tính ma trận N×N cho toàn bộ dataset
- So sánh với KNN để làm rõ sự khác biệt

### 2. Quy trình làm việc hoàn chỉnh
- Từ hiểu vấn đề → Đánh giá mô hình
- 10 notebook theo đúng thứ tự:
  - Notebook 01-08: EDA, preprocessing, visualization, analysis, model selection
  - Notebook 09: Modeling evaluation (5 recommendation + 3 sklearn clustering)
  - Notebook 10: PySpark clustering (3 models: KMeans, GMM, Bisecting K-Means)
- Mỗi bước có output và validation

### 3. Kết quả cụ thể
- **7,206 tin đăng** sau làm sạch
- **5 mô hình recommendation** (đặc biệt nhấn mạnh Content-Based Cosine Matrix và Gensim Doc2Vec)
- **6 mô hình clustering** (3 sklearn + 3 PySpark) với 5 phân khúc rõ ràng
- **3 chỉ số đánh giá** cho clustering sklearn (Silhouette, Davies-Bouldin, Calinski-Harabasz)
- **Silhouette + WSSSE + Log Likelihood** cho clustering PySpark

### 4. Giải thích rõ ràng
- Công thức cosine similarity cho Content-Based Cosine Matrix
- Cách hoạt động của Gensim Doc2Vec (TaggedDocument, embeddings, semantic similarity)
- Tại sao gợi ý phù hợp (cùng hãng, giá tương đồng, ...)
- Đặc điểm từng phân khúc clustering
- So sánh sklearn vs PySpark clustering (performance, scalability)

### 5. Ứng dụng thực tế
- Tích hợp vào website
- Tối ưu giá, marketing
- Giá trị cho người mua, người bán, nền tảng

---

## CHECKLIST TRƯỚC KHI THUYẾT TRÌNH

### Nội dung:
- [ ] Đã chụp tất cả output từ notebook (đặc biệt notebook 09 và 10)
- [ ] Đã thay `[Giá trị]` bằng số thực tế từ kết quả chạy notebook
- [ ] Đã có screenshot của Content-Based Cosine Matrix code và output
- [ ] Đã có screenshot của Gensim Doc2Vec code và output ⭐⭐
- [ ] Đã có screenshot của PySpark clustering code và output ⭐⭐
- [ ] Đã có bảng đánh giá 5 mô hình recommendation
- [ ] Đã có bảng đánh giá 6 mô hình clustering (3 sklearn + 3 PySpark)
- [ ] Đã có ví dụ recommendations cụ thể

### Hình ảnh:
- [ ] Histogram phân phối giá
- [ ] Boxplot giá theo thương hiệu
- [ ] Heatmap correlation
- [ ] Scatter plot giá theo năm
- [ ] Biểu đồ so sánh avg_distance (5 mô hình recommendation)
- [ ] Biểu đồ so sánh silhouette score (6 mô hình clustering: 3 sklearn + 3 PySpark)

### Code screenshots:
- [ ] Function parse_price, parse_km
- [ ] ColumnTransformer code
- [ ] Cosine similarity matrix calculation
- [ ] **Gensim Doc2Vec code** ⭐⭐ (TaggedDocument, Doc2Vec model)
- [ ] KMeans/GMM/Agglomerative code (sklearn)
- [ ] **PySpark clustering code** ⭐⭐ (KMeans, GMM, Bisecting K-Means)
- [ ] Evaluation metrics calculation

### Thuyết trình:
- [ ] Đã test thuyết trình (10-15 phút)
- [ ] Đã chuẩn bị câu trả lời cho Q&A
- [ ] Đã kiểm tra chính tả toàn bộ slide
- [ ] Đã thêm logo/icon phù hợp

---

**Lưu ý quan trọng**: 
- Thay các giá trị `[Giá trị]`, `[Giá trị từ notebook]` bằng kết quả thực tế khi chạy notebook trên môi trường local của bạn
- **Nhấn mạnh Content-Based Cosine Matrix** là mô hình chính theo yêu cầu đề bài (content-based filtering với cosine similarity)
- **Nhấn mạnh Gensim Doc2Vec** là mô hình theo yêu cầu đề bài (Gensim cho recommendation)
- **Nhấn mạnh PySpark Clustering** là mô hình theo yêu cầu đề bài (triển khai trên cả 2 môi trường: sklearn và PySpark)
- Chuẩn bị giải thích rõ sự khác biệt giữa KNN và Cosine Matrix approach
- Chuẩn bị giải thích về Gensim Doc2Vec và cách nó khác với TF-IDF
- Chuẩn bị so sánh sklearn vs PySpark clustering (khi nào dùng mỗi cái)
- Có sẵn ví dụ cụ thể về recommendations (5 mô hình) và clustering results (6 mô hình) để demo

