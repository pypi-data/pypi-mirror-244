# ! /usr/bin/env python3

# Copyright zengwenwu,1441778423@qq.com

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from osgeo import gdal, osr

class LatLonReader(object):
    '''
    Return the maximum of an array or maximum along an axis.
        Parameters
        ----------
        file_path : the file path of *.tif

        Returns
        -------
        getHeight : float,float
            return the latitude, longitude
            If pixel_x or pixel_y is out of *.tif image shape, the result is "None".
    '''

    def __init__(self, image_path):
        dataset = gdal.Open(image_path)
        self.source = osr.SpatialReference()
        self.source.ImportFromWkt(dataset.GetProjection())
        self.trans = dataset.GetGeoTransform()
        # width hight
        self.width = dataset.RasterXSize
        self.height = dataset.RasterYSize
        self.target = None
        self.ct = None
        if self.source.IsGeographic():
            pass
            # print("|--------------*.tif文件为地理坐标--------------|")
        else:
            # print("|--------------*.tif文件为投影坐标--------------|")
            # 继承了 source 的投影信息，但将其转换为地理坐标系
            self.target = self.source.CloneGeogCS()
            self.ct = osr.CoordinateTransformation(self.source, self.target)

    def getLatLon(self, pixel_x: int, pixel_y: int):
        if not (pixel_x < self.width and pixel_y < self.height):
            return None, None

        geo_x, geo_y = self._pixel2lonlat(pixel_x, pixel_y)
        if self.ct:
            geo_y, geo_x, _ = self.ct.TransformPoint(geo_x, geo_y)
        return geo_y, geo_x

    def _pixel2lonlat(self, pixel_x, pixel_y):
        geo_x = self.trans[0] + pixel_x*self.trans[1] + pixel_y*self.trans[2]
        geo_y = self.trans[3] + pixel_x*self.trans[4] + pixel_y*self.trans[5]
        return geo_x, geo_y

    def printInfo(self):
        print("Trans: ", self.trans)
        print("Width: ", self.width)
        print("Height: ", self.height)


class DEMReader(object):
    '''
    Return the maximum of an array or maximum along an axis.
        Parameters
        ----------
        dem_path : the file path of DEM Data

        Returns
        -------
        getHeight : int
            return the height of this position(latitude, longitude)
            If latitude or longitude is out of *.tif image shape, the result is "-1".
    '''

    def __init__(self, dem_path: str) -> None:
        self.dem_path = dem_path
        self.elevation, self.trans = self._readElevationAndTrans()
        self.nrows, self.ncols = self.elevation.shape

    def _readElevationAndTrans(self):
        ds = gdal.Open(self.dem_path)
        band = ds.GetRasterBand(1)
        elevation = band.ReadAsArray()
        trans = ds.GetGeoTransform()
        return elevation, trans

    def getHeight(self, latitude: float, longitude: float) -> int:
        new_nrows = int((latitude - self.trans[3]) / self.trans[5])
        new_ncols = int((longitude - self.trans[0]) / self.trans[1])
        if not ((new_nrows > 0) & (new_ncols > 0) & new_nrows < self.nrows and new_ncols < self.ncols):
            return -1
        return self.elevation[new_nrows][new_ncols]


class LatLonHeightReader(object):
    def __init__(self, image_path: str, dem_path: str) -> None:
        self.latlon_reader = LatLonReader(image_path)
        self.dem_reader = DEMReader(dem_path)

    def getLatLonHeight(self, pixel_x: int, pixel_y: int):
        lat, lon = self.latlon_reader.getLatLon(pixel_x, pixel_y)
        if lat is None or lon is None:
            return None, None, -1
        height = self.dem_reader.getHeight(lat, lon)
        return lat, lon, height


if __name__ == "__main__":

    dem_path = "xxx.tif"
    image_path = "xxx.tif"
    # your pixel
    pixel_x, pixel_y = 942, 876

    latlonheight_reader = LatLonHeightReader(image_path, dem_path)
    lat, lon, height = latlonheight_reader.getLatLonHeight(pixel_x, pixel_y)
    if (height > -1):
        print(f'Lat: {lat}° Lon: {lon}° Height: {height}m')
    else:
        print("Input Value ERROR")
