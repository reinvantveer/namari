#!/usr/bin/env bash
set -eux pipefail


# Pull a pre-compiled version of QGIS from Docker hub
IMAGE=qgis/qgis
TAG=release-3_18
docker pull ${IMAGE}:${TAG}

# Run the image so that we can extract the compiled PyQGIS lib from it,
# store the container id in the file .tmp-container-id
docker run \
  -it \
  --rm \
  --cidfile .tmp-container-id \
  -d \
  ${IMAGE}:${TAG} sh

# Copy the contents of the QGIS python output dir to the target dir
TARGET_DIR=~/.local/qgis-build-output
SRC_DIR=/QGIS/build/output
mkdir -p ${TARGET_DIR}
xargs -I {} docker container cp -a "{}:${SRC_DIR}" - < .tmp-container-id > ${TARGET_DIR}/build-output.tar
pushd ${TARGET_DIR} || exit
tar xf build-output.tar
popd || exit

# Cleanup:
# Stop the QGIS container
xargs -I {} docker container stop "{}" < .tmp-container-id
# Remove the intermediate tarball
rm ${TARGET_DIR}/build-output.tar
# Remove the tempfile containing the container id
rm .tmp-container-id

echo "You can now add ${TARGET_DIR}/output/python to your PYTHONPATH to enable IDE integration"
