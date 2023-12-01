"""
@st.cache(allow_output_mutation=True, suppress_st_warning=True)

@st.cache_data
def long_running_function(param1, param2):
    return …
cache computations that return data
    
@st.cache_resource
cache global resources like ML models

"""
import numpy as np
from PIL import Image
from pathlib import Path
import logging
import json
import ast
import streamlit as st
import pandas as pd


from tl2.tl2_utils import read_image_list_from_files, get_tempfile

from . import SessionState
from ..pil.pil_utils import imshow_pil, pil_save

def is_init():
  try:
    saved_suffix_state = SessionState.get(saved_suffix=0)
  except:
    return False
  return True


def st_set_sep(msg="", num_symbol=6, sidebar=True):
  if sidebar:
    st.sidebar.write(f'{"<"*num_symbol} {msg} {">"*num_symbol}')
  else:
    st.write(f'{"<"*num_symbol} {msg} {">"*num_symbol}')

def split_key_value(k_v_str):
  k, v = k_v_str.split(':')
  v = v.strip()
  return k, v

def get_seed(seeds):
  seed = selectbox('seeds', seeds, sidebar=True)
  use_seed = checkbox('use_seed', True, sidebar=True)
  if not use_seed:
    seed = np.random.randint(10000000)
  seed = number_input('selected_seed', seed, sidebar=True)
  return seed


def st_image(
      img_pil,
      caption=None,
      width=None,
      use_column_width=None,
      clamp=False,
      debug=False,
      outdir=None,
      st_empty=None):
  if st_empty:
    st_empty.image(image=img_pil, caption=caption, width=width, use_column_width=use_column_width, clamp=clamp)
  else:
    st.image(image=img_pil, caption=caption, width=width, use_column_width=use_column_width, clamp=clamp)
  if outdir:
    saved_path = caption.replace(' ', '_')
    saved_path = f"{outdir}/{saved_path}.png"
    pil_save(img_pil, image_path=saved_path)
    st.write(saved_path)
  if debug:
    imshow_pil(img_pil, title=caption)
  pass

def radio(label,
          options,
          index=0,
          default_value=None,
          sidebar=False,
          value_dict=None):
  options = list(options)
  if default_value is not None:
    index = options.index(default_value)

  if sidebar:
    ret = st.sidebar.radio(label=label, options=list(options), index=index)
  else:
    ret = st.radio(label=label, options=list(options), index=index)

  if value_dict is not None:
    ret = value_dict[ret]
    st.sidebar.write(f"{label}={ret}")

  logging.getLogger('st').info(f"{label}={ret}")
  print(f"{label}={ret}")
  return ret



class LineChart_deprecated(object):
  def __init__(self, x_label, y_label):
    self.x_label = x_label
    self.y_label = y_label

    self.pd_data = pd.DataFrame(columns=[x_label, y_label])
    self.st_line_chart = st.empty()
    self.st_init = is_init()
    pass

  def write(self, x, y):
    if not self.st_init:
      return
    self.pd_data = self.pd_data.append({self.x_label: x, self.y_label: y}, ignore_index=True)
    pd_data = self.pd_data.set_index(self.x_label)
    self.st_line_chart.line_chart(pd_data)
    pass


class LineChart(object):
  def __init__(self, x_label, y_label):
    self.x_label = x_label
    self.y_label = y_label

    # self.pd_data = pd.DataFrame(columns=[x_label, y_label])
    self.st_line_chart = st.line_chart()
    self.st_init = is_init()
    pass

  def write(self, x, y):
    # if not self.st_init:
    #   return
    data = {self.x_label: [x], self.y_label: [y]}
    pd_data = pd.DataFrame(data=data).set_index(self.x_label)

    # self.pd_data = self.pd_data.append(data, ignore_index=True)
    # pd_data = pd_data.set_index(self.x_label)

    # data = np.array([[x, y]])
    self.st_line_chart.add_rows(pd_data)
    pass


def multiselect(label, options, default=None, sidebar=False):
  if sidebar:
    ret = st.sidebar.multiselect(label=label, options=options, default=default)
  else:
    ret = st.multiselect(label=label, options=options, default=default)
  logging.getLogger('st').info(f"{label}={ret}")
  print(f"{label}={ret}")
  return ret


def selectbox(label,
              options,
              index=0,
              default_value=None,
              value_dict=None,
              sidebar=False):
  options = list(options)
  if default_value is not None:
    index = options.index(default_value)
  if sidebar:
    ret = st.sidebar.selectbox(label=label, options=options, index=index)
  else:
    ret = st.selectbox(label=label, options=options, index=index)

  if value_dict is not None:
    value_dict = dict(value_dict)
    ret = value_dict[ret]
    if sidebar:
      st.sidebar.write(f"{label}={ret}")

  logging.getLogger('st').info(f"{label}={ret}")
  # st.write(f"{label}={ret}")
  print(f"{label}={ret}")
  return ret

