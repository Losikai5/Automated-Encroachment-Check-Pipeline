import pytest
import geopandas as gpd
from shapely.geometry import Polygon, Point
from pipeline import find_encroachments

@pytest.fixture
def sample_zone_gdf():
    """Creates a basic square protection zone polygon for testing."""
    # A box from longitude 32.58 to 32.60, and latitude 0.32 to 0.34
    polygon = Polygon([(32.58, 0.32), (32.60, 0.32), (32.60, 0.34), (32.58, 0.34), (32.58, 0.32)])
    return gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[polygon])

def test_encroachment_inside_point(sample_zone_gdf):
    """Verifies that a point clearly inside the zone is successfully flagged."""
    point = Point(32.59, 0.33)  # Dead center
    points_gdf = gpd.GeoDataFrame([{"point_id": "TEST_IN", "description": "Inside"}], crs="EPSG:4326", geometry=[point])
    
    result = find_encroachments(sample_zone_gdf, points_gdf)
    
    assert len(result) == 1
    assert result.iloc[0]["point_id"] == "TEST_IN"

def test_encroachment_outside_point(sample_zone_gdf):
    """Verifies that a point clearly outside the zone is safely ignored."""
    point = Point(32.50, 0.30)  # Far away south-west
    points_gdf = gpd.GeoDataFrame([{"point_id": "TEST_OUT", "description": "Outside"}], crs="EPSG:4326", geometry=[point])
    
    result = find_encroachments(sample_zone_gdf, points_gdf)
    
    assert len(result) == 0

def test_empty_points_dataframe(sample_zone_gdf):
    """Ensures the intersection pipeline framework doesn't crash on empty datasets."""
    empty_gdf = gpd.GeoDataFrame(columns=["point_id", "description", "geometry"], crs="EPSG:4326")
    
    result = find_encroachments(sample_zone_gdf, empty_gdf)
    
    assert len(result) == 0

