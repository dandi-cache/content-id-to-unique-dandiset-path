import pathlib

import requests
import yaml


def _run(base_directory: pathlib.Path, /) -> None:
    # Download the cache data
    cache_url = "https://raw.githubusercontent.com/dandi-cache/content-id-to-dandiset-paths/main/cache.json"
    response = requests.get(cache_url)
    cache = response.json()

    # Filter to only content IDs with unique file paths
    unique_cache = {content_id: paths[0] for content_id, paths in cache.items() if len(paths) == 1}

    # Write to YAML in derivatives directory
    derivatives_dir = base_directory / "derivatives"
    derivatives_dir.mkdir(exist_ok=True)

    output_file = derivatives_dir / "unique_content_id_to_path.yaml"
    with output_file.open("w") as f:
        yaml.dump(unique_cache, f, default_flow_style=False, sort_keys=True)


if __name__ == "__main__":
    repo_head = pathlib.Path(__file__).parent.parent

    _run(repo_head)
