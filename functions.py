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
 
#--- 试图写一个带 retry 的读取函数版本
from retry import retry

class HttpError(Exception):         # retry把Exception作为重试的条件，这里我们自定义HttpError401
    """ Http Error """


@retry(HttpError, tries=3, delay=2)   # 以装饰器的方式使用retry
def attempt_read_request(app_token, table_id, authen_token_paras):
    import requests
    
    read_response = read_from_feishu(app_token, table_id, authen_token_paras)
    print(read_response.status_code)
    
    
    if read_response.status_code != 200:            # 如果请求不成功，即返回的不是200，则执行下面的抛出异常操作                      
        raise HttpError
    return read_response                    # 如果请求返回成功，则获取请求的响应数据

