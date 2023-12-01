import os
import sys
import unittest



class Testing_tyro(unittest.TestCase):
  
  def test_overriding_yaml_configs(self, debug=True):
    """
    Usage:

        export CUDA_VISIBLE_DEVICES=0
        export PORT=12345
        export TIME_STR=0
        export PYTHONPATH=.
        python -c "from tl2.proj.tyro.tests.test_tyro import Testing_tyro;\
          Testing_tyro().test_overriding_yaml_configs(debug=False)" \
          --training.checkpoint-steps 1 2 3

    :return:
    """
    if 'CUDA_VISIBLE_DEVICES' not in os.environ:
      os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    if 'TIME_STR' not in os.environ:
      os.environ['TIME_STR'] = '0'
    if 'RUN_NUM' not in os.environ:
      os.environ['RUN_NUM'] = '0'
    from tl2 import tl2_utils
    from tl2.launch.launch_utils import \
      (get_command_and_outdir, setup_outdir_and_yaml, get_append_cmd_str, start_cmd_run)
    
    # command, outdir = get_command_and_outdir(self, func_name=sys._getframe().f_code.co_name, file=__file__)
    
    import yaml
    import tyro
    import pprint
    from tl2.proj.tyro import tyro_utils
    
    cfg_path = "tl2/proj/tyro/configs/test.yml"
    
    # with open(cfg_path, 'r') as f:
    #   cfg = yaml.safe_load(f)
    #
    # cfg_overridden = tyro.cli(dict, default=cfg)
    
    cfg = tyro_utils.parse_cfg_from_yaml_cli(cfg_path)
    
    pprint.pprint(cfg)
    
    pass














