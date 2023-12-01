import numpy as np
from pathlib import Path
import logging
import os
import sys
from PIL import Image
import streamlit as st

import torch

from tl2.launch.launch_utils import update_parser_defaults_from_yaml, global_cfg
from tl2.proj.streamlit import st_utils
from tl2.proj.logger.logger_utils import get_file_logger
from tl2 import tl2_utils
from tl2.proj.streamlit import st_utils
from tl2.proj.fvcore import build_model
from tl2.proj.cv2 import cv2_utils
from tl2.proj.pil import pil_utils

sys.path.insert(0, os.getcwd())
# sys.path.insert(0, f"{os.getcwd()}/DGP_lib")
# from DGP_lib import utils
# sys.path.pop(0)


# @MODEL_REGISTRY.register(name_prefix=__name__)
class STModel(object):
  def __init__(self):
    # turn on page wide mode
    st.set_page_config(layout="wide")
    
    # outdir
    if not global_cfg.tl_debug:
      session_state = st.session_state
      
      if 'saved_suffix' not in session_state:
        session_state['saved_suffix'] = 0
        
      saved_suffix = int(session_state.saved_suffix)
    else:
      saved_suffix = 0
  
    outdir = f"{global_cfg.tl_outdir}/exp/{saved_suffix:04d}"
    os.makedirs(outdir, exist_ok=True)
    self.outdir = outdir
    st.sidebar.markdown(f"# Outdir: ")
    st.sidebar.write(outdir)
  
    get_file_logger(filename=f"{outdir}/log.txt", logger_names=['st'])
    logger = logging.getLogger('st')
    logger.info(f"global_cfg:\n {global_cfg.dump()}")
    
    pass

  def st_two_column(self,
                    cfg,
                    **kwargs):
  
    st_left_col, st_right_col = st.columns(2)
    
    with st_right_col:
      img_path = st_utils.parse_image_list(cfg.train_list_file,
                                           header="train list: ",
                                           default_index=0,
                                           show_image=True)



    
    if not global_cfg.tl_debug:
      if not st.sidebar.button("run_web"):
        return
      st.session_state.saved_suffix += 1
    
    
    
    pass


def main():

  update_parser_defaults_from_yaml(parser=None)

  st_model = STModel()
  
  if 'default_mode' in global_cfg:
    mode = st_utils.radio("Mode: ", global_cfg.mode, default_value=global_cfg.default_mode, sidebar=True)
  else:
    mode = st_utils.radio("Mode: ", global_cfg.mode, sidebar=True)
  
  getattr(st_model, mode)(cfg=global_cfg.get(mode, {}))

  pass

if __name__ == '__main__':
  main()
