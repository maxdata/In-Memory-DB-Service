# Test Results Report

Generated: 2025-03-23 09:33:31  

Python Version: 3.11.9

## Overall Summary
### Total Results
🟢 **Total Passed**: 109  
🔴 **Total Failed**: 0  
🟡 **Total Errors**: 0  
⏱️ **Total Time**: 16.25s

### Results by Category
| Category | Description | Passed | Failed | Errors | Time (s) |
|----------|-------------|--------:|--------:|--------:|---------:|
| **Config** | Configuration and environment setup tests | ✓ 1 | ✗ 0 | ! 0 | 0.43 |
| **Models** | Data model validation and schema tests | ✓ 8 | ✗ 0 | ! 0 | 0.44 |
| **Utils** | Utility function and helper method tests | ✓ 10 | ✗ 0 | ! 0 | 0.43 |
| **Database** | In-memory database operations and data persistence tests | ✓ 7 | ✗ 0 | ! 0 | 0.27 |
| **Api Main** | Core API functionality and endpoint tests | ✓ 5 | ✗ 0 | ! 0 | 0.59 |
| **Api Utils** | API utility functions and middleware tests | ✓ 6 | ✗ 0 | ! 0 | 0.61 |
| **Services** | Business logic and service layer tests | ✓ 7 | ✗ 0 | ! 0 | 0.35 |
| **Normal** | Standard use case and happy path tests | ✓ 19 | ✗ 0 | ! 0 | 0.77 |
| **Edge** | Edge cases, error handling, and boundary condition tests | ✓ 28 | ✗ 0 | ! 0 | 0.74 |
| **Performance** | Performance benchmarks and load testing | ✓ 18 | ✗ 0 | ! 0 | 11.62 |

## Coverage Summary
📊 **Overall Coverage**: 97.31%  
📝 **Total Statements**: 595  
❌ **Missing Statements**: 16

### Coverage by File
| File | Coverage % | Statements | Missing |
|------|------------|------------|---------|
| main.py | 100.00% | 47 | 0 |
| utils.py | 100.00% | 48 | 0 |
| api/deps.py | 100.00% | 13 | 0 |
| api/main.py | 100.00% | 6 | 0 |
| api/v1/tables.py | 94.31% | 123 | 7 |
| api/v1/utils.py | 88.89% | 9 | 1 |
| core/config.py | 100.00% | 12 | 0 |
| db/base.py | 100.00% | 94 | 0 |
| db/initial_data.py | 100.00% | 20 | 0 |
| models/order.py | 100.00% | 22 | 0 |
| models/user.py | 100.00% | 10 | 0 |
| schemas/base.py | 100.00% | 7 | 0 |
| schemas/order.py | 94.87% | 39 | 2 |
| schemas/user.py | 100.00% | 22 | 0 |
| services/base_service.py | 100.00% | 28 | 0 |
| services/order_service.py | 94.00% | 50 | 3 |
| services/user_service.py | 93.33% | 45 | 3 |


## Config Tests
🟢 **Passed**: 1  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.43s

### Detailed Output
```
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-8.3.5, pluggy-1.5.0
cachedir: .pytest_cache
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /backend
configfile: pytest.ini
plugins: cov-6.0.0, asyncio-0.25.3, anyio-4.8.0, langsmith-0.3.15, benchmark-4.0.0
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=function
collecting ... collected 1 item

tests/test_src/test_config.py::test_settings_defaults PASSED             [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      7    94%   166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     94     41    56%   121, 133-138, 180, 201-207, 221-223, 256, 261, 266-297, 299-303, 305, 309-348
app/db/initial_data.py             20      0   100%
app/main.py                        47      0   100%
app/models/order.py                22      0   100%
app/models/user.py                 10      0   100%
app/schemas/base.py                 7      0   100%
app/schemas/order.py               39      2    95%   38, 54
app/schemas/user.py                22      0   100%
app/services/base_service.py       28      0   100%
app/services/order_service.py      50      3    94%   33, 62, 67
app/services/user_service.py       45      3    93%   34, 62, 67
app/utils.py                       48      0   100%
-------------------------------------------------------------
TOTAL                             595     57    90%
Coverage XML written to file /backend/tests/test_reports/coverage.xml


============================== 1 passed in 0.43s ===============================

```


