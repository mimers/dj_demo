import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pyhive import hive
conn = hive.Connection(host='10.10.76.185', port=10008)

df_v = pd.read_sql('''select
    t1.account_name,
    t1.company_name,
    t1.account_num,
    t1.pay_ttl,
    t1.recent,
    row_number() over(partition by t1.account_name order by t1.recent) as recency_num
from
(
    select 
        account_name,
        company_name,
        DATEDIFF(to_date(from_utc_timestamp(current_timestamp(), 'Asia/Beijing')),pay_time) as recent,
        count(DISTINCT transaction_id) as account_num,
        sum(pay_amount) as pay_ttl
    from shixiaolu.test
    group by 1,2,3
    order by pay_ttl desc
)t1
having recency_num = 1
order by pay_ttl desc''', conn)
df_v