# import pytest
# import subprocess as sp
# import os
# import yaml




# config = yaml.safe_load(open(config_path, encoding='utf-8'))
# config_backup = config

# config_backup = None

# @pytest.fixture
# def setup_test_config():

#     src_path = str(os.path.dirname(__file__))
#     buffer_path = str(os.path.join(src_path, '../buffer'))
#     config_path = str(os.path.join(src_path, '../config.yaml'))
#     log_path = str(os.path.join(src_path, '../logs'))
#     config = yaml.safe_load(open(config_path, encoding='utf-8'))
#     config_backup = config

    

#     #speichere änderungen an der yaml
#     with open(config_path, 'w', encoding='utf-8') as file:
#         # Load the YAML data into a Python dictionary
#         yaml.dump(config, file, default_flow_style=False, encoding='utf-8', allow_unicode=True, Dumper=yaml.SafeDumper)


# def capital_case(x):
#     process = sp.Popen(['python', os.path.join(src_path, 'sensor_data_generator.py') ])
#     return x.capitalize()

# def test_capital_case():
#     assert capital_case('semaphore') == 'Semaphore'

# def test_raises_exception_on_non_string_arguments():
#     with pytest.raises(TypeError):
#         capital_case(9)