---

## Models Tests
🟢 **Passed**: 8  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.44s

### Detailed Output
```
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-8.3.5, pluggy-1.5.0
cachedir: .pytest_cache
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /backend
configfile: pytest.ini
plugins: cov-6.0.0, asyncio-0.25.3, anyio-4.8.0, langsmith-0.3.15, benchmark-4.0.0
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=function
collecting ... collected 8 items

tests/test_src/test_models.py::test_user_model_creation PASSED           [ 12%]
tests/test_src/test_models.py::test_user_model_validation PASSED         [ 25%]
tests/test_src/test_models.py::test_user_model_required_fields PASSED    [ 37%]
tests/test_src/test_models.py::test_order_model_creation PASSED          [ 50%]
tests/test_src/test_models.py::test_order_model_validation PASSED        [ 62%]
tests/test_src/test_models.py::test_order_model_required_fields PASSED   [ 75%]
tests/test_src/test_models.py::test_order_status_transitions PASSED      [ 87%]
tests/test_src/test_models.py::test_user_order_model PASSED              [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      7    94%   166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     94     41    56%   121, 133-138, 180, 201-207, 221-223, 256, 261, 266-297, 299-303, 305, 309-348
app/db/initial_data.py             20      0   100%
app/main.py                        47      0   100%
app/models/order.py                22      0   100%
app/models/user.py                 10      0   100%
app/schemas/base.py                 7      0   100%
app/schemas/order.py               39      2    95%   38, 54
app/schemas/user.py                22      0   100%
app/services/base_service.py       28      0   100%
app/services/order_service.py      50      3    94%   33, 62, 67
app/services/user_service.py       45      3    93%   34, 62, 67
app/utils.py                       48      0   100%
-------------------------------------------------------------
TOTAL                             595     57    90%
Coverage XML written to file /backend/tests/test_reports/coverage.xml


============================== 8 passed in 0.44s ===============================

```


---

## Utils Tests
🟢 **Passed**: 10  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.43s

### Detailed Output
```
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-8.3.5, pluggy-1.5.0
cachedir: .pytest_cache
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /backend
configfile: pytest.ini
plugins: cov-6.0.0, asyncio-0.25.3, anyio-4.8.0, langsmith-0.3.15, benchmark-4.0.0
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=function
collecting ... collected 10 items

tests/test_src/test_utils.py::test_datetime_formatting PASSED            [ 10%]
tests/test_src/test_utils.py::test_uuid_parsing PASSED                   [ 20%]
tests/test_src/test_utils.py::test_generate_record_id PASSED             [ 30%]
tests/test_src/test_utils.py::test_table_name_validation PASSED          [ 40%]
tests/test_src/test_utils.py::test_record_data_validation PASSED         [ 50%]
tests/test_src/test_utils.py::test_validate_join_key PASSED              [ 60%]
tests/test_src/test_utils.py::test_error_response_formatting PASSED      [ 70%]
tests/test_src/test_utils.py::test_success_response_formatting PASSED    [ 80%]
tests/test_src/test_utils.py::test_record_id_validation PASSED           [ 90%]
tests/test_src/test_utils.py::test_join_operations PASSED                [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      7    94%   166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     94     41    56%   121, 133-138, 180, 201-207, 221-223, 256, 261, 266-297, 299-303, 305, 309-348
app/db/initial_data.py             20      0   100%
app/main.py                        47      0   100%
app/models/order.py                22      0   100%
app/models/user.py                 10      0   100%
app/schemas/base.py                 7      0   100%
app/schemas/order.py               39      2    95%   38, 54
app/schemas/user.py                22      0   100%
app/services/base_service.py       28      0   100%
app/services/order_service.py      50      3    94%   33, 62, 67
app/services/user_service.py       45      3    93%   34, 62, 67
app/utils.py                       48      0   100%
-------------------------------------------------------------
TOTAL                             595     57    90%
Coverage XML written to file /backend/tests/test_reports/coverage.xml


============================== 10 passed in 0.43s ==============================

```


