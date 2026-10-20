#!/bin/bash

# Check if the user provided a file or list of PDB IDs
if [ $# -lt 1 ]; then
    echo "Usage: $0 <pdb_id1> [pdb_id2 ...] OR $0 -f <file_with_pdb_ids>"
    exit 1
fi

# Function to download a single PDB file
download_pdb() {
    pdb_id=$1
    pdb_id_lower=$(echo "$pdb_id" | tr '[:upper:]' '[:lower:]')
    url="https://files.rcsb.org/download/${pdb_id_lower}.pdb"
    
    echo "Downloading $pdb_id from $url..."
    curl -O "$url"
    
    if [ $? -eq 0 ]; then
        echo "Successfully downloaded ${pdb_id}.pdb"
    else
        echo "Failed to download ${pdb_id}.pdb"
    fi
}

# Handle the case where PDB IDs are provided in a file
if [ "$1" == "-f" ]; then
    if [ -z "$2" ]; then
        echo "Error: Please provide a file containing PDB IDs."
        exit 1
    fi
    
    file=$2
    if [ ! -f "$file" ]; then
        echo "Error: File $file does not exist."
        exit 1
    fi
    
    while IFS= read -r pdb_id; do
        if [ ! -z "$pdb_id" ]; then
            download_pdb "$pdb_id"
        fi
    done < "$file"
else
    # Handle the case where PDB IDs are provided as arguments
    for pdb_id in "$@"; do
        download_pdb "$pdb_id"
    done
fi

