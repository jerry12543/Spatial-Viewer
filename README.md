# Tasks

- [x] Set up a conda environment with tifffile, nd2, numpy, dask, zarr, and napari
- [x] Visualize tiff file
- [x] Write a script to extract metadata from the ND2 files (dimensions, voxel sizes, channel info)
- [ ] Load and visualize a sample file in napari to understand the data structure
- [ ] Document findings


# Quickstart

```
git clone git@github.com:jerry12543/Spatial-Viewer.git
cd Spatial-Viewer
conda env create -f environment.yml
conda activate spatial-viewer
```


# ND2 Metadata Extraction
Modify the DATA_PATH and OUTPUT_PATH fields at the top of extract_nd2_metadata.py. For all .nd2 files in DATA_PATH, the extract_nd2_metadata.py script extracts:

## Extracted Metadata

### Global (per file)
- `channelCount`: number of channels  
- `widthPx`: image width (pixels)  
- `heightPx`: image height (pixels)  
- `sequenceCount`: number of images per channel  

Stored as:
- `dimensions = (channelCount, width, height, sequenceCount)`

### Per Channel
- `name`: channel name  
- `index`: channel index  
- `color`: ABGR `uint32`  
- `voxelCount`: voxel dimensions  

## Output
All metadata is written to:
```
OUTPUT_PATH/metadata.json
```

```
Structure:
{
    "filename": {
        "dimensions": [...],
        "perChannelData: [
            {
                "name": "...",
                "index": ...,
                "color": ...,
                "voxelCount": [...]
            },
            ...
        ]
    },
    ...
}
```
To run the script, from the Spatial-Viewer folder run:
```
conda activate spatial-viewer
python extract_nd2_metadata.py
```