def selectbox_v1(label,
                 options_dict,
                 default_key,
                 sidebar=False,
                 ret_key_value=False,
                 verbose=True):
  options_dict = dict(options_dict)

  options_keys = list(options_dict.keys())
  index = options_keys.index(default_key)
  if sidebar:
    ret_key = st.sidebar.selectbox(label=label, options=options_keys, index=index)
  else:
    ret_key = st.selectbox(label=label, options=options_keys, index=index)

  ret = options_dict[ret_key]

  logging.getLogger('st').info(f"{label}={ret}")
  if verbose:
    if sidebar:
      st.sidebar.write(f"{ret_key}={ret}")
    else:
      st.write(f"{label}={ret}")
  print(f"{label}={ret}")

  if ret_key_value:
    return ret_key, ret
  else:
    return ret

def number_input(label,
                 value,
                 min_value=None,
                 step=None,
                 format=None, # "%.8f"
                 sidebar=False,
                 **kwargs):
  if sidebar:
    st_empty = st.sidebar.empty()
  else:
    st_empty = st.empty()
  ret = st_empty.number_input(label=f"{label}: {value}", value=value, min_value=min_value,
                              step=step, format=format, **kwargs)
  logging.getLogger('st').info(f"{label}={ret}")
  print(f"{label}={ret}")
  return ret


def checkbox(label, value, sidebar=True):
  if sidebar:
    st_empty = st.sidebar.empty()
  else:
    st_empty = st.empty()
  ret = st_empty.checkbox(label=f"{label}: {value}", value=value)
  logging.getLogger('st').info(f"{label}={ret}")
  print(f"{label}={ret}")
  return ret


def text_input(label,
               value,
               sidebar=False,
               **kwargs):
  if sidebar:
    ret = st.sidebar.text_input(label=f"{label}: {value}", value=value, key=label)
  else:
    ret = st.text_input(label=f"{label}: {value}", value=value, key=label)
  logging.getLogger('st').info(f"{label}={ret}")
  print(f"{label}={ret}")
  return ret


def parse_list_from_st_text_input(label, value, sidebar=False):
  """
  return: list
  """
  value = str(value)
  if sidebar:
    st_text_input = st.sidebar.empty()
  else:
    st_text_input = st.empty()
  st_value = st_text_input.text_input(label=f"{label}: {value}", value=value, key=label)

  parsed_value = ast.literal_eval(st_value)
  print(f"{label}: {parsed_value}")
  logging.getLogger('st').info(f"label: {parsed_value}")
  return parsed_value





def st_show_image(image_path,
                  width=None):
  image_pil = Image.open(image_path)
  st.image(image_pil, caption=f"{image_path.name, image_pil.size}", width=width)
  st.write(f"{image_path}")
  pass




def parse_dict_from_st_text_input(label, value):
  to_list = False
  if isinstance(value, list):
    value = {str(k): v for k, v in enumerate(value)}
    to_list = True

  if isinstance(value, dict):
    value = json.dumps(value)
  st_text_input = st.empty()
  st_value = st_text_input.text_input(label=f"{label}: {value}", value=value, key=label)
  parse_value = json.loads(st_value)
  print(f"{label}: {parse_value}")
  logging.getLogger('st').info(f"label: {parse_value}")
  if to_list:
    parse_value = list(parse_value.values())
    print(f"{label}={parse_value}")
  return parse_value


def v_spacer(height,
             sb=False) -> None:
  for _ in range(height):
    if sb:
      st.sidebar.write('\n')
    else:
      st.write('\n')
  st.markdown("***")
  pass

def read_image_list_and_show_in_st(image_list_file,
                                   columns=['path'],
                                   show_dataframe=True):
  if not isinstance(image_list_file, (list, tuple)):
    image_list_file = [image_list_file, ]

  all_image_list = read_image_list_from_files(image_list_file)

  return all_image_list

def parse_image_list_from_dir(image_dir,
                              default_index=0,
                              header="Input image",
                              columns=['path', ],
                              image_root=None):
  """

  :param image_dir: dir, image_list_file, or list
  :param header:
  :param columns:
  :param default_index:
  :param image_root:
  :return:
  """
  with st.expander(header, expanded=True):
    st_left_col, st_right_col = st.columns(2)

    image_list = read_image_list_and_show_in_st(image_list_file=image_dir,
                                                columns=columns,
                                                show_dataframe=True)

    with st_left_col:
      image_list_df = pd.DataFrame(image_list, columns=columns)
      st.dataframe(image_list_df, height=200)

      default_index = st.number_input(f"Image idx: (0~{len(image_list) - 1})",
                                      value=default_index,
                                      min_value=0,
                                      max_value=len(image_list) - 1,
                                      key=header)
      file = st.file_uploader("Upload your own:")

    default_index = int(default_index)
    image_path = image_list[default_index][0]
    if image_root is not None:
      image_path = f"{image_root}/{image_path}"
    image_path = Path(image_path)

    if file:
      raw_img = Image.open(file).convert("RGB")
      temp_file = get_tempfile()
      image_path = Path(f"{temp_file}.png")
      raw_img.save(str(image_path))


    with st_right_col:
      st_show_image(image_path)

  return image_path



