# pydatavolley

Python counterpart to the datavolley R package:
<https://github.com/openvolley/datavolley/>

A python set of code for reading volleyball scouting files in DataVolley
format (\*.dvw).

## Work in progress

------------------------------------------------------------------------

<div>

> **Current condition**
>
> ``` python
> from read_dv import get_plays
> import pandas as pd
> df = get_plays()
> print(df[df['skill'].notna()])
> ```
>
>                         code  point_phase  attack_phase start_coordinate mid_coordainte end_coordainte  time set home_setter_position visiting_setter_position video_file_number video_time home_p1 home_p2 home_p3 home_p4 home_p5 home_p6 visiting_p1 visiting_p2 visiting_p3  \
>     4      *10SM+~~~11C~~~00          NaN           NaN             0077            NaN           7732   NaN   1                    3                        1                 1        721      10      17       5      20       9      11           6           8           9   
>     5     a01RM-~~~11CM~~00B          NaN           NaN             0077            NaN           7732   NaN   1                    3                        1                 1        722      10      17       5      20       9      11           6           8           9   
>     6      a06EH#K1P~9C~~~00          NaN           NaN             3475            NaN            NaN   NaN   1                    3                        1                 1        724      10      17       5      20       9      11           6           8           9   
>     7     a07AH+VP~81CH1~00B          NaN           NaN             4546           5541           8127   NaN   1                    3                        1                 1        725      10      17       5      20       9      11           6           8           9   
>     8      *17BH/~~~~3B~~~00          NaN           NaN             4559            NaN            NaN   NaN   1                    3                        1                 1        725      10      17       5      20       9      11           6           8           9   
>     ...                  ...          ...           ...              ...            ...            ...   ...  ..                  ...                      ...               ...        ...     ...     ...     ...     ...     ...     ...         ...         ...         ...   
>     1420   a01SH!~~~57A~~~-4          NaN           NaN             0323            NaN           7574   NaN   3                    5                        2                 1       5077      12      16      10      17       5      20           9          10          17   
>     1421  *10RH!~~~57AM~~+4F          NaN           NaN             0323            NaN           7574   NaN   3                    5                        2                 1       5078      12      16      10      17       5      20           9          10          17   
>     1422   *05ET#K1F~4A~~~+4          NaN           NaN             4331            NaN            NaN   NaN   3                    5                        2                 1       5080      12      16      10      17       5      20           9          10          17   
>     1423  *10AT#X5~48AP2~+4F          NaN           NaN             4418            NaN           7647   NaN   3                    5                        2                 1       5081      12      16      10      17       5      20           9          10          17   
>     1424             *p25:20          NaN           NaN             2453            NaN            NaN   NaN   3                    5                        2                 1       5082      12      16      10      17       5      20           9          10          17   
>
>          visiting_p4 visiting_p5 visiting_p6                     team player_number player_id      player_name      skill evaluation_code set_code set_type attack_code num_players_numeric home_team_id visiting_team_id start_zone end_zone end_subzone  rally_number  \
>     4             12           7          11        Purdue University            10      2397    Azariah Stahl      Serve               +      NaN      NaN         NaN                 NaN          103              342          1        1           C             1   
>     5             12           7          11  Oral Roberts University             1      2252         Tori Roe  Reception               -      NaN      NaN         NaN                 NaN          103              342          1        1           C             1   
>     6             12           7          11  Oral Roberts University             6      2257  Lucija Bojanjac        Set               #       K1        P         NaN                 NaN          103              342        NaN        9           C             1   
>     7             12           7          11  Oral Roberts University             7      2258      Laura Milos     Attack               +      NaN      NaN          VP                   1          103              342          8        1           C             1   
>     8             12           7          11        Purdue University            17      2402     Blake Mohler      Block               /      NaN      NaN         NaN                 NaN          103              342        NaN        3           B             1   
>     ...          ...         ...         ...                      ...           ...       ...              ...        ...             ...      ...      ...         ...                 ...          ...              ...        ...      ...         ...           ...   
>     1420          11           4           7  Oral Roberts University             1      2252         Tori Roe      Serve               !      NaN      NaN         NaN                 NaN          103              342          5        7           A            45   
>     1421          11           4           7        Purdue University            10      2397    Azariah Stahl  Reception               !      NaN      NaN         NaN                 NaN          103              342          5        7           A            45   
>     1422          11           4           7        Purdue University             5      2392     Ashley Evans        Set               #       K1        F         NaN                 NaN          103              342        NaN        4           A            45   
>     1423          11           4           7        Purdue University            10      2397    Azariah Stahl     Attack               #      NaN      NaN          X5                   2          103              342          4        8           A            45   
>     1424          11           4           7        Purdue University           NaN       NaN              NaN      Point             NaN      NaN      NaN         NaN                 NaN          103              342        NaN      NaN         NaN            45   
>
>                      point_won_by home_team_score visiting_team_score             serving_team           receiving_team  
>     4     Oral Roberts University              00                  01        Purdue University  Oral Roberts University  
>     5     Oral Roberts University              00                  01        Purdue University  Oral Roberts University  
>     6     Oral Roberts University              00                  01        Purdue University  Oral Roberts University  
>     7     Oral Roberts University              00                  01        Purdue University  Oral Roberts University  
>     8     Oral Roberts University              00                  01        Purdue University  Oral Roberts University  
>     ...                       ...             ...                 ...                      ...                      ...  
>     1420        Purdue University              25                  20  Oral Roberts University        Purdue University  
>     1421        Purdue University              25                  20  Oral Roberts University        Purdue University  
>     1422        Purdue University              25                  20  Oral Roberts University        Purdue University  
>     1423        Purdue University              25                  20  Oral Roberts University        Purdue University  
>     1424        Purdue University              25                  20  Oral Roberts University        Purdue University  
>
>     [864 rows x 45 columns]

</div>
