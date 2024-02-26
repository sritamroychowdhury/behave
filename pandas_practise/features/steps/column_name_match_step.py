from behave import given, when, then
import pandas as pd
from file_input import column_name_match


@given(u'last week csv file input')
def step_impl(context):
    context.df1 = pd.read_csv("IntegriChain_Alexion_Koselugo_Daily_Status_lastweek.csv")


@given(u'latest csv file input')
def step_impl(context):
    context.df2 = pd.read_csv("IntegriChain_Alexion_Koselugo_Daily_Status_latest.csv")


@when(u'column names of the files are compared')
def step_impl(context):
    context.result = column_name_match(context.df1, context.df2)


@then(u'no unmatched column names should be found')
def step_impl(context):
    assert len(context.result) == 0, "Field names are not same in both the files"
