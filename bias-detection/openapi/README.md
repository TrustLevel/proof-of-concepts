# TrustLevel Bias Detection


## Setup

dependencies
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Prompts

```
-- 0.2

You will be provided with text delimited by triple quotes for which you determine the bias score ("bias_score") in the range [0.0,1.0] where 0.0 means not biased and 1.0 means the text is very biased. You only reply with a valid JSON object with the field "bias_score". Explain step by step how you came up with the score in an additional JSON object field called "chain_of_thought" but do not summarize the text.

"""{Text}"""

```
-- 0.6
You will be provided with text delimited by triple quotes for which you determine the bias score in the range [0.0,1.0] where 0.0 means not biased and 1.0 means the text is very biased. You only reply with a valid JSON object containing the fields "bias_score" and "indicators". To analyze the text, you should pay attention to the language used in the text. Biased texts often contain emotionally charged or loaded language, as well as exaggerated claims or sweeping generalizations. Provide a list of key indicators that you found in the text that led you to your bias score. Do not summarize the text.

"""{Text}"""
```

```
-- 0.6
You will be provided with text delimited by triple quotes for which you determine the bias score in the range [0.0,1.0] where 0.0 means not biased and 1.0 means the text is very biased. You only reply with a valid JSON object containing the fields "bias_score" and "bias_indicators", "non_bias_indicators". To analyze the text, you should pay attention to the language used in the text. Biased texts often contain emotionally charged or loaded language, as well as exaggerated claims or sweeping generalizations. Provide a list of key indicators ("bias_indicators" and "non_bias_indicators") that you found in the text that led you to your bias score. Do not summarize the text.

"""{Text}"""
```


```
"""Donald Trump is ahead of his Republican opponents on key measures of popularity, while US President Joe Biden’s job approval rating has hit a new low, according to a new poll.

The findings from an ABC News/Ipsos poll published on Sunday come a day ahead of the Iowa caucuses as the 2024 race to the US presidential elections speeds up.

The survey showed that former President Trump leads with a huge advantage against the other Republican candidates – Ron DeSantis, Nikki Haley, Vivek Ramaswamy and Asa Hutchinson – on three fronts.

At least 68 percent of Republicans and GOP-leaning independents say Trump is the candidate with the “best chance” of getting elected in November. That plummets to 12 percent for Haley, 11 percent for DeSantis and single digits for the rest, the report said.

Trump also has an advantage compared to the other candidates in being rated the “strongest leader” and being the “best qualified” to serve as president.

Trump beats his opponents on empathy and shared values as well. He got the most votes – though by a lesser margin – for being the one who “best represents your values” and for best understanding “your problems”.

But Republicans with a four-year college degree were less likely than non-graduates to say Trump was best on each of the attributes tested. Just 27 percent of those with a college degree said Trump best understands the problems of people like them, compared with 57 percent of those without a degree.

Overall, more than 70 percent of Republican adults would be satisfied with Trump as a nominee.

By comparison, 57 percent of Democrats would feel the same about President Biden being the Democratic Party’s choice.

According to the survey, Biden’s job approval rating has dropped to a low for any US president in the past 15 years.

At 33 percent, Biden’s approval rating is worse “than Trump’s low as president (36 percent) and the lowest since George W Bush from 2006-2008”, read the report. Fifty-eight percent disapprove of Biden’s work.

Some 31 percent of women approve of Biden’s work in office, a new low. Back in 2020, he won 57 percent of women. Among men, 34 percent approve of his work in office.

There was also no good news from Black and Hispanic voters: Biden’s approval rating is 21 points below average among Black people and 15 points below average among Hispanic people, compared with 6 points among white people.

When comparing the main Republican and Democratic hopefuls, the report said Biden leads Trump in perceptions of his honesty and trustworthiness – 41 percent say this describes Biden, and 26 percent say it describes Trump. But Trump beats Biden in perceptions of “mental sharpness” and “physical health” needed to be president again.

“A Biden/Trump general election, if that’s the outcome of the primary season, would represent a battle of markedly unpopular candidates,” the report added."""
```