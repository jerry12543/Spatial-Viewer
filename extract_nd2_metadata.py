import nd2
from pathlib import Path
import json

DATA_PATH = Path("./data/Brain08/")
OUTPUT_PATH = Path("./data/Brain08/metadata/")

if not DATA_PATH.is_dir():
    raise NotADirectoryError(f"{DATA_PATH} is not a directory")

metadata = {}

for file_path in DATA_PATH.iterdir():
    if (
        not file_path.is_file()
        or file_path.suffix != ".nd2"
        or not nd2.ND2File.is_supported_file(file_path)
    ):
        continue

    image_metadata = {}
    with nd2.ND2File(file_path) as f:
        channelCount = f.attributes.channelCount
        width = f.attributes.widthPx
        height = f.attributes.heightPx
        numImagesPerChannel = f.attributes.sequenceCount

        dimensions = (channelCount, width, height, numImagesPerChannel)

        # channel and voxel data
        channels = f.metadata.channels
        channel_data = []
        for channel in channels:
            curr_channel = {}
            curr_channel["name"] = channel.channel.name  # str
            curr_channel["index"] = channel.channel.index  # int
            curr_channel["color"] = (
                channel.channel.color.as_abgr_u4()
            )  # can be reversed with Color.from_abgr_u4()
            curr_channel["voxelCount"] = (
                channel.volume.voxelCount
            )  # tuple -- should be the same as dimensions (except for first index)
            channel_data.append(curr_channel)

    image_metadata["dimensions"] = dimensions
    image_metadata["perChannelData"] = channel_data
    filename = file_path.stem
    metadata[filename] = image_metadata

# store the metadata
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
out_file = OUTPUT_PATH / "metadata.json"
with out_file.open("w") as w:
    json.dump(metadata, w, indent=2)
print(
    f"read metadata from the following files: {[f + '.nd2' for f in metadata.keys()]}"
)
