# Test Results Report

Generated: 2025-03-22 21:36:50  

Python Version: 3.11.9

## Overall Summary
### Total Results
🟢 **Total Passed**: 110  
🔴 **Total Failed**: 0  
🟡 **Total Errors**: 0  
⏱️ **Total Time**: 16.17s

### Results by Category
| Category | Description | Passed | Failed | Errors | Time (s) |
|----------|-------------|--------:|--------:|--------:|---------:|
| **Config** | Configuration and environment setup tests | ✓ 1 | ✗ 0 | ! 0 | 0.38 |
| **Models** | Data model validation and schema tests | ✓ 8 | ✗ 0 | ! 0 | 0.46 |
| **Utils** | Utility function and helper method tests | ✓ 10 | ✗ 0 | ! 0 | 0.27 |
| **Database** | In-memory database operations and data persistence tests | ✓ 8 | ✗ 0 | ! 0 | 0.47 |
| **Api Main** | Core API functionality and endpoint tests | ✓ 5 | ✗ 0 | ! 0 | 0.59 |
| **Api Utils** | API utility functions and middleware tests | ✓ 6 | ✗ 0 | ! 0 | 0.53 |
| **Services** | Business logic and service layer tests | ✓ 7 | ✗ 0 | ! 0 | 0.55 |
| **Normal** | Standard use case and happy path tests | ✓ 19 | ✗ 0 | ! 0 | 0.85 |
| **Edge** | Edge cases, error handling, and boundary condition tests | ✓ 28 | ✗ 0 | ! 0 | 0.80 |
| **Performance** | Performance benchmarks and load testing | ✓ 18 | ✗ 0 | ! 0 | 11.27 |

## Coverage Summary
📊 **Overall Coverage**: 96.79%  
📝 **Total Statements**: 560  
❌ **Missing Statements**: 18

### Coverage by File
| File | Coverage % | Statements | Missing |
|------|------------|------------|---------|
| main.py | 100.00% | 47 | 0 |
| utils.py | 100.00% | 48 | 0 |
| api/deps.py | 100.00% | 13 | 0 |
| api/main.py | 100.00% | 6 | 0 |
| api/v1/tables.py | 92.68% | 123 | 9 |
| api/v1/utils.py | 88.89% | 9 | 1 |
| core/config.py | 100.00% | 12 | 0 |
| db/base.py | 100.00% | 59 | 0 |
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
⏱ **Time**: 0.38s

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

