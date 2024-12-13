#!/usr/bin/env bash

me=$(basename "$0")

set -e  # exit on error
for f in scripts/*.sh; do {
    base_name=$(basename ${f})

    # Skip this file
    if [ ${base_name} = ${me} ]; then
        continue
    fi

    bash "$f"
}
done
