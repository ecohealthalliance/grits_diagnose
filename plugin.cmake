add_python_test(diagnose PLUGIN grits_diagnose)
if(PYTHON_STYLE_TESTS)
  add_python_style_test(pep8_style_grits_diagnose
                        "${PROJECT_SOURCE_DIR}/plugins/grits_diagnose/server")
endif()
