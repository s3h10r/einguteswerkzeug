#!/bin/bash -vx
./test_generators_basic.sh || echo "... test_generators_basic : FAILED" && exit 1
echo "... test_generators_basic : ok"
./test_filters_basic.sh || echo "... test_filters_basic : FAILED" && exit 1
echo "... test_filters_basic : ok"
