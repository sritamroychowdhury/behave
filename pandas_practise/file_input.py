from datetime import datetime
import re
import pandas as pd


#IntegriChain_Alexion_Koselugo_Daily_Status_lastweek.csv
#IntegriChain_Alexion_Koselugo_Daily_Status_latest.csv
#Koselugo_status.csv

def column_name_match(file1, file2):
    columnname_lastweek = file1.axes[1]
    columnname_latest = file2.axes[1]
    mismatch1 = [i for i in columnname_latest if i not in columnname_lastweek]
    mismatch2 = [i for i in columnname_lastweek if i not in columnname_latest]
    mismatched = mismatch1+mismatch2
    return mismatched


def row_count(file1, file2):
    columcount_latest = len(file1)
    columncount_lastweek = len(file2)
    count = columcount_latest - columncount_lastweek
    return count


def field_name_match(file1, file2):
    fieldname = file2["Field Name"].tolist()
    columnname_extract = file1.axes[1]
    a = [i for i in columnname_extract if i not in fieldname]
    return a



def field_format_match(file1, file2):
  extract_df = file1
  config_df = file2
  config_df = config_df.loc[0::, ['Field Name', 'Field Format']]
  config_df = config_df.dropna()
  dict_df = config_df.set_index('Field Name')['Field Format'].to_dict()
  dict_df.pop("SHIP_DATE")
  pass_list = []

  def validate_fieldformat(pattern, test_str):

      # initializing format
      if pattern == "YYYY":
          format = "%Y"
          if bool(datetime.strptime(str(test_str), format)):
              return True
          else:
              return False

      elif pattern == "YYYYMMDD":
          format = "%Y%m%d"
          if bool(datetime.strptime(str(test_str), format)):
              return True
          else:
              return False

      elif pattern == "YYYYMMDDHHMMSS":
          format = "%Y%m%d%H%M%S"
          if bool(datetime.strptime(str(test_str), format)):
              return True
          else:
              return False

      elif pattern == "YYYYMMDD HH:MM:SS":
          format = "%Y%m%d %H:%M:%S"
          if bool(datetime.strptime(str(test_str), format)):
              return True
          else:
              return False

      elif pattern == "2 chars":
          my_reg_exp = "^[a-zA-Z]{2}$"
          if re.match(my_reg_exp, test_str):
              return True
          else:
              print(False)

      elif pattern == "3 digits":
          my_reg_exp = "^[0-9]{3}$"
          if re.match(my_reg_exp, test_str):
              return True
          else:
              return False

      elif pattern == "No dashes":
          my_reg_exp = "[-]"
          if re.search(my_reg_exp, test_str):
              return False
          else:
              return True


  for key in dict_df.keys():
    for row in extract_df[key]:
      if pd.isnull(row):
        continue
      else:
        format = dict_df[key]
        if format == "YYYYMMDD HH:MM:SS":
          pass_list.append(validate_fieldformat(format, row))
        else:
          pass_list.append(validate_fieldformat(format, int(row)))
  for i in pass_list:
    if i == False:
      return False
    else:
      return True



def datatype_match(file1, file2):
  config_df = file2
  extract = file1

  config_df = config_df.loc[0::, ['Field Name', 'Data Type']]
  config_df = config_df.dropna()
  dict_df = config_df.set_index('Field Name')['Data Type'].to_dict()
  dict_df.pop("SHIP_DATE")
  extract["REFERRAL_DATE"] = extract["REFERRAL_DATE"].astype('Int64')
  extract["PATIENT_CONSENT_DATE"] = extract["PATIENT_CONSENT_DATE"].astype('Int64')

  pass_lst = []
  for key in dict_df.keys():
      dict_df[key] = re.sub("\(.*?\)", "", dict_df[key])


  def datatype_match(pattern, test_str):

      if pattern == "DATE":
        format = "%Y%m%d"
        if bool(datetime.strptime(str(test_str), format)):
          return True
        else:
          return False

      elif pattern == "TIMESTAMP":
        format = "%Y%m%d %H:%M:%S"
        if bool(datetime.strptime(str(test_str), format)):
          return True
        else:
          return False


      elif pattern == "VARCHAR":
        if isinstance(test_str,str) or isinstance(test_str,int):
          return True
        else:
          return False


      elif pattern == "NUMERIC":
        if isinstance(test_str,float):
            return True
        else:
          return False


      elif pattern == "INTEGER":
        if isinstance(test_str,int):
          return True
        else:
          return False



  for key in dict_df.keys():
    if key not in extract.columns:
      continue
    else:
      for row in extract[key]:
        format = dict_df[key]
        if pd.isnull(row) or pd.isna(row):
          continue
        else:
          pass_lst.append(datatype_match(format, row))
  i = False
  if i in pass_lst:
    return False
  else:
    return True
  return pass_lst


def expected_values_match(file1, file2):
    config_df = file2
    extract = file1
    config_df = config_df.loc[0::, ['Field Name', 'Expected Value/s (comma separated)']]
    config_df = config_df.dropna()
    dict_df = config_df.set_index('Field Name')['Expected Value/s (comma separated)'].to_dict()
    pass_lst = []

    for key in dict_df.keys():
        if key not in extract.columns:
            continue
        else:
            for row in extract[key]:
                if pd.isnull(row):
                    continue
                elif row in dict_df[key]:
                    pass_lst.append(True)

    i = False
    if i in pass_lst:
        return False
    else:
        return True
    return pass_lst
