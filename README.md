# SpatialInformaticsProject
# Hydrological Pattern Analysis: Rivers & Reservoirs  
## A Multi-Sensor Remote Sensing Study of the Krishna River Basin

## Overview
This project presents a scalable geospatial analysis framework for monitoring river morphology, reservoir dynamics, and groundwater–surface water coupling using multi-sensor remote sensing data. The study focuses on the Krishna River basin and the Nagarjuna Sagar reservoir, analyzing hydrological behavior across seasonal, interannual, and decadal timescales.

By integrating optical satellite imagery, climatic datasets, and land data assimilation products, the project quantifies river width variation, channel migration, reservoir storage trends, and land-use-driven hydrological impacts in a data-scarce environment.

---

## Key Objectives
- Quantify seasonal and long-term changes in river width and reservoir surface area  
- Separate river channels from reservoir backwaters using geometry-based algorithms  
- Analyze groundwater recharge as a predictor of dry-season surface water availability  
- Measure channel migration rates and identify erosion hotspots  
- Study land-use change impacts within hydrologically sensitive buffer zones  

---

## Datasets Used

| Dataset        | Resolution / Period | Purpose |
|---------------|---------------------|---------|
| Sentinel-2 MSI | 10 m, 2018–2025 | River width, reservoir area, LULC near water bodies |
| Landsat 5 | 30 m, 1995–2015 | Decadal trend analysis |
| CHIRPS | Daily rainfall | Climatic forcing and monsoon analysis |
| GLDAS | Soil moisture | Groundwater proxy and recharge analysis |
| Bhuvan LULC | Classified maps | Land-use change detection |

---

## Methodology

### 1. Water Body Extraction
- Applied NDWI and MNDWI on multispectral imagery to generate binary water masks  
- Removed noise by filtering water bodies smaller than 1 km²  

### 2. River–Reservoir Separation
- Developed a morphology-based erosion algorithm to distinguish narrow linear river channels from wide reservoir bodies  
- Reservoirs retained a structural core after erosion, while river channels fragmented, enabling automated classification  

### 3. River Width Estimation
- Estimated river width using an area–perimeter approximation to enable robust basin-scale analysis without point-wise measurements  

### 4. Channel Migration Analysis
- Extracted river centerlines across multiple years and computed lateral migration rates using boundary-distance metrics  
- Identified spatial erosion hotspots and quantified average migration rates (~20 m/year in active zones)  

### 5. Hydro-Climatic Coupling
- Correlated monsoon rainfall, groundwater recharge (GLDAS), and dry-season surface water extent  
- Demonstrated a strong lagged relationship (r ≈ 0.75) between groundwater recharge and dry-season river health  

---

## Key Findings
- Reservoir surface area in winter often exceeds monsoon levels, indicating active dam management strategies  
- Groundwater acts as a “hydrological bank,” sustaining river flows during dry periods  
- River channels exhibit localized high-migration hotspots (up to ~66 m/year) rather than uniform erosion  
- Agricultural land use expanded by ~4.93% independent of short-term hydrological stress  
- Decadal analysis shows a significant increase in regulated reservoir storage (1995–2025)  

---

## Applications
- Floodplain zoning and infrastructure risk assessment  
- Reservoir operation and water security planning  
- Large-scale environmental monitoring in data-scarce regions  
- Predictive modeling for river dynamics and erosion risk  

---

## Future Work
- Predictive modeling of channel migration under climate change scenarios  
- Flood-risk mapping using population and infrastructure layers  
- Integration of SAR data to mitigate cloud-cover limitations  

---

## Tech Stack
- **Language:** Python  
- **Geospatial:** GeoPandas, Rasterio, Shapely  
- **Scientific Computing:** NumPy, pandas, SciPy  
- **Remote Sensing:** NDWI, MNDWI, Sentinel-2, Landsat  
- **Analysis:** Time-series processing, statistical correlation  

---

## Authors
Aman Srivastava  
Rohan Naidu  
Gajawada Bharath  

International Institute of Information Technology, Hyderabad
