import pandas as pd


# sort dataframe values
def sort_df(main_df, selected_sort_by, selected_is_descending):
    df = main_df.copy()
    if selected_sort_by == 'Max Salary' and selected_is_descending:
        df = df.sort_values(by=['max_salary'], ascending=False)
    elif selected_sort_by == 'Min Salary' and selected_is_descending:
        df = df.sort_values(by=['min_salary'], ascending=False)
    elif selected_sort_by == 'Max Salary':
        df = df.sort_values(by=['max_salary'])
    elif selected_sort_by == 'Min Salary':
        df = df.sort_values(by=['min_salary'])
    return df


# filter df with job title keywords
def filter_job_title(main_df, selected_job_title_keywords):
    df = main_df.copy()
    job_title_keywords = selected_job_title_keywords.split()
    data = pd.DataFrame()
    for keyword in job_title_keywords:
        filtered_df = df[df['job_title'].str.contains(keyword)]
        data = pd.concat([data, filtered_df])
    data.drop_duplicates()
    if job_title_keywords:
        df = data
    return df


# filter df with company name keywords
def filter_company_name(main_df, selected_company_name_keywords):
    df = main_df.copy()
    company_name_keywords = selected_company_name_keywords.split()
    data = pd.DataFrame()
    for keyword in company_name_keywords:
        filtered_df = df[df['employer'].str.contains(keyword)]
        data = pd.concat([data, filtered_df])
    data.drop_duplicates()
    if company_name_keywords:
        df = data
    return df


# filter df with contract types
def filter_contract_type(main_df, selected_contract_type):
    df = main_df.copy()
    if selected_contract_type != "All":
        df = df[df['contract_type'].str.contains(selected_contract_type, na=False)]
    return df


# filter df for salary range
def filter_salary_range(main_df, selected_salary_range):
    df = main_df.copy()
    df = df.loc[(df['min_salary'] <= selected_salary_range[1]) &
                (df['max_salary'] >= selected_salary_range[0]),]
    return df
