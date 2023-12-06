import time
def print_list(list, parse_by_str):
  out = ''
  for i in range(len(list)):
    out = out + str(list[i])
    if i != len(list) - 1:
      out = out + parse_by_str
  print(out)
def list_to_str(list, parse_by_str):
  out = ''
  for i in range(len(list)):
    out = out + str(list[i])
    if i != len(list) - 1:
      out = out + parse_by_str
  return out
def delete_all_from_list(lst, item):
  return [x for x in lst if x != item]
def num_len(num):
  inter1 = str(num)
  inter2 = list(inter1)
  inter3 = delete_all_from_list(inter2, '.')
  inter4 = delete_all_from_list(inter3, '-')
  inter5 = delete_all_from_list(inter4, ',')
  return len(list_to_str(inter5, ''))
def flatten_list(lst):
  return [item for sublist in lst for item in (flatten_list(sublist) if isinstance(sublist, list) else [sublist])]
def item_getter(list, key):
    return [item[key] for item in list]
def transpose(matrix):
  return list(map(list, zip(*matrix)))
def retry(func, attempts=3, delay=1, exceptions=(Exception,)):
    for _ in range(attempts):
        try:
            return func()
        except exceptions as e:
            print(f"Error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise ValueError("Operation failed after multiple attempts")
def make_unique(lst):
  seen = set()
  result = []
  for item in lst:
    if item not in seen:
        result.append(item)
        seen.add(item)
  return result
def make_unique_keep_idx(lst):
  seen = set()
  result = []
  for item in lst:
    if item not in seen:
        result.append(item)
        seen.add(item)
    else:
      result.append("")
  return result
def merge_dicts(dict1, dict2):
    return {**dict1, **dict2}
def print_dict(dict, parse_by_str):
  last_key = list(dict.keys())[-1]
  for key in dict:
    if key != last_key:
      print(dict[key], end=parse_by_str)
    else:
      print(dict[key], end="")
def dict_to_list(dict):
  out = []
  for key in dict:
    out.append(dict[key])
  return out
def dict_to_str(dict, parse_by_str):
  return list_to_str(dict_to_list(dict), parse_by_str)