---

## Database Tests
🟢 **Passed**: 7  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.27s

### Detailed Output
```
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-8.3.5, pluggy-1.5.0
cachedir: .pytest_cache
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /backend
configfile: pytest.ini
plugins: cov-6.0.0, asyncio-0.25.3, anyio-4.8.0, langsmith-0.3.15, benchmark-4.0.0
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=function
collecting ... collected 7 items

tests/test_src/test_db.py::test_db_initialization PASSED                 [ 14%]
tests/test_src/test_db.py::test_db_crud_operations PASSED                [ 28%]
tests/test_src/test_db.py::test_db_error_handling PASSED                 [ 42%]
tests/test_src/test_db.py::test_db_concurrent_operations PASSED          [ 57%]
tests/test_src/test_db.py::test_db_table_operations PASSED               [ 71%]
tests/test_src/test_db.py::test_db_relationships PASSED                  [ 85%]
tests/test_src/test_db.py::test_db_sample_data PASSED                    [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      7    94%   166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     94      2    98%   267, 321
app/db/initial_data.py             20      0   100%
app/main.py                        47      0   100%
app/models/order.py                22      0   100%
app/models/user.py                 10      0   100%
app/schemas/base.py                 7      0   100%
app/schemas/order.py               39      2    95%   38, 54
app/schemas/user.py                22      0   100%
app/services/base_service.py       28      0   100%
app/services/order_service.py      50      3    94%   33, 62, 67
app/services/user_service.py       45      3    93%   34, 62, 67
app/utils.py                       48      0   100%
-------------------------------------------------------------
TOTAL                             595     18    97%
Coverage XML written to file /backend/tests/test_reports/coverage.xml


============================== 7 passed in 0.27s ===============================

```


---

## Api_Main Tests
🟢 **Passed**: 5  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.59s

### Detailed Output
```
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-8.3.5, pluggy-1.5.0
cachedir: .pytest_cache
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /backend
configfile: pytest.ini
plugins: cov-6.0.0, asyncio-0.25.3, anyio-4.8.0, langsmith-0.3.15, benchmark-4.0.0
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=function
collecting ... collected 5 items

tests/test_src/test_api_main.py::test_root PASSED                        [ 20%]
tests/test_src/test_api_main.py::test_cors_middleware PASSED             [ 40%]
tests/test_src/test_api_main.py::test_database_error_handler PASSED      [ 60%]
tests/test_src/test_api_main.py::test_general_exception_handler PASSED   [ 80%]
tests/test_src/test_api_main.py::test_lifespan PASSED                    [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      7    94%   166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     94      2    98%   267, 321
app/db/initial_data.py             20      0   100%
app/main.py                        47      0   100%
app/models/order.py                22      0   100%
app/models/user.py                 10      0   100%
app/schemas/base.py                 7      0   100%
app/schemas/order.py               39      2    95%   38, 54
app/schemas/user.py                22      0   100%
app/services/base_service.py       28      0   100%
app/services/order_service.py      50      3    94%   33, 62, 67
app/services/user_service.py       45      3    93%   34, 62, 67
app/utils.py                       48      0   100%
-------------------------------------------------------------
TOTAL                             595     18    97%
Coverage XML written to file /backend/tests/test_reports/coverage.xml


============================== 5 passed in 0.59s ===============================

```


---

## Api_Utils Tests
🟢 **Passed**: 6  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.61s

