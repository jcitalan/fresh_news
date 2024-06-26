#!/bin/bash

set_version() {
    local file=$1
    local pattern=$3

    if [ -f "$file" ]; then
        echo "Updating version in $file"
        awk -v ver="$VERSION" "$pattern" "$file" > temp && mv temp "$file"
    fi
}

VERSION=$1
SCRAPERS="scrapers"
CURRENT_DIR=$(pwd)
SCRAPE_DIR="${CURRENT_DIR}/${SCRAPERS}"
INIT_FILE="${SCRAPE_DIR}/__init__.py"

if [ -d "$SCRAPE_DIR" ]; then
    echo "Entered the ${RETAILER} directory"

    set_version "$INIT_FILE" "$VERSION" '/__version__/ {$3 = "\"" ver "\""} 1'
else
    echo "The ${SCRAPERS} directory was not found in the current directory"
fi
