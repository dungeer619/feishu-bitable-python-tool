#--- 读取
def read_from_feishu(app_token, table_id, authen_token_paras):
    import requests

    authen_token_url = authen_token_paras['authen_token_url']
    authen_token_post_data = authen_token_paras['authen_token_post_data']
    authen_token_name = authen_token_paras['authen_token_name']
    
    # 获取tenant_access_token
    r = requests.post(authen_token_url, data=authen_token_post_data)
    tat = r.json()[authen_token_name]


    # 电子表格单元格的数据
    header = {"content-type":"application/json", "Authorization":"Bearer " + str(tat)}

    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/{0}/tables/{1}/records".format(app_token, table_id)
    print(url)

    read_response = requests.request("GET", url, headers=header)
    print(read_response.status_code)
    return(read_response)
 

    
#------ 试图写一个带 retry 的读取函数版本
from retry import retry

class HttpError(Exception):         # retry把Exception作为重试的条件
    """ Http Error """


@retry(HttpError, tries=3, delay=2)   # 以装饰器的方式使用retry
def attempt_read_request(app_token, table_id, authen_token_paras):
    import requests
    
    read_response = read_from_feishu(app_token, table_id, authen_token_paras)
    print(read_response.status_code)
    
    
    if read_response.status_code != 200:            # 如果请求不成功，即返回的不是200，则执行下面的抛出异常操作                      
        raise HttpError
    return read_response                    # 如果请求返回成功，则获取请求的响应数据


#--- 按页读取
def read_from_feishu_by_page(page_token, app_token, table_id, authen_token_paras):
    import requests

    authen_token_url = authen_token_paras['authen_token_url']
    authen_token_post_data = authen_token_paras['authen_token_post_data']
    authen_token_name = authen_token_paras['authen_token_name']
    
    # 获取tenant_access_token
    r = requests.post(authen_token_url, data=authen_token_post_data)
    tat = r.json()[authen_token_name]


    # 电子表格单元格的数据
    header = {"content-type":"application/json", "Authorization":"Bearer " + str(tat)}

    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/{0}/tables/{1}/records?page_token={2}".format(app_token, table_id, page_token)
    print(url)

    read_response = requests.request("GET", url, headers=header)
    print(read_response.status_code)
    return(read_response)


#------ 试图写一个带 retry 的读取函数版本
from retry import retry

class HttpError(Exception):         # retry把Exception作为重试的条件
    """ Http Error """


@retry(HttpError, tries=3, delay=2)   # 以装饰器的方式使用retry
def attempt_read_request_by_page(page_token, app_token, table_id, authen_token_paras):
    import requests
    
    read_response = read_from_feishu_by_page(page_token, app_token, table_id, authen_token_paras)
    print(read_response.status_code)
    
    
    if read_response.status_code != 200:            # 如果请求不成功，即返回的不是200，则执行下面的抛出异常操作                      
        raise HttpError
    return read_response                    # 如果请求返回成功，则获取请求的响应数据


#--- 按页读取所有记录
def get_records_from_feishu(app_token, table_id, authen_token_paras):
    import json
    import pandas
    from pandas import json_normalize

    read_response = attempt_read_request(app_token, table_id, authen_token_paras)
    readin_df = json_normalize(json.loads(read_response.text)['data']['items'])

    page_token = json.loads(read_response.text)['data']['page_token']
    totalNum = json.loads(read_response.text)['data']['total']
    num_of_iterations = (totalNum-1)//500

    print(readin_df)
    for i in range(0, num_of_iterations):
        read_response = attempt_read_request_by_page(page_token, app_token, table_id, authen_token_paras)
        readin_df = pd.concat([readin_df, json_normalize(json.loads(read_response.text)['data']['items'])], ignore_index=True)
        # print("---------------------- New -----------------------")
        # print(readin_df)
    print("app_token:"+app_token+" table_id:"+table_id)
    print("总行数:"+str(readin_df.shape[0]))
    return readin_df


#--- 删除
#------ 获取删除的record_id
def get_records_to_del(read_response):
    import requests
    import json
    
    # 2. 拆出record_id
    import json
    history_records = json.loads(read_response.text)
    # print(history_records)

    # data -> items -> record_id
    records_to_del = []
    
    if history_records['data']['items']!=None:
        for item in history_records['data']['items']:
            records_to_del.append(item['record_id'])

    print(len(records_to_del))
    return(records_to_del)

