#!/usr/bin/env bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export source_dir=$THIS_DIR/../..

export android_abi=arm64-v8a
$THIS_DIR/_impl_cmake_android.sh
