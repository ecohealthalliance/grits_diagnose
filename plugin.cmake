# add_python_test(search PLUGIN diagnose)
if(PYTHON_STYLE_TESTS)
  add_python_style_test(pep8_style_diagnose
                        "${PROJECT_SOURCE_DIR}/plugins/diagnose/server")
endif()