#------ 根据record_id删除
def delete_records_of_feishu(app_token, table_id, records_to_del, authen_token_paras):
    import requests
    import json
    
    authen_token_url = authen_token_paras['authen_token_url']
    authen_token_post_data = authen_token_paras['authen_token_post_data']
    authen_token_name = authen_token_paras['authen_token_name']
    
    # 获取tenant_access_token
    r = requests.post(authen_token_url, data=authen_token_post_data)
    tat = r.json()[authen_token_name]

    # 删除历史数据
    # 电子表格单元格的数据
    header = {"content-type":"application/json", "Authorization":"Bearer " + str(tat)}

    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/{0}/tables/{1}/records/batch_delete".format(app_token, table_id)
    print(url)

    request_content = {
        "records": records_to_del
    }

    # print(request_content)

    response = requests.request("POST", url, headers=header, data=json.dumps(request_content))

    # print(response.text)
    return response


#------ 试图写一个带 retry 的删除函数版本
from retry import retry

class HttpError(Exception):         # retry把Exception作为重试的条件
    """ Http Error """

@retry(HttpError, tries=3, delay=2)   # 以装饰器的方式使用retry
def attempt_delete_request(app_token, table_id, records_to_del, authen_token_paras):
    import requests
    
    delete_response = delete_records_of_feishu(app_token, table_id, records_to_del, authen_token_paras)
    print(delete_response.status_code)
    
    
    if delete_response.status_code != 200:            # 如果请求不成功，即返回的不是200，则执行下面的抛出异常操作                      
        raise HttpError
    return delete_response                    # 如果请求返回成功，则获取请求的响应数据


#------ 删除所有记录
def delete_records_of_feishu_per500(app_token, table_id, authen_token_paras):
    import requests
    import json
    
    read_response = attempt_read_request(app_token, table_id, authen_token_paras)
    records_to_del = get_records_to_del(read_response)
    # print(records_to_del)

    while(json.loads(read_response.text)['data']['total']!=0):
        # print(json.loads(read_response.text)['data']['total'])
        delete_response = attempt_delete_request(app_token, table_id, records_to_del, authen_token_paras)
        print(delete_response.status_code)
        read_response = read_from_feishu(app_token, table_id, authen_token_paras)
        records_to_del = get_records_to_del(read_response)
        # print(records_to_del)

    print(len(records_to_del))
    
    

#--- 写入
#------ 单次写入
def write_to_feishu(app_token, table_id, data_json_str, authen_token_paras):
    import json
    import requests
    
    authen_token_url = authen_token_paras['authen_token_url']
    authen_token_post_data = authen_token_paras['authen_token_post_data']
    authen_token_name = authen_token_paras['authen_token_name']
    
    # 获取tenant_access_token
    r = requests.post(authen_token_url, data=authen_token_post_data)
    tat = r.json()[authen_token_name]


    # 电子表格单元格的数据
    header = {"content-type":"application/json", "Authorization":"Bearer " + str(tat)}

    api_url = "https://open.feishu.cn/open-apis/bitable/v1/apps/{0}/tables/{1}/records/batch_create".format(app_token, table_id)
    print(api_url)

    # print("--------function: write_to_feishu---------")
    # print(data_json_str)
    request_content = json.loads(data_json_str)

    # print(request_content)

    response = requests.request("POST", api_url, headers=header, data=json.dumps(request_content))
    # print(response.text)
    return response


#------ 试图写一个带 retry 的写入函数版本
from retry import retry

class HttpError(Exception):         # retry把Exception作为重试的条件
    """ Http Error """


@retry(HttpError, tries=3, delay=2)   # 以装饰器的方式使用retry
def attempt_write_request(app_token, table_id, data_json_str, authen_token_paras):
    import requests
    
    write_response = write_to_feishu(app_token, table_id, data_json_str, authen_token_paras)
    print(write_response.status_code)
    
    
    if write_response.status_code != 200:            # 如果请求不成功，即返回的不是200，则执行下面的抛出异常操作                      
        raise HttpError
    return write_response                    # 如果请求返回成功，则获取请求的响应数据


#------ 总写入
def write_to_feishu_per500(data_frame, app_token, table_id, authen_token_paras):
    num_of_iterations = data_frame.shape[0]//500
    
    end_index = 0
    for i in range(0, num_of_iterations+(data_frame.shape[0]%500>0 and 1 or 0)):
        start_index = end_index
        end_index = (i<num_of_iterations and start_index+500 or data_frame.shape[0])

        data_json_ = data_frame[start_index:end_index].to_json(orient="records")
        data_json_mid = data_json_.replace("{\""+data_frame.columns[0]+"\"", "{\"fields\": {\""+data_frame.columns[0]+"\"")
        data_json_mid = data_json_mid.replace("}", "}}")
        data_json_str = "{\"records\": " + data_json_mid + "}"

        # print("--------function: write_to_feishu_per500---------")
        # print(data_json_str)
        write_response = attempt_write_request(app_token, table_id, data_json_str, authen_token_paras)
        print(write_response.status_code)