tests/test_config.py::test_settings_defaults PASSED                      [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      9    93%   47-48, 166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     59      0   100%
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
TOTAL                             560     18    97%


============================== 1 passed in 0.38s ===============================

```


---

## Models Tests
🟢 **Passed**: 8  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.46s

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

tests/test_models.py::test_user_model_creation PASSED                    [ 12%]
tests/test_models.py::test_user_model_validation PASSED                  [ 25%]
tests/test_models.py::test_user_model_required_fields PASSED             [ 37%]
tests/test_models.py::test_order_model_creation PASSED                   [ 50%]
tests/test_models.py::test_order_model_validation PASSED                 [ 62%]
tests/test_models.py::test_order_model_required_fields PASSED            [ 75%]
tests/test_models.py::test_order_status_transitions PASSED               [ 87%]
tests/test_models.py::test_user_order_model PASSED                       [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      9    93%   47-48, 166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     59      0   100%
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
TOTAL                             560     18    97%


============================== 8 passed in 0.46s ===============================

```


---

## Utils Tests
🟢 **Passed**: 10  
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
collecting ... collected 10 items

tests/test_utils.py::test_datetime_formatting PASSED                     [ 10%]
tests/test_utils.py::test_uuid_parsing PASSED                            [ 20%]
tests/test_utils.py::test_generate_record_id PASSED                      [ 30%]
tests/test_utils.py::test_table_name_validation PASSED                   [ 40%]
tests/test_utils.py::test_record_data_validation PASSED                  [ 50%]
tests/test_utils.py::test_validate_join_key PASSED                       [ 60%]
tests/test_utils.py::test_error_response_formatting PASSED               [ 70%]
tests/test_utils.py::test_success_response_formatting PASSED             [ 80%]
tests/test_utils.py::test_record_id_validation PASSED                    [ 90%]
tests/test_utils.py::test_join_operations PASSED                         [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      9    93%   47-48, 166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     59      0   100%
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
TOTAL                             560     18    97%


============================== 10 passed in 0.27s ==============================

```


---

## Database Tests
🟢 **Passed**: 8  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.47s

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

tests/test_db.py::test_db_initialization PASSED                          [ 12%]
tests/test_db.py::test_db_crud_operations PASSED                         [ 25%]
tests/test_db.py::test_db_error_handling PASSED                          [ 37%]
tests/test_db.py::test_db_concurrent_operations PASSED                   [ 50%]
tests/test_db.py::test_db_table_operations PASSED                        [ 62%]
tests/test_db.py::test_db_relationships PASSED                           [ 75%]
tests/test_db.py::test_db_sample_data PASSED                             [ 87%]
tests/test_db.py::test_db_transaction_safety PASSED                      [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      9    93%   47-48, 166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     59      0   100%
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
TOTAL                             560     18    97%


============================== 8 passed in 0.47s ===============================

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

tests/test_api_main.py::test_root PASSED                                 [ 20%]
tests/test_api_main.py::test_cors_middleware PASSED                      [ 40%]
tests/test_api_main.py::test_database_error_handler PASSED               [ 60%]
tests/test_api_main.py::test_general_exception_handler PASSED            [ 80%]
tests/test_api_main.py::test_lifespan PASSED                             [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      9    93%   47-48, 166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     59      0   100%
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
TOTAL                             560     18    97%


============================== 5 passed in 0.59s ===============================

```


---

## Api_Utils Tests
🟢 **Passed**: 6  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.53s

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

tests/test_api_utils.py::test_health_check PASSED                        [ 16%]
tests/test_api_utils.py::test_health_check_method_not_allowed PASSED     [ 33%]
tests/test_api_utils.py::test_router_prefix PASSED                       [ 50%]
tests/test_api_utils.py::test_router_routes PASSED                       [ 66%]
tests/test_api_utils.py::test_health_check_in_main_app PASSED            [ 83%]
tests/test_api_utils.py::test_health_check_integration PASSED            [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      9    93%   47-48, 166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     59      0   100%
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
TOTAL                             560     18    97%


============================== 6 passed in 0.53s ===============================

```


---

## Services Tests
🟢 **Passed**: 7  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.55s

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

tests/test_services.py::test_base_service_initialization PASSED          [ 14%]
tests/test_services.py::test_base_service_create PASSED                  [ 28%]
tests/test_services.py::test_base_service_get PASSED                     [ 42%]
tests/test_services.py::test_base_service_update PASSED                  [ 57%]
tests/test_services.py::test_base_service_delete PASSED                  [ 71%]
tests/test_services.py::test_base_service_list PASSED                    [ 85%]
tests/test_services.py::test_base_service_exists PASSED                  [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      9    93%   47-48, 166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     59      0   100%
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
TOTAL                             560     18    97%


============================== 7 passed in 0.55s ===============================

```


---

## Normal Tests
🟢 **Passed**: 19  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.85s

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

tests/test_api_normal.py::test_create_user PASSED                        [  5%]
tests/test_api_normal.py::test_create_order PASSED                       [ 10%]
tests/test_api_normal.py::test_get_user PASSED                           [ 15%]
tests/test_api_normal.py::test_update_user_variations[test_case0] PASSED [ 21%]
tests/test_api_normal.py::test_update_user_variations[test_case1] PASSED [ 26%]
tests/test_api_normal.py::test_update_user_variations[test_case2] PASSED [ 31%]
tests/test_api_normal.py::test_delete_user PASSED                        [ 36%]
tests/test_api_normal.py::test_list_users PASSED                         [ 42%]
tests/test_api_normal.py::test_get_user_orders PASSED                    [ 47%]
tests/test_api_normal.py::test_get_order_user PASSED                     [ 52%]
tests/test_api_normal.py::test_dump_table PASSED                         [ 57%]
tests/test_api_normal.py::test_list_orders PASSED                        [ 63%]
tests/test_api_normal.py::test_update_order_variations[test_case0] PASSED [ 68%]
tests/test_api_normal.py::test_update_order_variations[test_case1] PASSED [ 73%]
tests/test_api_normal.py::test_update_order_variations[test_case2] PASSED [ 78%]
tests/test_api_normal.py::test_update_order_variations[test_case3] PASSED [ 84%]
tests/test_api_normal.py::test_delete_order PASSED                       [ 89%]
tests/test_api_normal.py::test_health_check PASSED                       [ 94%]
tests/test_api_normal.py::test_readiness_check PASSED                    [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      9    93%   47-48, 166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     59      0   100%
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
TOTAL                             560     18    97%


============================== 19 passed in 0.85s ==============================

```


---

## Edge Tests
🟢 **Passed**: 28  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 0.80s

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

tests/test_api_edge_cases.py::test_create_user_invalid_data PASSED       [  3%]
tests/test_api_edge_cases.py::test_get_user_invalid_uuid PASSED          [  7%]
tests/test_api_edge_cases.py::test_get_nonexistent_user PASSED           [ 10%]
tests/test_api_edge_cases.py::test_update_user_invalid_uuid PASSED       [ 14%]
tests/test_api_edge_cases.py::test_update_nonexistent_user PASSED        [ 17%]
tests/test_api_edge_cases.py::test_delete_user_invalid_uuid PASSED       [ 21%]
tests/test_api_edge_cases.py::test_delete_nonexistent_user PASSED        [ 25%]
tests/test_api_edge_cases.py::test_get_orders_invalid_user_uuid PASSED   [ 28%]
tests/test_api_edge_cases.py::test_get_orders_nonexistent_user PASSED    [ 32%]
tests/test_api_edge_cases.py::test_get_order_user_invalid_uuid PASSED    [ 35%]
tests/test_api_edge_cases.py::test_get_order_user_nonexistent_order PASSED [ 39%]
tests/test_api_edge_cases.py::test_dump_nonexistent_table PASSED         [ 42%]
tests/test_api_edge_cases.py::test_verify_deleted_user PASSED            [ 46%]
tests/test_api_edge_cases.py::test_create_user_empty_values PASSED       [ 50%]
tests/test_api_edge_cases.py::test_create_user_special_characters PASSED [ 53%]
tests/test_api_edge_cases.py::test_concurrent_user_updates PASSED        [ 57%]
tests/test_api_edge_cases.py::test_order_with_deleted_user PASSED        [ 60%]
tests/test_api_edge_cases.py::test_boundary_values PASSED                [ 64%]
tests/test_api_edge_cases.py::test_update_order_invalid_uuid PASSED      [ 67%]
tests/test_api_edge_cases.py::test_update_nonexistent_order PASSED       [ 71%]
tests/test_api_edge_cases.py::test_update_order_invalid_status PASSED    [ 75%]
tests/test_api_edge_cases.py::test_update_order_invalid_amount PASSED    [ 78%]
tests/test_api_edge_cases.py::test_delete_order_invalid_uuid PASSED      [ 82%]
tests/test_api_edge_cases.py::test_delete_nonexistent_order PASSED       [ 85%]
tests/test_api_edge_cases.py::test_health_check_edge_cases PASSED        [ 89%]
tests/test_api_edge_cases.py::test_readiness_check_edge_cases PASSED     [ 92%]
tests/test_api_edge_cases.py::test_dump_table_invalid_format PASSED      [ 96%]
tests/test_api_edge_cases.py::test_dump_table_concurrent_access PASSED   [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      9    93%   47-48, 166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     59      0   100%
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
TOTAL                             560     18    97%


============================== 28 passed in 0.80s ==============================

```


---

## Performance Tests
🟢 **Passed**: 18  
🔴 **Failed**: 0  
🟡 **Errors**: 0  
⏱ **Time**: 11.27s

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

tests/test_api_performance.py::test_single_operation_performance PASSED  [  5%]
tests/test_api_performance.py::test_concurrent_operations_performance PASSED [ 11%]
tests/test_api_performance.py::test_bulk_operations_performance PASSED   [ 16%]
tests/test_api_performance.py::test_user_creation_performance PASSED     [ 22%]
tests/test_api_performance.py::test_user_retrieval_performance PASSED    [ 27%]
tests/test_api_performance.py::test_concurrent_user_creation_performance PASSED [ 33%]
tests/test_api_performance.py::test_bulk_user_listing_performance PASSED [ 38%]
tests/test_api_performance.py::test_table_dump_performance PASSED        [ 44%]
tests/test_api_performance.py::test_sequential_operations_performance PASSED [ 50%]
tests/test_api_performance.py::test_rapid_sequential_reads PASSED        [ 55%]
tests/test_api_performance.py::test_concurrent_reads_performance PASSED  [ 61%]
tests/test_api_performance.py::test_relationship_endpoints_performance PASSED [ 66%]
tests/test_api_performance.py::test_concurrent_relationship_queries PASSED [ 72%]
tests/test_api_performance.py::test_order_listing_performance PASSED     [ 77%]
tests/test_api_performance.py::test_order_update_performance PASSED      [ 83%]
tests/test_api_performance.py::test_health_endpoint_performance PASSED   [ 88%]
tests/test_api_performance.py::test_readiness_endpoint_performance PASSED [ 94%]
tests/test_api_performance.py::test_concurrent_order_operations PASSED   [100%]

---------- coverage: platform darwin, python 3.11.9-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/api/deps.py                    13      0   100%
app/api/main.py                     6      0   100%
app/api/v1/tables.py              123      9    93%   47-48, 166-167, 409-413
app/api/v1/utils.py                 9      1    89%   19
app/core/config.py                 12      0   100%
app/db/base.py                     59      0   100%
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
TOTAL                             560     18    97%



--------------------------------------------------------------------------------------------- benchmark: 9 tests ---------------------------------------------------------------------------------------------
Name (time in ms)                               Min                 Max               Mean             StdDev             Median               IQR            Outliers       OPS            Rounds  Iterations
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_user_creation_performance               1.3273 (1.0)       16.9424 (6.98)      1.6514 (1.0)       0.7322 (5.27)      1.5980 (1.0)      0.1602 (2.46)         5;37  605.5501 (1.0)         468           1
test_user_retrieval_performance              1.4745 (1.11)       7.6520 (3.15)      1.8374 (1.11)      0.3580 (2.58)      1.7939 (1.12)     0.2489 (3.82)        36;25  544.2485 (0.90)        612           1
test_readiness_endpoint_performance          1.6003 (1.21)       2.4266 (1.0)       1.7191 (1.04)      0.1389 (1.0)       1.6632 (1.04)     0.0651 (1.0)         70;83  581.6923 (0.96)        547           1
test_health_endpoint_performance             1.6013 (1.21)       2.8061 (1.16)      1.7272 (1.05)      0.1531 (1.10)      1.6659 (1.04)     0.0914 (1.40)        59;63  578.9609 (0.96)        498           1
test_order_listing_performance               2.4988 (1.88)       3.6903 (1.52)      2.7700 (1.68)      0.2167 (1.56)      2.6907 (1.68)     0.2058 (3.16)        58;26  361.0084 (0.60)        315           1
test_order_update_performance                2.6437 (1.99)       3.8233 (1.58)      2.9142 (1.76)      0.2205 (1.59)      2.8391 (1.78)     0.2097 (3.22)        55;23  343.1510 (0.57)        305           1
test_relationship_endpoints_performance      9.2080 (6.94)      13.7209 (5.65)     10.3331 (6.26)      0.7981 (5.75)     10.1686 (6.36)     0.9106 (13.99)        30;4   96.7763 (0.16)        106           1
test_bulk_user_listing_performance          56.5263 (42.59)     58.6359 (24.16)    57.4716 (34.80)     0.6019 (4.33)     57.4572 (35.96)    0.6788 (10.43)         5;0   17.3999 (0.03)         13           1
test_table_dump_performance                 57.1334 (43.05)    103.5403 (42.67)    63.0061 (38.15)    12.8260 (92.36)    58.2680 (36.46)    2.2115 (33.97)         2;2   15.8715 (0.03)         18           1
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
============================= 18 passed in 11.27s ==============================

```

### Performance Metrics
| Operation | Min (μs) | Max (μs) | Mean (μs) | OPS |
|-----------|----------|----------|-----------|-----|
| test_user_creation_performance | 1.33 | 16.94 | 1.65 | 0.16 |
| test_user_retrieval_performance | 1.47 | 7.65 | 1.84 | 0.25 |
| test_readiness_endpoint_performance | 1.60 | 2.43 | 1.72 | 0.07 |
| test_health_endpoint_performance | 1.60 | 2.81 | 1.73 | 0.09 |
| test_order_listing_performance | 2.50 | 3.69 | 2.77 | 0.21 |
| test_order_update_performance | 2.64 | 3.82 | 2.91 | 0.21 |
| test_relationship_endpoints_performance | 9.21 | 13.72 | 10.33 | 0.91 |
| test_bulk_user_listing_performance | 56.53 | 58.64 | 57.47 | 0.68 |
| test_table_dump_performance | 57.13 | 103.54 | 63.01 | 2.21 |

---
