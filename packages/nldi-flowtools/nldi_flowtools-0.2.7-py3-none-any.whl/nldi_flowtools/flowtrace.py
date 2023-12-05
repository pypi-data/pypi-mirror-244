"""Generate Raindrop Trace path using NLDI and user-defined point."""
from typing import Any
from typing import Tuple
from typing import Union

import geojson
import shapely.geometry

from nldi_flowtools.utils import check_coords
from nldi_flowtools.utils import geom_to_geojson
from nldi_flowtools.utils import get_coordsys
from nldi_flowtools.utils import get_flowgrid
from nldi_flowtools.utils import get_intersection_point
from nldi_flowtools.utils import get_local_catchment
from nldi_flowtools.utils import get_local_flowline
from nldi_flowtools.utils import get_on_flowline
from nldi_flowtools.utils import get_raindrop_path
from nldi_flowtools.utils import get_reach_measure
from nldi_flowtools.utils import JsonFeatureCollectionType
from nldi_flowtools.utils import project_point
from nldi_flowtools.utils import split_flowline


class Flowtrace:
    """Define inputs and outputs for the main Flowtrace class."""

    def __init__(self, x: float, y: float, direction: str) -> None:
        """Initialize Flowtrace."""
        self.x = x
        self.y = y
        self.direction = direction
        self.catchmentIdentifier: str
        self.flowline: JsonFeatureCollectionType
        self.flw = None
        self.flwdir_transform: object
        self.projected_xy = Tuple[float, float]
        self.onFlowline: bool

        # geoms
        self.catchmentGeom = shapely.geometry
        self.intersectionPointGeom = shapely.geometry.point.Point
        self.raindropPathGeom = shapely.geometry.linestring.LineString
        self.nhdFlowlineGeom = shapely.geometry.linestring.LineString
        self.upstreamFlowlineGeom = shapely.geometry.linestring.LineString
        self.downstreamFlowlineGeom = shapely.geometry.linestring.LineString
        self.downstreamPathGeom = shapely.geometry.linestring.LineString

        # outputs
        self.catchment: JsonFeatureCollectionType
        self.raindropPath: JsonFeatureCollectionType
        self.nhdFlowline: JsonFeatureCollectionType
        self.streamInfo: dict[str, Union[Tuple[Any, Any], str, float, None]]
        self.upstreamFlowline: JsonFeatureCollectionType
        self.downstreamFlowline: JsonFeatureCollectionType
        self.downstreamPath: JsonFeatureCollectionType

        # create transform
        self.transformToRaster: object
        self.transformToWGS84: object

        # kick off
        self.run()

    def serialize(self) -> geojson.feature.FeatureCollection:  # noqa C901
        """Convert returns to GeoJSON to be exported."""
        if self.onFlowline is True:
            if self.direction == "up":
                feature1 = geojson.Feature(
                    geometry=self.upstreamFlowline,
                    id="upstreamFlowline",
                    properties=self.streamInfo,
                )
                featurecollection = geojson.FeatureCollection([feature1])

            if self.direction == "down":
                feature1 = geojson.Feature(
                    geometry=self.downstreamFlowline,
                    id="downstreamFlowline",
                    properties=self.streamInfo,
                )
                featurecollection = geojson.FeatureCollection([feature1])

            if self.direction == "none":
                feature1 = geojson.Feature(
                    geometry=self.nhdFlowline,
                    id="nhdFlowline",
                    properties=self.streamInfo,
                )
                featurecollection = geojson.FeatureCollection([feature1])

        if self.onFlowline is False:
            if self.direction == "up":
                feature1 = geojson.Feature(
                    geometry=self.upstreamFlowline,
                    id="upstreamFlowline",
                    properties=self.streamInfo,
                )
                feature2 = geojson.Feature(
                    geometry=self.raindropPath, id="raindropPath"
                )
                featurecollection = geojson.FeatureCollection([feature1, feature2])

            if self.direction == "down":
                feature1 = geojson.Feature(
                    geometry=self.downstreamFlowline,
                    id="downstreamFlowline",
                    properties=self.streamInfo,
                )
                feature2 = geojson.Feature(
                    geometry=self.raindropPath, id="raindropPath"
                )
                featurecollection = geojson.FeatureCollection([feature1, feature2])

            if self.direction == "none":
                feature1 = geojson.Feature(
                    geometry=self.nhdFlowline,
                    id="nhdFlowline",
                    properties=self.streamInfo,
                )
                feature2 = geojson.Feature(
                    geometry=self.raindropPath, id="raindropPath"
                )
                featurecollection = geojson.FeatureCollection([feature1, feature2])

        return featurecollection

    # main functions
    def run(self) -> None:  # noqa C901
        """Run FLowtrace module."""
        # Order of these functions is important!
        check_coords(self.x, self.y)
        self.catchmentIdentifier, self.catchmentGeom = get_local_catchment(
            self.x, self.y
        )
        self.flowline, self.nhdFlowlineGeom = get_local_flowline(
            self.catchmentIdentifier
        )
        self.transformToRaster, self.transformToWGS84 = get_coordsys()
        self.projected_xy = project_point(self.x, self.y, self.transformToRaster)
        self.flw, self.flwdir_transform = get_flowgrid(
            self.catchmentGeom, self.transformToRaster
        )
        self.onFlowline = get_on_flowline(
            self.projected_xy, self.flowline, self.transformToRaster
        )
        self.catchment = geom_to_geojson(self.catchmentGeom)

        if self.onFlowline is True:
            self.intersectionPointGeom = get_intersection_point(
                self.x, self.y, raindrop_path=None
            )
            self.streamInfo = get_reach_measure(
                self.intersectionPointGeom, self.flowline
            )
            self.upstreamFlowlineGeom, self.downstreamFlowlineGeom = split_flowline(
                self.intersectionPointGeom, self.flowline
            )

            # Outputs
            if self.direction == "up":
                self.upstreamFlowline = geom_to_geojson(self.upstreamFlowlineGeom)

            if self.direction == "down":
                self.downstreamFlowline = geom_to_geojson(self.downstreamFlowlineGeom)

            if self.direction == "none":
                self.nhdFlowline = geom_to_geojson(self.nhdFlowlineGeom)

        if self.onFlowline is False:
            self.raindropPathGeom = get_raindrop_path(
                self.flw,
                self.projected_xy,
                self.nhdFlowlineGeom,
                self.flowline,
                self.transformToRaster,
                self.transformToWGS84,
            )
            self.intersectionPointGeom, self.raindropPathGeom = get_intersection_point(
                self.x, self.y, raindrop_path=self.raindropPathGeom
            )
            # self.streamInfo = get_reach_measure(self.intersectionPointGeom, self.flowline)
            self.upstreamFlowlineGeom, self.downstreamFlowlineGeom = split_flowline(
                self.intersectionPointGeom, self.flowline
            )

            # Outputs
            if self.direction == "up":
                self.upstreamFlowline = geom_to_geojson(self.upstreamFlowlineGeom)
                self.raindropPath = geom_to_geojson(self.raindropPathGeom)

            if self.direction == "down":
                self.downstreamFlowline = geom_to_geojson(self.downstreamFlowlineGeom)
                self.raindropPath = geom_to_geojson(self.raindropPathGeom)

            if self.direction == "none":
                self.nhdFlowline = geom_to_geojson(self.nhdFlowlineGeom)
                self.raindropPath = geom_to_geojson(self.raindropPathGeom)

            self.streamInfo = get_reach_measure(
                self.intersectionPointGeom, self.flowline, self.raindropPathGeom
            )
