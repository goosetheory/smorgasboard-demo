pushd board_tests
pytest
popd

pushd payment_tests
pytest
popd

pushd presigned_url_tests
pytest
popd