### Detailed Output
```
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-8.3.5, pluggy-1.5.0
cachedir: .pytest_cache
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /backend
configfile: pytest.ini
plugins: cov-6.0.0, asyncio-0.25.3, anyio-4.8.0, langsmith-0.3.15, benchmark-4.0.0
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=function
collecting ... collected 6 items

tests/test_src/test_api_utils.py::test_health_check PASSED               [ 16%]
tests/test_src/test_api_utils.py::test_health_check_method_not_allowed PASSED [ 33%]
tests/test_src/test_api_utils.py::test_router_prefix PASSED              [ 50%]
tests/test_src/test_api_utils.py::test_router_routes PASSED              [ 66%]
tests/test_src/test_api_utils.py::test_health_check_in_main_app PASSED   [ 83%]
tests/test_src/test_api_utils.py::test_health_check_integration PASSED   [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      7    94%   166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     94      2    98%   267, 321
app/db/initial_data.py             20      0   100%
app/main.py                        47      0   100%
app/models/order.py                22      0   100%
app/models/user.py                 10      0   100%
app/schemas/base.py                 7      0   100%
app/schemas/order.py               39      2    95%   38, 54
app/schemas/user.py                22      0   100%
app/services/base_service.py       28      0   100%
app/services/order_service.py      50      3    94%   33, 62, 67
app/services/user_service.py       45      3    93%   34, 62, 67
app/utils.py                       48      0   100%
-------------------------------------------------------------
TOTAL                             595     18    97%
Coverage XML written to file /backend/tests/test_reports/coverage.xml


============================== 6 passed in 0.61s ===============================

```


---

## Services Tests
🟢 **Passed**: 7  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.35s

### Detailed Output
```
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-8.3.5, pluggy-1.5.0
cachedir: .pytest_cache
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /backend
configfile: pytest.ini
plugins: cov-6.0.0, asyncio-0.25.3, anyio-4.8.0, langsmith-0.3.15, benchmark-4.0.0
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=function
collecting ... collected 7 items

tests/test_src/test_services.py::test_base_service_initialization PASSED [ 14%]
tests/test_src/test_services.py::test_base_service_create PASSED         [ 28%]
tests/test_src/test_services.py::test_base_service_get PASSED            [ 42%]
tests/test_src/test_services.py::test_base_service_update PASSED         [ 57%]
tests/test_src/test_services.py::test_base_service_delete PASSED         [ 71%]
tests/test_src/test_services.py::test_base_service_list PASSED           [ 85%]
tests/test_src/test_services.py::test_base_service_exists PASSED         [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      7    94%   166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     94      2    98%   267, 321
app/db/initial_data.py             20      0   100%
app/main.py                        47      0   100%
app/models/order.py                22      0   100%
app/models/user.py                 10      0   100%
app/schemas/base.py                 7      0   100%
app/schemas/order.py               39      2    95%   38, 54
app/schemas/user.py                22      0   100%
app/services/base_service.py       28      0   100%
app/services/order_service.py      50      3    94%   33, 62, 67
app/services/user_service.py       45      3    93%   34, 62, 67
app/utils.py                       48      0   100%
-------------------------------------------------------------
TOTAL                             595     18    97%
Coverage XML written to file /backend/tests/test_reports/coverage.xml


============================== 7 passed in 0.35s ===============================

```


---

## Normal Tests
🟢 **Passed**: 19  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.77s

