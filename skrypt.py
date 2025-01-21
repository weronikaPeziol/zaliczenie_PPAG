import arcpy

#Warstwy z budynkami
Budynki_moldawia = r"C:\studia\semestr5\programowaniw_gis\zal\moldova-latest-free.shp\gis_osm_buildings_a_free_1.shp"
Budynki_belgia = r"C:\studia\semestr5\programowaniw_gis\zal\belgium-latest-free.shp\gis_osm_buildings_a_free_1.shp"

#Warstwy z granicami
Granica_moldawia = r"C:\studia\semestr5\programowaniw_gis\zal\moldawia_gran\moldawia_gran\moldova_boundry.shp"
Granica_belgia = r"C:\studia\semestr5\programowaniw_gis\zal\belgium_gran\belgium_gran\belium_boundry.shp"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MOŁDAWIA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Stworzenie siatki kilometrowej
siatkaM = arcpy.management.CreateFishnet(
    out_feature_class=rf"C:\studia\semestr5\programowaniw_gis\zal\wyniki\siatka_M.shp",
    origin_coord="60628.1290650636 35962.0495340452",
    y_axis_coord="60628.1290650636 35972.0495340452",
    cell_width=1000,
    cell_height=1000,
    number_rows=None,
    number_columns=None,
    corner_coord="335419.778196932 373684.005501438",
    labels="NO_LABELS",
    template='60628.1290650636 35962.0495340452 335419.778196932 373684.005501438 PROJCS["MOLDREF99_Moldova_TM",GEOGCS["GCS_MOLDREF99",DATUM["D_MOLDREF99",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",200000.0],PARAMETER["False_Northing",-5000000.0],PARAMETER["Central_Meridian",28.4],PARAMETER["Scale_Factor",0.99994],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
    geometry_type="POLYGON"
)

#Selekcja
selekcjaM=arcpy.management.SelectLayerByLocation(
    in_layer= siatkaM,
    overlap_type="INTERSECT",
    select_features=Granica_moldawia,
    search_distance=None,
    selection_type="NEW_SELECTION",
    invert_spatial_relationship="NOT_INVERT"
)

#Eksport selekcji
siatkaM_select = arcpy.conversion.ExportFeatures(
    in_features=selekcjaM,
    out_features=rf"C:\studia\semestr5\programowaniw_gis\zal\wyniki\siatka_select_M.shp",
    where_clause="",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='Id "Id" true true false 6 Long 0 6,First,#,siatka,Id,-1,-1',
    sort_field=None
)

#Zamiana budynków na punkty
punktyM = arcpy.management.FeatureToPoint(
    in_features=Budynki_moldawia,
    out_feature_class=rf"C:\studia\semestr5\programowaniw_gis\zal\wyniki\punkty_M.shp",
    point_location="CENTROID"
)

#Spatial join punktów z budynków z siatką
siatka_spatial_joinM = arcpy.analysis.SpatialJoin(
    target_features=siatkaM_select,
    join_features= punktyM,
    out_feature_class=rf"C:\studia\semestr5\programowaniw_gis\zal\wyniki\siatka_spatial_join_M.shp",
    join_operation="JOIN_ONE_TO_ONE",
    join_type="KEEP_ALL",
    field_mapping='Id "Id" true true false 6 Long 0 6,First,#,siatka_select1,Id,-1,-1;osm_id "osm_id" true true false 12 Text 0 0,First,#,punkty,osm_id,0,11;code "code" true true false 4 Short 0 4,First,#,punkty,code,-1,-1;fclass "fclass" true true false 28 Text 0 0,First,#,punkty,fclass,0,27;name "name" true true false 100 Text 0 0,First,#,punkty,name,0,99;type "type" true true false 20 Text 0 0,First,#,punkty,type,0,19;ORIG_FID "ORIG_FID" true true false 10 Long 0 10,First,#,punkty,ORIG_FID,-1,-1',
    match_option="INTERSECT",
    search_radius=None,
    distance_field_name="",
    match_fields=None
)

