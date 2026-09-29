# Automated Encroachment Check Pipeline

A micro-service pipeline designed to parse unstructured telemetry feeds, handle Coordinate Reference System (CRS) management, and run spatial intersection triggers against protected zones.

## Quick Start

### 1. Environment Setup
```bash
# Clone the repository
git clone <your-repo-link>
cd encroachment-pipeline

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install exact dependencies
pip install -r requirements.txt
```

### 2. Execution
Run the automated routing script:
```bash
python pipeline.py
```

---

## Architectural & Production Scaling Decisions

### 1. Framework Choice: Why GeoPandas/Shapely?
For lightweight batch worker environments (like AWS Lambda functions or Cloud Run triggers responding to newly dropped telemetry files), **GeoPandas** keeps code simple without requiring heavy infrastructural overhead. 

### 2. Scaling Up to Production Spatial Pipelines
To scale this solution up to thousands of high-velocity satellite images or millions of coordinate telemetry points daily, the pipeline would be upgraded using the following architectural layers:

* **Spatial Database (PostGIS):** Shift calculations to an indexing database. By creating a database table with an `rtree` spatial index (`GIST`), point-in-polygon math drops from an O(N) linear scan to highly efficient logarithmic speeds.
* **Spatial Pre-Filtering (Bounding Boxes):** Before computing complex polygon intersections on large datasets, filter coordinates out early by running a quick bounding box limit check (`polygon.bounds`).
* **Distributed Engines (Apache Sedona / Dask-GeoPandas):** For large cluster distributed environments handling massive geographic datasets across multiple machines simultaneously.