### Detailed Output
```
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-8.3.5, pluggy-1.5.0
cachedir: .pytest_cache
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /backend
configfile: pytest.ini
plugins: cov-6.0.0, asyncio-0.25.3, anyio-4.8.0, langsmith-0.3.15, benchmark-4.0.0
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=function
collecting ... collected 19 items

tests/test_src/test_api_normal.py::test_create_user PASSED               [  5%]
tests/test_src/test_api_normal.py::test_create_order PASSED              [ 10%]
tests/test_src/test_api_normal.py::test_get_user PASSED                  [ 15%]
tests/test_src/test_api_normal.py::test_update_user_variations[test_case0] PASSED [ 21%]
tests/test_src/test_api_normal.py::test_update_user_variations[test_case1] PASSED [ 26%]
tests/test_src/test_api_normal.py::test_update_user_variations[test_case2] PASSED [ 31%]
tests/test_src/test_api_normal.py::test_delete_user PASSED               [ 36%]
tests/test_src/test_api_normal.py::test_list_users PASSED                [ 42%]
tests/test_src/test_api_normal.py::test_get_user_orders PASSED           [ 47%]
tests/test_src/test_api_normal.py::test_get_order_user PASSED            [ 52%]
tests/test_src/test_api_normal.py::test_dump_table PASSED                [ 57%]
tests/test_src/test_api_normal.py::test_list_orders PASSED               [ 63%]
tests/test_src/test_api_normal.py::test_update_order_variations[test_case0] PASSED [ 68%]
tests/test_src/test_api_normal.py::test_update_order_variations[test_case1] PASSED [ 73%]
tests/test_src/test_api_normal.py::test_update_order_variations[test_case2] PASSED [ 78%]
tests/test_src/test_api_normal.py::test_update_order_variations[test_case3] PASSED [ 84%]
tests/test_src/test_api_normal.py::test_delete_order PASSED              [ 89%]
tests/test_src/test_api_normal.py::test_health_check PASSED              [ 94%]
tests/test_src/test_api_normal.py::test_readiness_check PASSED           [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      7    94%   166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     94      1    99%   321
app/db/initial_data.py             20      0   100%
app/main.py                        47      0   100%
app/models/order.py                22      0   100%
app/models/user.py                 10      0   100%
app/schemas/base.py                 7      0   100%
app/schemas/order.py               39      2    95%   38, 54
app/schemas/user.py                22      0   100%
app/services/base_service.py       28      0   100%
app/services/order_service.py      50      3    94%   33, 62, 67
app/services/user_service.py       45      3    93%   34, 62, 67
app/utils.py                       48      0   100%
-------------------------------------------------------------
TOTAL                             595     17    97%
Coverage XML written to file /backend/tests/test_reports/coverage.xml


============================== 19 passed in 0.77s ==============================

```


---

## Edge Tests
🟢 **Passed**: 28  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.74s

### Detailed Output
```
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-8.3.5, pluggy-1.5.0
cachedir: .pytest_cache
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /backend
configfile: pytest.ini
plugins: cov-6.0.0, asyncio-0.25.3, anyio-4.8.0, langsmith-0.3.15, benchmark-4.0.0
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=function
collecting ... collected 28 items

tests/test_src/test_api_edge_cases.py::test_create_user_invalid_data PASSED [  3%]
tests/test_src/test_api_edge_cases.py::test_get_user_invalid_uuid PASSED [  7%]
tests/test_src/test_api_edge_cases.py::test_get_nonexistent_user PASSED  [ 10%]
tests/test_src/test_api_edge_cases.py::test_update_user_invalid_uuid PASSED [ 14%]
tests/test_src/test_api_edge_cases.py::test_update_nonexistent_user PASSED [ 17%]
tests/test_src/test_api_edge_cases.py::test_delete_user_invalid_uuid PASSED [ 21%]
tests/test_src/test_api_edge_cases.py::test_delete_nonexistent_user PASSED [ 25%]
tests/test_src/test_api_edge_cases.py::test_get_orders_invalid_user_uuid PASSED [ 28%]
tests/test_src/test_api_edge_cases.py::test_get_orders_nonexistent_user PASSED [ 32%]
tests/test_src/test_api_edge_cases.py::test_get_order_user_invalid_uuid PASSED [ 35%]
tests/test_src/test_api_edge_cases.py::test_get_order_user_nonexistent_order PASSED [ 39%]
tests/test_src/test_api_edge_cases.py::test_dump_nonexistent_table PASSED [ 42%]
tests/test_src/test_api_edge_cases.py::test_verify_deleted_user PASSED   [ 46%]
tests/test_src/test_api_edge_cases.py::test_create_user_empty_values PASSED [ 50%]
tests/test_src/test_api_edge_cases.py::test_create_user_special_characters PASSED [ 53%]
tests/test_src/test_api_edge_cases.py::test_concurrent_user_updates PASSED [ 57%]
tests/test_src/test_api_edge_cases.py::test_order_with_deleted_user PASSED [ 60%]
tests/test_src/test_api_edge_cases.py::test_boundary_values PASSED       [ 64%]
tests/test_src/test_api_edge_cases.py::test_update_order_invalid_uuid PASSED [ 67%]
tests/test_src/test_api_edge_cases.py::test_update_nonexistent_order PASSED [ 71%]
tests/test_src/test_api_edge_cases.py::test_update_order_invalid_status PASSED [ 75%]
tests/test_src/test_api_edge_cases.py::test_update_order_invalid_amount PASSED [ 78%]
tests/test_src/test_api_edge_cases.py::test_delete_order_invalid_uuid PASSED [ 82%]
tests/test_src/test_api_edge_cases.py::test_delete_nonexistent_order PASSED [ 85%]
tests/test_src/test_api_edge_cases.py::test_health_check_edge_cases PASSED [ 89%]
tests/test_src/test_api_edge_cases.py::test_readiness_check_edge_cases PASSED [ 92%]
tests/test_src/test_api_edge_cases.py::test_dump_table_invalid_format PASSED [ 96%]
tests/test_src/test_api_edge_cases.py::test_dump_table_concurrent_access PASSED [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      7    94%   166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     94      0   100%
app/db/initial_data.py             20      0   100%
app/main.py                        47      0   100%
app/models/order.py                22      0   100%
app/models/user.py                 10      0   100%
app/schemas/base.py                 7      0   100%
app/schemas/order.py               39      2    95%   38, 54
app/schemas/user.py                22      0   100%
app/services/base_service.py       28      0   100%
app/services/order_service.py      50      3    94%   33, 62, 67
app/services/user_service.py       45      3    93%   34, 62, 67
app/utils.py                       48      0   100%
-------------------------------------------------------------
TOTAL                             595     16    97%
Coverage XML written to file /backend/tests/test_reports/coverage.xml


============================== 28 passed in 0.74s ==============================

```