#Tworzenie rastra
rasterM = arcpy.conversion.PolygonToRaster(
    in_features= siatka_spatial_joinM,
    value_field="Join_Count",
    out_rasterdataset=rf"C:\studia\semestr5\programowaniw_gis\zal\wyniki\raster_densit_M.tif",
    cell_assignment="CELL_CENTER",
    priority_field="NONE",
    cellsize=1000,
    build_rat="BUILD"
)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~BELGIA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Stworzenie siatki kilometrowej
siatkaB = arcpy.management.CreateFishnet(
    out_feature_class=r"C:\studia\semestr5\programowaniw_gis\zal\wyniki\siatka_b.shp",
    origin_coord="16287.8208654198 20309.7855528407",
    y_axis_coord="16287.8208654198 20319.7855528407",
    cell_width=1000,
    cell_height=1000,
    number_rows=None,
    number_columns=None,
    corner_coord="295398.726232872 244788.043335842",
    labels="NO_LABELS",
    template='16287.8208654198 20309.7855528407 295398.726232872 244788.043335842 PROJCS["Belge_Lambert_1972",GEOGCS["GCS_Belge_1972",DATUM["D_Belge_1972",SPHEROID["International_1924",6378388.0,297.0]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",150000.013],PARAMETER["False_Northing",5400088.438],PARAMETER["Central_Meridian",4.367486666666666],PARAMETER["Standard_Parallel_1",49.8333339],PARAMETER["Standard_Parallel_2",51.16666723333333],PARAMETER["Latitude_Of_Origin",90.0],UNIT["Meter",1.0]]',
    geometry_type="POLYGON"
)

#Selekcja
selekcjaB=arcpy.management.SelectLayerByLocation(
    in_layer= siatkaB,
    overlap_type="INTERSECT",
    select_features=Granica_belgia,
    search_distance=None,
    selection_type="NEW_SELECTION",
    invert_spatial_relationship="NOT_INVERT"
)

#Eksport selekcji
siatkaB_select = arcpy.conversion.ExportFeatures(
    in_features=selekcjaB,
    out_features=rf"C:\studia\semestr5\programowaniw_gis\zal\wyniki\siatka_select_B.shp",
    where_clause="",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='Id "Id" true true false 6 Long 0 6,First,#,siatka,Id,-1,-1',
    sort_field=None
)

#Zamiana budynków na punkty
punktyB = arcpy.management.FeatureToPoint(
    in_features=Budynki_belgia,
    out_feature_class= rf"C:\studia\semestr5\programowaniw_gis\zal\wyniki\punkty_B.shp",
    point_location="CENTROID"
)
#Spatial join punktów z budynków z siatką
siatka_spatial_joinB = arcpy.analysis.SpatialJoin(
    target_features=siatkaB_select,
    join_features= punktyB,
    out_feature_class=rf"C:\studia\semestr5\programowaniw_gis\zal\wyniki\siatka_spatial_join_B.shp",
    join_operation="JOIN_ONE_TO_ONE",
    join_type="KEEP_ALL",
    field_mapping='Id "Id" true true false 6 Long 0 6,First,#,siatka_select1,Id,-1,-1;osm_id "osm_id" true true false 12 Text 0 0,First,#,punkty,osm_id,0,11;code "code" true true false 4 Short 0 4,First,#,punkty,code,-1,-1;fclass "fclass" true true false 28 Text 0 0,First,#,punkty,fclass,0,27;name "name" true true false 100 Text 0 0,First,#,punkty,name,0,99;type "type" true true false 20 Text 0 0,First,#,punkty,type,0,19;ORIG_FID "ORIG_FID" true true false 10 Long 0 10,First,#,punkty,ORIG_FID,-1,-1',
    match_option="INTERSECT",
    search_radius=None,
    distance_field_name="",
    match_fields=None
)

#Tworzenie rastra
rasterB = arcpy.conversion.PolygonToRaster(
    in_features= siatka_spatial_joinB,
    value_field="Join_Count",
    out_rasterdataset=rf"C:\studia\semestr5\programowaniw_gis\zal\wyniki\raster_density_B.tif",
    cell_assignment="CELL_CENTER",
    priority_field="NONE",
    cellsize=1000,
    build_rat="BUILD"
)


print("KONIEC")