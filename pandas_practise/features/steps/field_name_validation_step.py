from behave import given, when, then
import pandas as pd
from file_input import field_name_match


@given(u'extract file input')
def step_impl(context):
    context.df1 = pd.read_csv("IntegriChain_Alexion_Koselugo_Daily_Status_latest.csv")


@given(u'config csv file input')
def step_impl(context):
    context.df3 = pd.read_csv("Koselugo_status.csv")


@when(u'field names of the extract file is compared with config file')
def step_impl(context):
    context.result = field_name_match(context.df1, context.df3)


@then(u'no unmatched field names should be found')
def step_impl(context):
    assert len(context.result) == 0, context.result
