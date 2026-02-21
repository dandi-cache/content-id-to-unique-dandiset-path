import gzip
import json
import pathlib

import requests
import yaml


def _run(base_directory: pathlib.Path, /) -> None:
    url = "https://raw.githubusercontent.com/dandi-cache/content-id-to-dandiset-paths/refs/heads/min/derivatives/content_id_to_dandiset_paths.min.json.gz"
    response = requests.get(url)
    content_id_to_dandiset_paths = json.loads(gzip.decompress(data=response.content))

    content_id_to_unique_dandiset_path: dict[str, dict[str, list[str]]] = dict()
    multiple_dandisets: dict[str, dict[str, list[str]]] = dict()
    multiple_paths_same_dandiset: dict[str, dict[str, list[str]]] = dict()

    for content_id, dandisets in content_id_to_dandiset_paths.items():
        if len(dandisets) > 1:
            multiple_dandisets[content_id] = dandisets
            continue

        dandiset_id, paths = next(iter(dandisets.items()))
        if len(paths) > 1:
            multiple_paths_same_dandiset[content_id] = {dandiset_id: paths}
            continue

        content_id_to_unique_dandiset_path[content_id] = {dandiset_id: paths}

    outputs = {
        "content_id_to_unique_dandiset_path.yaml": content_id_to_unique_dandiset_path,
        "multiple_dandisets.yaml": multiple_dandisets,
        "multiple_paths_same_dandiset.yaml": multiple_paths_same_dandiset,
    }
    for filename, data in outputs.items():
        with (base_directory / "derivatives" / filename).open(mode="w") as file_stream:
            yaml.safe_dump(data=data, stream=file_stream)


if __name__ == "__main__":
    repo_head = pathlib.Path(__file__).parent.parent

    _run(repo_head)
