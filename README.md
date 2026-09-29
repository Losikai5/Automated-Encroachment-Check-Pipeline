# Automated Encroachment Check Pipeline

A small Python geospatial pipeline that checks whether detected locations fall inside a protected area. It was built for a technical mini-challenge using GeoPandas and Shapely.

The supplied sample contains a protected polygon in WKT format and five detected locations as longitude/latitude pairs. The pipeline converts them into geometries, assigns both layers the boundary’s CRS (`EPSG:4326`), and uses a spatial join to find points within the polygon. It prints the matching records as JSON.

> This project processes the challenge’s provided coordinates. It does not ingest or analyze satellite imagery.

## Results for the sample data

The pipeline flags `LOC_001`, `LOC_003`, and `LOC_005`. `LOC_002` and `LOC_004` are outside the protected polygon. The spatial predicate is `within`, so points exactly on the polygon boundary are not included.

## Requirements

- Python 3.10 or newer
- Dependencies listed in `requirements.txt`

## Setup

```bash
git clone <your-public-repository-url>
cd <repository-directory>
python3 -m venv venv
source venv/bin/activate
 # Windows PowerShell: venv\Scripts\Activate.ps1
 pip install -r requirements.txt
```

## Run

```bash
python pipeline.py
```

The script logs progress and prints the flagged records in a JSON array. It uses the mock input embedded in `pipeline.py`.

## Run tests

```bash
pytest -v
```

The tests cover an inside point, an outside point, and an empty points dataset.

## Project files

```text
pipeline.py            Loads sample data, builds geometries, and finds encroachments
tests/test_pipeline.py Unit tests for the spatial query
requirements.txt       Python dependencies
```

## CRS and scope

The sample polygon and detected coordinates are both in `EPSG:4326` (longitude/latitude), so no reprojection is needed. The code assigns that CRS to both GeoDataFrames. For other input data, confirm the coordinate reference system first and reproject one layer with `to_crs()` when the source CRSs differ; assigning a CRS does not transform coordinates.

This is a compact example intended for the provided challenge input. A production system would also need input validation, configurable data sources, operational error handling, and testing against its chosen spatial-index dependencies and data volumes.
