"""
Motorbike dataset analysis pipeline without heavy numeric dependencies.
Reads the CSV export, validates and preprocesses data, runs textual EDA,
and trains lightweight recommendation and clustering models implemented
with standard Python modules.
"""

from __future__ import annotations

import csv
import json
import math
import os
import random
from collections import Counter, defaultdict
from statistics import mean, median
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import os
from pathlib import Path

# Import config
try:
    from config import RAW_DATA_FILE as DATA_PATH
except ImportError:
    # Fallback if config not available
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_PATH = PROJECT_ROOT / "data" / "data_motobikes.xlsx - Sheet1.csv"
RANDOM_SEED = 42


# ---------------------------------------------------------------------------
# Utility parsing helpers
# ---------------------------------------------------------------------------

def _clean_text(value: str) -> str:
    if value is None:
        return ""
    return " ".join(value.strip().split())


def _parse_price(raw: str) -> Optional[float]:
    """Return price in millions of VND from strings like '66.000.000 đ' or '72.53 tr'."""
    if not raw:
        return None
    value = raw.lower().strip()
    if value in {"đang cập nhật", "liên hệ"}:
        return None
    value = value.replace("đ", "").replace("vnđ", "").replace("vnd", "")
    value = value.replace("triệu", "tr").replace("tỷ", "ty")
    value = value.replace(",", ".")
    value = value.replace(" ", "")
    # Values like 66.000.000 become 66 million. Remove dots from thousand separators.
    if value.endswith("tr"):
        num = value[:-2]
        try:
            return float(num)
        except ValueError:
            return None
    if value.endswith("ty"):
        num = value[:-2]
        try:
            return float(num) * 1000.0
        except ValueError:
            return None
    digits = value.replace(".", "")
    try:
        return float(digits) / 1_000_000.0
    except ValueError:
        return None


def _parse_year(raw: str) -> Optional[int]:
    if not raw:
        return None
    raw = raw.strip()
    if not raw or raw.lower() in {"đang cập nhật", "khác"}:
        return None
    try:
        year = int(raw[:4])
        if 1950 <= year <= 2030:
            return year
    except ValueError:
        return None
    return None


def _parse_kilometers(raw: str) -> Optional[float]:
    if not raw:
        return None
    raw = raw.lower().strip()
    if raw in {"đang cập nhật", "khác"}:
        return None
    raw = raw.replace("km", "").replace(",", "").replace(".", "")
    raw = raw.replace(" ", "")
    try:
        return float(raw)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Data ingestion & preprocessing
# ---------------------------------------------------------------------------

def load_dataset(path: str = DATA_PATH) -> List[Dict[str, str]]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows: List[Dict[str, str]] = [dict(row) for row in reader]
    return rows


def preprocess_records(rows: Iterable[Dict[str, str]]) -> List[Dict[str, object]]:
    cleaned: List[Dict[str, object]] = []
    for row in rows:
        price = _parse_price(row.get("Giá", ""))
        price_min = _parse_price(row.get("Khoảng giá min", ""))
        price_max = _parse_price(row.get("Khoảng giá max", ""))
        year = _parse_year(row.get("Năm đăng ký", ""))
        km = _parse_kilometers(row.get("Số Km đã đi", ""))
        cleaned.append(
            {
                "id": row.get("id"),
                "title": _clean_text(row.get("Tiêu đề", "")),
                "price_m": price,
                "price_min_m": price_min,
                "price_max_m": price_max,
                "address": _clean_text(row.get("Địa chỉ", "")),
                "description": _clean_text(row.get("Mô tả chi tiết", "")),
                "brand": _clean_text(row.get("Thương hiệu", "")).lower(),
                "model": _clean_text(row.get("Dòng xe", "")).lower(),
                "year": year,
                "kilometers": km,
                "condition": _clean_text(row.get("Tình trạng", "")).lower(),
                "vehicle_type": _clean_text(row.get("Loại xe", "")).lower(),
                "displacement": _clean_text(row.get("Dung tích xe", "")).lower(),
                "origin": _clean_text(row.get("Xuất xứ", "")).lower(),
                "warranty": _clean_text(row.get("Chính sách bảo hành", "")).lower(),
            }
        )
    return cleaned


