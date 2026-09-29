import json
import logging
from typing import Any, Dict, List
import geopandas as gpd
import pandas as pd
from shapely import wkt
from shapely.geometry import Point

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_mock_data() -> Dict[str, Any]:
    """Provides the raw mock data string provided in the challenge prompt."""
    raw_json = """
    {
      "protection_zone_wkt": "POLYGON ((32.5800 0.3200, 32.6000 0.3200, 32.6000 0.3400, 32.5800 0.3400, 32.5800 0.3200))",
      "protection_zone_crs": "EPSG:4326",
      "detected_points": [
        {"point_id": "LOC_001", "lon": 32.5900, "lat": 0.3300, "description": "Foundation excavation observed"},
        {"point_id": "LOC_002", "lon": 32.5750, "lat": 0.3250, "description": "Commercial warehouse structure"},
        {"point_id": "LOC_003", "lon": 32.5950, "lat": 0.3350, "description": "Active bricklaying site"},
        {"point_id": "LOC_004", "lon": 32.6100, "lat": 0.3500, "description": "Residential fence wall completed"},
        {"point_id": "LOC_005", "lon": 32.5850, "lat": 0.3220, "description": "Grading of marshland vegetation"}
      ]
    }
    """
    return json.loads(raw_json)


def build_geometries(data: Dict[str, Any]) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Parses raw text and dictionaries into spatially aligned GeoDataFrames."""
    crs = data["protection_zone_crs"]
    logger.info(f"Parsing spatial data using CRS: {crs}")

    zone_polygon = wkt.loads(data["protection_zone_wkt"])
    zone_gdf = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[zone_polygon])

    points_list: List[Dict[str, Any]] = data["detected_points"]
    df = pd.DataFrame(points_list)
    geometry = [Point(xy) for xy in zip(df["lon"], df["lat"])]
    points_gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

    return zone_gdf, points_gdf


def find_encroachments(
    zone_gdf: gpd.GeoDataFrame, points_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Performs a spatial join to isolate points within the protection perimeter."""
    logger.info("Executing spatial intersection query...")
    encroachments = gpd.sjoin(points_gdf, zone_gdf, how="inner", predicate="within")

    if "index_right" in encroachments.columns:
        encroachments = encroachments.drop(columns=["index_right"])

    return encroachments


def run_pipeline() -> None:
    """Executes the pipeline lifecycle and logs out flagged records."""
    try:
        raw_data = load_mock_data()
        zone_layer, points_layer = build_geometries(raw_data)

        flagged_gdf = find_encroachments(zone_layer, points_layer)

        logger.info(f"Pipeline complete. Flagged {len(flagged_gdf)} infringements.")

        output_fields = ["point_id", "lon", "lat", "description"]
        output_records = flagged_gdf[output_fields].to_dict(orient="records")

        print("\n=== FLAGGED ENCROACHMENT RECORDS ===")
        print(json.dumps(output_records, indent=2))
        print("====================================\n")

    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}", exc_info=True)


if __name__ == "__main__":
    run_pipeline()