---

## Performance Tests
🟢 **Passed**: 18  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 11.62s

### Detailed Output
```
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-8.3.5, pluggy-1.5.0
cachedir: .pytest_cache
benchmark: 4.0.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /backend
configfile: pytest.ini
plugins: cov-6.0.0, asyncio-0.25.3, anyio-4.8.0, langsmith-0.3.15, benchmark-4.0.0
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=function
collecting ... collected 18 items

tests/test_src/test_api_performance.py::test_single_operation_performance PASSED [  5%]
tests/test_src/test_api_performance.py::test_concurrent_operations_performance PASSED [ 11%]
tests/test_src/test_api_performance.py::test_bulk_operations_performance PASSED [ 16%]
tests/test_src/test_api_performance.py::test_user_creation_performance PASSED [ 22%]
tests/test_src/test_api_performance.py::test_user_retrieval_performance PASSED [ 27%]
tests/test_src/test_api_performance.py::test_concurrent_user_creation_performance PASSED [ 33%]
tests/test_src/test_api_performance.py::test_bulk_user_listing_performance PASSED [ 38%]
tests/test_src/test_api_performance.py::test_table_dump_performance PASSED [ 44%]
tests/test_src/test_api_performance.py::test_sequential_operations_performance PASSED [ 50%]
tests/test_src/test_api_performance.py::test_rapid_sequential_reads PASSED [ 55%]
tests/test_src/test_api_performance.py::test_concurrent_reads_performance PASSED [ 61%]
tests/test_src/test_api_performance.py::test_relationship_endpoints_performance PASSED [ 66%]
tests/test_src/test_api_performance.py::test_concurrent_relationship_queries PASSED [ 72%]
tests/test_src/test_api_performance.py::test_order_listing_performance PASSED [ 77%]
tests/test_src/test_api_performance.py::test_order_update_performance PASSED [ 83%]
tests/test_src/test_api_performance.py::test_health_endpoint_performance PASSED [ 88%]
tests/test_src/test_api_performance.py::test_readiness_endpoint_performance PASSED [ 94%]
tests/test_src/test_api_performance.py::test_concurrent_order_operations PASSED [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      7    94%   166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     94      0   100%
app/db/initial_data.py             20      0   100%
app/main.py                        47      0   100%
app/models/order.py                22      0   100%
app/models/user.py                 10      0   100%
app/schemas/base.py                 7      0   100%
app/schemas/order.py               39      2    95%   38, 54
app/schemas/user.py                22      0   100%
app/services/base_service.py       28      0   100%
app/services/order_service.py      50      3    94%   33, 62, 67
app/services/user_service.py       45      3    93%   34, 62, 67
app/utils.py                       48      0   100%
-------------------------------------------------------------
TOTAL                             595     16    97%
Coverage XML written to file /backend/tests/test_reports/coverage.xml



-------------------------------------------------------------------------------------------- benchmark: 9 tests --------------------------------------------------------------------------------------------
Name (time in ms)                               Min                Max               Mean            StdDev             Median               IQR            Outliers       OPS            Rounds  Iterations
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_user_creation_performance               1.3524 (1.0)      16.8387 (7.11)      1.6436 (1.0)      0.7223 (5.04)      1.5874 (1.0)      0.1762 (1.88)         3;25  608.4356 (1.0)         471           1
test_user_retrieval_performance              1.4847 (1.10)      3.0687 (1.30)      1.8476 (1.12)     0.2662 (1.86)      1.7971 (1.13)     0.2447 (2.61)       148;48  541.2518 (0.89)        631           1
test_health_endpoint_performance             1.5975 (1.18)      2.4154 (1.02)      1.7314 (1.05)     0.1502 (1.05)      1.6705 (1.05)     0.0958 (1.02)        62;62  577.5656 (0.95)        538           1
test_readiness_endpoint_performance          1.6077 (1.19)      2.3669 (1.0)       1.7303 (1.05)     0.1434 (1.0)       1.6717 (1.05)     0.0937 (1.0)         48;47  577.9213 (0.95)        450           1
test_order_listing_performance               2.4438 (1.81)      3.7365 (1.58)      2.7244 (1.66)     0.2418 (1.69)      2.6567 (1.67)     0.1899 (2.03)        63;41  367.0599 (0.60)        381           1
test_order_update_performance                2.6471 (1.96)     27.0505 (11.43)     3.0029 (1.83)     1.2900 (9.00)      2.8517 (1.80)     0.2105 (2.25)         1;39  333.0128 (0.55)        364           1
test_relationship_endpoints_performance      9.0742 (6.71)     11.4886 (4.85)     10.1013 (6.15)     0.6217 (4.34)      9.9716 (6.28)     1.0086 (10.76)        35;0   98.9971 (0.16)        100           1
test_bulk_user_listing_performance          56.8458 (42.03)    58.0004 (24.51)    57.4178 (34.94)    0.4065 (2.84)     57.3785 (36.15)    0.8536 (9.10)          9;0   17.4162 (0.03)         18           1
test_table_dump_performance                 57.6419 (42.62)    58.7543 (24.82)    58.0756 (35.34)    0.2572 (1.79)     58.0595 (36.57)    0.2673 (2.85)          5;1   17.2189 (0.03)         18           1
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
============================= 18 passed in 11.62s ==============================

```

### Performance Metrics
| Operation | Min (μs) | Max (μs) | Mean (μs) | OPS |
|-----------|----------|----------|-----------|-----|
| test_user_creation_performance | 1.35 | 16.84 | 1.64 | 0.18 |
| test_user_retrieval_performance | 1.48 | 3.07 | 1.85 | 0.24 |
| test_health_endpoint_performance | 1.60 | 2.42 | 1.73 | 0.10 |
| test_readiness_endpoint_performance | 1.61 | 2.37 | 1.73 | 0.09 |
| test_order_listing_performance | 2.44 | 3.74 | 2.72 | 0.19 |
| test_order_update_performance | 2.65 | 27.05 | 3.00 | 0.21 |
| test_relationship_endpoints_performance | 9.07 | 11.49 | 10.10 | 1.01 |
| test_bulk_user_listing_performance | 56.85 | 58.00 | 57.42 | 0.85 |
| test_table_dump_performance | 57.64 | 58.75 | 58.08 | 0.27 |

---