# ---------------------------------------------------------------------------
# Validation & EDA
# ---------------------------------------------------------------------------

def validate_data(records: Sequence[Dict[str, object]]) -> Dict[str, object]:
    total = len(records)
    missing_counts = Counter()
    for record in records:
        for field in [
            "price_m",
            "price_min_m",
            "price_max_m",
            "year",
            "kilometers",
            "brand",
            "vehicle_type",
        ]:
            if not record.get(field):
                missing_counts[field] += 1
    return {
        "total_rows": total,
        "missing_counts": dict(missing_counts),
    }


def eda_summary(records: Sequence[Dict[str, object]]) -> Dict[str, object]:
    prices = [r["price_m"] for r in records if isinstance(r.get("price_m"), (int, float))]
    years = [r["year"] for r in records if isinstance(r.get("year"), int)]
    kms = [r["kilometers"] for r in records if isinstance(r.get("kilometers"), (int, float))]

    brand_counter = Counter(r.get("brand") for r in records if r.get("brand"))
    type_counter = Counter(r.get("vehicle_type") for r in records if r.get("vehicle_type"))

    def describe(series: Sequence[float]) -> Dict[str, float]:
        if not series:
            return {}
        ordered = sorted(series)
        mid = len(ordered) // 2
        median_value = (
            ordered[mid]
            if len(ordered) % 2
            else (ordered[mid - 1] + ordered[mid]) / 2
        )
        return {
            "count": len(series),
            "min": ordered[0],
            "max": ordered[-1],
            "mean": mean(series),
            "median": median_value,
        }

    def top_items(counter: Counter, n: int = 10) -> List[Tuple[str, int]]:
        return counter.most_common(n)

    return {
        "price_stats": describe(prices),
        "year_stats": describe(years),
        "kilometer_stats": describe(kms),
        "top_brands": top_items(brand_counter),
        "top_vehicle_types": top_items(type_counter),
    }


# ---------------------------------------------------------------------------
# Feature engineering helpers for modeling
# ---------------------------------------------------------------------------

def _build_category_map(records: Sequence[Dict[str, object]], field: str) -> Dict[str, int]:
    unique = sorted({r[field] for r in records if r.get(field)})
    return {value: idx for idx, value in enumerate(unique)}


def _prepare_feature_vectors(records: Sequence[Dict[str, object]]) -> Tuple[List[Dict[str, object]], Dict[str, Dict[str, float]]]:
    usable: List[Dict[str, object]] = []
    for record in records:
        if record.get("price_m") is None:
            continue
        usable.append(record)

    price_values = [r["price_m"] for r in usable if r.get("price_m") is not None]
    year_values = [r["year"] for r in usable if r.get("year") is not None]
    km_values = [r["kilometers"] for r in usable if r.get("kilometers") is not None]

    price_min, price_max = min(price_values), max(price_values)
    year_min, year_max = (min(year_values), max(year_values)) if year_values else (None, None)
    km_min, km_max = (min(km_values), max(km_values)) if km_values else (None, None)

    brand_map = _build_category_map(usable, "brand")
    type_map = _build_category_map(usable, "vehicle_type")
    displacement_map = _build_category_map(usable, "displacement")
    condition_map = _build_category_map(usable, "condition")

    def scale(value: Optional[float], low: Optional[float], high: Optional[float]) -> float:
        if value is None or low is None or high is None or math.isclose(low, high):
            return 0.5
        return (float(value) - low) / (high - low)

    vectors = []
    for record in usable:
        vector = {
            "id": record.get("id"),
            "record": record,
            "price": scale(record.get("price_m"), price_min, price_max),
            "year": scale(record.get("year"), year_min, year_max),
            "km": scale(record.get("kilometers"), km_min, km_max),
            "brand": brand_map.get(record.get("brand"), -1) / max(len(brand_map), 1),
            "vehicle_type": type_map.get(record.get("vehicle_type"), -1)
            / max(len(type_map), 1),
            "displacement": displacement_map.get(record.get("displacement"), -1)
            / max(len(displacement_map), 1),
            "condition": condition_map.get(record.get("condition"), -1)
            / max(len(condition_map), 1),
        }
        vectors.append(vector)

    return vectors, {
        "price": {"min": price_min, "max": price_max},
        "year": {"min": year_min, "max": year_max},
        "km": {"min": km_min, "max": km_max},
        "brand_map": brand_map,
        "vehicle_type_map": type_map,
        "displacement_map": displacement_map,
        "condition_map": condition_map,
    }


