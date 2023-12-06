# pydatavolley

Python counterpart to the datavolley R package:
<https://github.com/openvolley/datavolley/>

<https://pypi.org/project/pydatavolley/>

A python set of code for reading volleyball scouting files in DataVolley
format (\*.dvw).

## Work in progress

## Installation

Install pydatavolley using `pip`:

``` terminal
py -m pip install pydatavolley
python3 -m pip install pydatavolley
pip install pydatavolley
```

------------------------------------------------------------------------

## Example

<div>

> **Current condition**
>
> ``` python
> import pandas as pd
> from read_dv import DataVolley
> file_path = '&2017-08-25 PURD-ORU.dvw'
> dv_instance = DataVolley(file_path)
> df = dv_instance.get_plays()
> print(df[df['skill'].notna()].head(20))
> ```
>
>                       code  point_phase  attack_phase start_coordinate  \
>     4    *10SM+~~~11C~~~00          NaN           NaN             0077   
>     5   a01RM-~~~11CM~~00B          NaN           NaN             0077   
>     6    a06EH#K1P~9C~~~00          NaN           NaN             3475   
>     7   a07AH+VP~81CH1~00B          NaN           NaN             4546   
>     8    *17BH/~~~~3B~~~00          NaN           NaN             4559   
>     9   a08DH#~~~32DC~~00F          NaN           NaN             5554   
>     10   a06EQ#K1C~3A~~~00          NaN           NaN             4159   
>     11  a09AQ#X1~35BH2~00F          NaN           NaN             4644   
>     12             ap00:01          NaN           NaN             1622   
>     17   a08SM=~~~12C~~~+1          NaN           NaN             0579   
>     18             *p01:01          NaN           NaN             4667   
>     23   *17SM!~~~59A~~~00          NaN           NaN             0124   
>     24  a08RM!~~~59AM~~00B          NaN           NaN             0124   
>     25   a06ET#K1F~2C~~~00          NaN           NaN             4470   
>     26  a07AT+X5~46BH2~00F          NaN           NaN             4616   
>     27  *10DT-~~~46BS~~00B          NaN           NaN             4616   
>     28  a08FH!~~~89D~~~00B          NaN           NaN             2649   
>     29   a06EM#K1F~2D~~~00          NaN           NaN             4371   
>     30  a07AM-X9~47AH2~00F          NaN           NaN             4330   
>     31  *17DM+~~~47AS~~00B          NaN           NaN             4330   
>
>        mid_coordainte end_coordainte  time set home_setter_position  \
>     4             NaN           7732   NaN   1                    3   
>     5             NaN           7732   NaN   1                    3   
>     6             NaN            NaN   NaN   1                    3   
>     7            5541           8127   NaN   1                    3   
>     8             NaN            NaN   NaN   1                    3   
>     9            4559           6022   NaN   1                    3   
>     10            NaN            NaN   NaN   1                    3   
>     11            NaN           8478   NaN   1                    3   
>     12            NaN            NaN   NaN   1                    3   
>     17            NaN           4667   NaN   1                    3   
>     18            NaN            NaN   NaN   1                    3   
>     23            NaN           7618   NaN   1                    2   
>     24            NaN           7618   NaN   1                    2   
>     25            NaN            NaN   NaN   1                    2   
>     26            NaN           8045   NaN   1                    2   
>     27            NaN           8045   NaN   1                    2   
>     28            NaN           7625   NaN   1                    2   
>     29            NaN            NaN   NaN   1                    2   
>     30            NaN           7273   NaN   1                    2   
>     31            NaN           7273   NaN   1                    2   
>
>        visiting_setter_position  ... visiting_team_id start_zone end_zone  \
>     4                         1  ...              342          1        1   
>     5                         1  ...              342          1        1   
>     6                         1  ...              342        NaN        9   
>     7                         1  ...              342          8        1   
>     8                         1  ...              342        NaN        3   
>     9                         1  ...              342          3        2   
>     10                        1  ...              342        NaN        3   
>     11                        1  ...              342          3        5   
>     12                        1  ...              342        NaN      NaN   
>     17                        6  ...              342          1        2   
>     18                        6  ...              342        NaN      NaN   
>     23                        6  ...              342          5        9   
>     24                        6  ...              342          5        9   
>     25                        6  ...              342        NaN        2   
>     26                        6  ...              342          4        6   
>     27                        6  ...              342          4        6   
>     28                        6  ...              342          8        9   
>     29                        6  ...              342        NaN        2   
>     30                        6  ...              342          4        7   
>     31                        6  ...              342          4        7   
>
>        end_subzone rally_number             point_won_by home_team_score  \
>     4            C            1  Oral Roberts University              00   
>     5            C            1  Oral Roberts University              00   
>     6            C            1  Oral Roberts University              00   
>     7            C            1  Oral Roberts University              00   
>     8            B            1  Oral Roberts University              00   
>     9            D            1  Oral Roberts University              00   
>     10           A            1  Oral Roberts University              00   
>     11           B            1  Oral Roberts University              00   
>     12         NaN            1  Oral Roberts University              00   
>     17           C            2        Purdue University              01   
>     18         NaN            2        Purdue University              01   
>     23           A            3        Purdue University              02   
>     24           A            3        Purdue University              02   
>     25           C            3        Purdue University              02   
>     26           B            3        Purdue University              02   
>     27           B            3        Purdue University              02   
>     28           D            3        Purdue University              02   
>     29           D            3        Purdue University              02   
>     30           A            3        Purdue University              02   
>     31           A            3        Purdue University              02   
>
>        visiting_team_score             serving_team           receiving_team  
>     4                   01        Purdue University  Oral Roberts University  
>     5                   01        Purdue University  Oral Roberts University  
>     6                   01        Purdue University  Oral Roberts University  
>     7                   01        Purdue University  Oral Roberts University  
>     8                   01        Purdue University  Oral Roberts University  
>     9                   01        Purdue University  Oral Roberts University  
>     10                  01        Purdue University  Oral Roberts University  
>     11                  01        Purdue University  Oral Roberts University  
>     12                  01        Purdue University  Oral Roberts University  
>     17                  01  Oral Roberts University        Purdue University  
>     18                  01  Oral Roberts University        Purdue University  
>     23                  01        Purdue University  Oral Roberts University  
>     24                  01        Purdue University  Oral Roberts University  
>     25                  01        Purdue University  Oral Roberts University  
>     26                  01        Purdue University  Oral Roberts University  
>     27                  01        Purdue University  Oral Roberts University  
>     28                  01        Purdue University  Oral Roberts University  
>     29                  01        Purdue University  Oral Roberts University  
>     30                  01        Purdue University  Oral Roberts University  
>     31                  01        Purdue University  Oral Roberts University  
>
>     [20 rows x 45 columns]

</div>
