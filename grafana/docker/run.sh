#!/bin/bash
SCRIPT_DIR=$(dirname $(readlink -e $0))
. ${SCRIPT_DIR}/image


set -e
shift
IMAGE=${IMAGE} k2-compose -f ${SCRIPT_DIR}/k2-compose.yml up $*