def _vector_to_list(vector: Dict[str, float]) -> List[float]:
    return [
        vector["price"],
        vector["year"],
        vector["km"],
        vector["brand"],
        vector["vehicle_type"],
        vector["displacement"],
        vector["condition"],
    ]


def _euclidean_distance(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


# ---------------------------------------------------------------------------
# Recommendation model (kNN using Euclidean distance)
# ---------------------------------------------------------------------------

def recommend_similar(
    vectors: Sequence[Dict[str, object]],
    target_id: str,
    top_n: int = 5,
) -> List[Tuple[Dict[str, object], float]]:
    lookup = {v["id"]: v for v in vectors}
    if target_id not in lookup:
        raise ValueError(f"Listing id {target_id} not found in dataset")
    target_vector = _vector_to_list(lookup[target_id])
    scores: List[Tuple[Dict[str, object], float]] = []
    for vector in vectors:
        if vector["id"] == target_id:
            continue
        dist = _euclidean_distance(target_vector, _vector_to_list(vector))
        scores.append((vector["record"], dist))
    scores.sort(key=lambda item: item[1])
    return scores[:top_n]


# ---------------------------------------------------------------------------
# Clustering model (vanilla KMeans)
# ---------------------------------------------------------------------------

def kmeans(
    vectors: Sequence[Dict[str, object]],
    k: int = 5,
    max_iters: int = 50,
) -> Tuple[List[List[Dict[str, object]]], List[List[float]]]:
    random.seed(RANDOM_SEED)
    points = [_vector_to_list(v) for v in vectors]
    if len(points) < k:
        raise ValueError("Not enough points for clustering")
    centroids = [points[idx] for idx in random.sample(range(len(points)), k)]

    def assign_clusters() -> List[int]:
        assignment = []
        for point in points:
            distances = [_euclidean_distance(point, centroid) for centroid in centroids]
            assignment.append(distances.index(min(distances)))
        return assignment

    assignment = assign_clusters()
    for iteration in range(max_iters):
        clusters: Dict[int, List[List[float]]] = defaultdict(list)
        for idx, cluster_id in enumerate(assignment):
            clusters[cluster_id].append(points[idx])
        new_centroids: List[List[float]] = []
        for cluster_id in range(k):
            cluster_points = clusters.get(cluster_id)
            if not cluster_points:
                new_centroids.append(random.choice(points))
                continue
            centroid = [mean(dim_values) for dim_values in zip(*cluster_points)]
            new_centroids.append(centroid)
        if all(
            _euclidean_distance(old, new) < 1e-4
            for old, new in zip(centroids, new_centroids)
        ):
            centroids = new_centroids
            break
        centroids = new_centroids
        new_assignment = assign_clusters()
        if new_assignment == assignment:
            break
        assignment = new_assignment

    cluster_records: List[List[Dict[str, object]]] = [list() for _ in range(k)]
    for vector, cluster_id in zip(vectors, assignment):
        cluster_records[cluster_id].append(vector["record"])

    return cluster_records, centroids


def cluster_summary(
    clusters: Sequence[Sequence[Dict[str, object]]],
    centroids: Sequence[Sequence[float]],
    stats: Dict[str, Dict[str, float]],
) -> List[Dict[str, object]]:
    summaries = []
    for idx, (items, centroid) in enumerate(zip(clusters, centroids)):
        prices = [item["price_m"] for item in items if item.get("price_m") is not None]
        years = [item["year"] for item in items if item.get("year") is not None]
        kms = [item["kilometers"] for item in items if item.get("kilometers") is not None]
        brands = Counter(item.get("brand") for item in items if item.get("brand"))
        types = Counter(item.get("vehicle_type") for item in items if item.get("vehicle_type"))
        summaries.append(
            {
                "cluster": idx,
                "size": len(items),
                "avg_price_m": mean(prices) if prices else None,
                "median_year": median(years) if years else None,
                "median_km": median(kms) if kms else None,
                "top_brands": brands.most_common(3),
                "top_vehicle_types": types.most_common(3),
                "centroid": centroid,
            }
        )
    return summaries


# ---------------------------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------------------------

def wcss(clusters: Sequence[Sequence[Dict[str, object]]], centroids: Sequence[Sequence[float]], vector_lookup: Dict[str, List[float]]) -> float:
    total = 0.0
    for items, centroid in zip(clusters, centroids):
        for item in items:
            point = vector_lookup[item["id"]]
            total += _euclidean_distance(point, centroid) ** 2
    return total


# ---------------------------------------------------------------------------
# Pipeline orchestration
# ---------------------------------------------------------------------------

def run_pipeline(sample_listing_id: Optional[str] = None) -> Dict[str, object]:
    print("Loading dataset...")
    rows = load_dataset()
    print(f"Loaded {len(rows)} raw rows")

    print("Preprocessing records...")
    records = preprocess_records(rows)
    print(f"Records after preprocessing: {len(records)}")

    print("Validating data...")
    validation_metrics = validate_data(records)
    print(json.dumps(validation_metrics, indent=2, ensure_ascii=False))

    print("Running EDA summary...")
    eda_metrics = eda_summary(records)
    print(json.dumps(eda_metrics, indent=2, ensure_ascii=False))

    print("Preparing feature vectors...")
    vectors, stats = _prepare_feature_vectors(records)
    print(f"Feature vectors prepared: {len(vectors)} usable rows")

    vector_lookup = {v["id"]: _vector_to_list(v) for v in vectors}

    recommender_output = None
    if sample_listing_id and sample_listing_id in vector_lookup:
        print(f"Generating recommendations for listing {sample_listing_id}...")
        recs = recommend_similar(vectors, sample_listing_id, top_n=5)
        recommender_output = [
            {
                "id": rec["id"],
                "title": rec["title"],
                "price_m": rec["price_m"],
                "brand": rec["brand"],
                "model": rec["model"],
                "distance": dist,
            }
            for rec, dist in recs
        ]
        print(json.dumps(recommender_output, indent=2, ensure_ascii=False))
    else:
        print("No sample listing supplied or listing not found; skipping recommendation demo")

    print("Running KMeans clustering...")
    clusters, centroids = kmeans(vectors, k=5)
    summaries = cluster_summary(clusters, centroids, stats)
    print(json.dumps(summaries, indent=2, ensure_ascii=False))

    print("Computing WCSS metric...")
    total_wcss = wcss(clusters, centroids, vector_lookup)
    print(f"WCSS: {total_wcss:.4f}")

    return {
        "validation": validation_metrics,
        "eda": eda_metrics,
        "recommendations": recommender_output,
        "cluster_summaries": summaries,
        "wcss": total_wcss,
    }


if __name__ == "__main__":
    random.seed(RANDOM_SEED)
    # Use the first record's id for the recommendation demo
    try:
        data = load_dataset()
        sample_id = data[0]["id"] if data else None
    except FileNotFoundError:
        sample_id = None
    outputs = run_pipeline(sample_id)
    with open("analysis_outputs.json", "w", encoding="utf-8") as handle:
        json.dump(outputs, handle, indent=2, ensure_ascii=False)
    print("Outputs saved to analysis_outputs.json")
