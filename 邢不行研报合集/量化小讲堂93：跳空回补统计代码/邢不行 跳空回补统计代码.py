import pandas as pd
import numpy as np


pd.set_option('expand_frame_repr', False)

df = pd.read_csv('sh000001.csv')

con_up = df['low'] > df['high'].shift(1)
con_down = df['high'] < df['low'].shift(1)
df['hop'] = np.nan
df.loc[con_up, 'hop_up'] = -1
df.loc[con_down, 'hop_down'] = 1

hop_record = []

for i in range(len(df)):
    if df['hop_up'].at[i] == -1:

        hop_date = df['candle_end_time'].at[i]
        ex_hop_price = df['high'].at[i - 1]
        post_hop_price = df['low'].at[i]
        fill_date = ''

        for j in range(i, len(df)):
            if df['low'].at[j] <= ex_hop_price:
                fill_date = df['candle_end_time'].at[j]
                break

        hop_record.append({'hop': 'up',
                           'hop_date': hop_date,
                           'ex_hop_price': ex_hop_price,
                           'post_hop_price': post_hop_price,
                           'fill_date': fill_date
                           })

    elif df['hop_down'].at[i] == 1:
        hop_date = df['candle_end_time'].at[i]
        ex_hop_price = df['low'].at[i - 1]
        post_hop_price = df['high'].at[i]
        fill_date = ''
        # 看之后有没有回补向下的跳空
        for j in range(i, len(df)):
            if df['high'].at[j] >= ex_hop_price:
                fill_date = df['candle_end_time'].at[j]
                break
        hop_record.append({'hop': 'down',
                           'hop_date': hop_date,
                           'ex_hop_price': ex_hop_price,
                           'post_hop_price': post_hop_price,
                           'fill_date': fill_date,
                           })

hop_df = pd.DataFrame(hop_record)
hop_df.to_csv('上证指数跳空回补记录.csv', encoding='gbk')
print(hop_df)