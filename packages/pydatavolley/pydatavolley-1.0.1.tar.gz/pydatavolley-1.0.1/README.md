# pydatavolley

Python counterpart to the datavolley R package:
<https://github.com/openvolley/datavolley/>

<https://pypi.org/project/pydatavolley/>

A python set of code for reading volleyball scouting files in DataVolley
format (\*.dvw).

## Work in progress

------------------------------------------------------------------------

## Installation

Install pydatavolley using `pip`:

pip install pydatavolley - in some situations you might need to use
python3 -m pip install pydatavolley, or py -m pip install pydatavolley

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
>                       code  point_phase  attack_phase start_coordinate mid_coordainte end_coordainte  time set home_setter_position visiting_setter_position video_file_number video_time home_p1 home_p2 home_p3 home_p4 home_p5 home_p6 visiting_p1 visiting_p2 visiting_p3 visiting_p4  \
>     4    *10SM+~~~11C~~~00          NaN           NaN             0077            NaN           7732   NaN   1                    3                        1                 1        721      10      17       5      20       9      11           6           8           9          12   
>     5   a01RM-~~~11CM~~00B          NaN           NaN             0077            NaN           7732   NaN   1                    3                        1                 1        722      10      17       5      20       9      11           6           8           9          12   
>     6    a06EH#K1P~9C~~~00          NaN           NaN             3475            NaN            NaN   NaN   1                    3                        1                 1        724      10      17       5      20       9      11           6           8           9          12   
>     7   a07AH+VP~81CH1~00B          NaN           NaN             4546           5541           8127   NaN   1                    3                        1                 1        725      10      17       5      20       9      11           6           8           9          12   
>     8    *17BH/~~~~3B~~~00          NaN           NaN             4559            NaN            NaN   NaN   1                    3                        1                 1        725      10      17       5      20       9      11           6           8           9          12   
>     9   a08DH#~~~32DC~~00F          NaN           NaN             5554           4559           6022   NaN   1                    3                        1                 1        727      10      17       5      20       9      11           6           8           9          12   
>     10   a06EQ#K1C~3A~~~00          NaN           NaN             4159            NaN            NaN   NaN   1                    3                        1                 1        728      10      17       5      20       9      11           6           8           9          12   
>     11  a09AQ#X1~35BH2~00F          NaN           NaN             4644            NaN           8478   NaN   1                    3                        1                 1        729      10      17       5      20       9      11           6           8           9          12   
>     12             ap00:01          NaN           NaN             1622            NaN            NaN   NaN   1                    3                        1                 1        730      10      17       5      20       9      11           6           8           9          12   
>     17   a08SM=~~~12C~~~+1          NaN           NaN             0579            NaN           4667   NaN   1                    3                        6                 1        749      10      17       5      20       9      11           8           9          12           7   
>     18             *p01:01          NaN           NaN             4667            NaN            NaN   NaN   1                    3                        6                 1        751      10      17       5      20       9      11           8           9          12           7   
>     23   *17SM!~~~59A~~~00          NaN           NaN             0124            NaN           7618   NaN   1                    2                        6                 1        763      17       5      20       9      11      10           8           9          12           7   
>     24  a08RM!~~~59AM~~00B          NaN           NaN             0124            NaN           7618   NaN   1                    2                        6                 1        765      17       5      20       9      11      10           8           9          12           7   
>     25   a06ET#K1F~2C~~~00          NaN           NaN             4470            NaN            NaN   NaN   1                    2                        6                 1        766      17       5      20       9      11      10           8           9          12           7   
>     26  a07AT+X5~46BH2~00F          NaN           NaN             4616            NaN           8045   NaN   1                    2                        6                 1        767      17       5      20       9      11      10           8           9          12           7   
>     27  *10DT-~~~46BS~~00B          NaN           NaN             4616            NaN           8045   NaN   1                    2                        6                 1        768      17       5      20       9      11      10           8           9          12           7   
>     28  a08FH!~~~89D~~~00B          NaN           NaN             2649            NaN           7625   NaN   1                    2                        6                 1        774      17       5      20       9      11      10           8           9          12           7   
>     29   a06EM#K1F~2D~~~00          NaN           NaN             4371            NaN            NaN   NaN   1                    2                        6                 1        775      17       5      20       9      11      10           8           9          12           7   
>     30  a07AM-X9~47AH2~00F          NaN           NaN             4330            NaN           7273   NaN   1                    2                        6                 1        776      17       5      20       9      11      10           8           9          12           7   
>     31  *17DM+~~~47AS~~00B          NaN           NaN             4330            NaN           7273   NaN   1                    2                        6                 1        776      17       5      20       9      11      10           8           9          12           7   
>
>        visiting_p5 visiting_p6                     team player_number player_id       player_name      skill evaluation_code set_code set_type attack_code num_players_numeric home_team_id visiting_team_id start_zone end_zone end_subzone  rally_number             point_won_by  \
>     4            7          11        Purdue University            10      2397     Azariah Stahl      Serve               +      NaN      NaN         NaN                 NaN          103              342          1        1           C             1  Oral Roberts University   
>     5            7          11  Oral Roberts University             1      2252          Tori Roe  Reception               -      NaN      NaN         NaN                 NaN          103              342          1        1           C             1  Oral Roberts University   
>     6            7          11  Oral Roberts University             6      2257   Lucija Bojanjac        Set               #       K1        P         NaN                 NaN          103              342        NaN        9           C             1  Oral Roberts University   
>     7            7          11  Oral Roberts University             7      2258       Laura Milos     Attack               +      NaN      NaN          VP                   1          103              342          8        1           C             1  Oral Roberts University   
>     8            7          11        Purdue University            17      2402      Blake Mohler      Block               /      NaN      NaN         NaN                 NaN          103              342        NaN        3           B             1  Oral Roberts University   
>     9            7          11  Oral Roberts University             8     14622  Katarina Mikulic        Dig               #      NaN      NaN         NaN                 NaN          103              342          3        2           D             1  Oral Roberts University   
>     10           7          11  Oral Roberts University             6      2257   Lucija Bojanjac        Set               #       K1        C         NaN                 NaN          103              342        NaN        3           A             1  Oral Roberts University   
>     11           7          11  Oral Roberts University             9    -73747  Morgan Blomquist     Attack               #      NaN      NaN          X1                   2          103              342          3        5           B             1  Oral Roberts University   
>     12           7          11  Oral Roberts University           NaN       NaN               NaN      Point             NaN      NaN      NaN         NaN                 NaN          103              342        NaN      NaN         NaN             1  Oral Roberts University   
>     17          11           6  Oral Roberts University             8     14622  Katarina Mikulic      Serve               =      NaN      NaN         NaN                 NaN          103              342          1        2           C             2        Purdue University   
>     18          11           6        Purdue University           NaN       NaN               NaN      Point             NaN      NaN      NaN         NaN                 NaN          103              342        NaN      NaN         NaN             2        Purdue University   
>     23          11           6        Purdue University            17      2402      Blake Mohler      Serve               !      NaN      NaN         NaN                 NaN          103              342          5        9           A             3        Purdue University   
>     24          11           6  Oral Roberts University             8     14622  Katarina Mikulic  Reception               !      NaN      NaN         NaN                 NaN          103              342          5        9           A             3        Purdue University   
>     25          11           6  Oral Roberts University             6      2257   Lucija Bojanjac        Set               #       K1        F         NaN                 NaN          103              342        NaN        2           C             3        Purdue University   
>     26          11           6  Oral Roberts University             7      2258       Laura Milos     Attack               +      NaN      NaN          X5                   2          103              342          4        6           B             3        Purdue University   
>     27          11           6        Purdue University            10      2397     Azariah Stahl        Dig               -      NaN      NaN         NaN                 NaN          103              342          4        6           B             3        Purdue University   
>     28          11           6  Oral Roberts University             8     14622  Katarina Mikulic   Freeball               !      NaN      NaN         NaN                 NaN          103              342          8        9           D             3        Purdue University   
>     29          11           6  Oral Roberts University             6      2257   Lucija Bojanjac        Set               #       K1        F         NaN                 NaN          103              342        NaN        2           D             3        Purdue University   
>     30          11           6  Oral Roberts University             7      2258       Laura Milos     Attack               -      NaN      NaN          X9                   2          103              342          4        7           A             3        Purdue University   
>     31          11           6        Purdue University            17      2402      Blake Mohler        Dig               +      NaN      NaN         NaN                 NaN          103              342          4        7           A             3        Purdue University   
>
>        home_team_score visiting_team_score             serving_team           receiving_team  
>     4               00                  01        Purdue University  Oral Roberts University  
>     5               00                  01        Purdue University  Oral Roberts University  
>     6               00                  01        Purdue University  Oral Roberts University  
>     7               00                  01        Purdue University  Oral Roberts University  
>     8               00                  01        Purdue University  Oral Roberts University  
>     9               00                  01        Purdue University  Oral Roberts University  
>     10              00                  01        Purdue University  Oral Roberts University  
>     11              00                  01        Purdue University  Oral Roberts University  
>     12              00                  01        Purdue University  Oral Roberts University  
>     17              01                  01  Oral Roberts University        Purdue University  
>     18              01                  01  Oral Roberts University        Purdue University  
>     23              02                  01        Purdue University  Oral Roberts University  
>     24              02                  01        Purdue University  Oral Roberts University  
>     25              02                  01        Purdue University  Oral Roberts University  
>     26              02                  01        Purdue University  Oral Roberts University  
>     27              02                  01        Purdue University  Oral Roberts University  
>     28              02                  01        Purdue University  Oral Roberts University  
>     29              02                  01        Purdue University  Oral Roberts University  
>     30              02                  01        Purdue University  Oral Roberts University  
>     31              02                  01        Purdue University  Oral Roberts University  

</div>
