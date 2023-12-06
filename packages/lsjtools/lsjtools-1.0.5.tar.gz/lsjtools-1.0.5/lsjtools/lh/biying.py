import requests
import pandas as pd
from ..util._core import makedirs

def load_lsfs(code='601702',fsjb='dn', licence='biyinglicence', csv_path=None):
    '''历史分时交易
        Args:  
            code (str): 沪深股票代码.  
            fsjb (str): 分时级别，对应的值分别是 5m（5分钟）、15m（15分钟）、30m（30分钟）、60m（60分钟）、
            dn(日线未复权)、dq（日线前复权）、dh（日线后复权）、wn(周线未复权)、wq（周线前复权）、wh（周线后复权）、
            mn(月线未复权)、mq（月线前复权）、mh（月线后复权）、yn(年线未复权)、yq（年线前复权）、yh（年线后复权）
            licence (str): 必盈api授权码.  
            csv_path: 以csv格式存储至目标路径（如果为空则不存）
        Returns:  
            json对象
            字段名称:	数据类型	字段说明
            d:	string	交易时间，短分时级别格式为yyyy-MM-dd HH:mm:ss，日线级别为yyyy-MM-dd
            o:	number	开盘价（元）
            h:	number	最高价（元）
            l:	number	最低价（元）
            c:	number	收盘价（元）
            v:	number	成交量（手）
            e:	number	成交额（元）
            zf:	number	振幅（%）
            hs:	number	换手率（%）
            zd:	number	涨跌幅（%）
            zde:number	涨跌额（元） 
    '''

    response = requests.get(f'https://api.biyingapi.com/hszbl/fsjy/{code}/{fsjb}/{licence}')
    # 确保请求成功
    if response.status_code == 200:
        # 解析JSON响应
        df = pd.read_json(response.text)
        if csv_path is not None:
            makedirs(csv_path)
            df.to_csv(csv_path, index=False)

        return df
    else:
        raise RuntimeError(f"请求失败，状态码：{response.status_code}")

# if __name__ == '__main__':
#     makedirs('./test/data/biying/601702.csv')
#     # df = load_lsfs(fsjb='yq',csv_path='./test/data/biying/601702.csv')
#     # print(df)
