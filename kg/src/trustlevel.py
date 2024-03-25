import json
import os

from dotenv import load_dotenv

load_dotenv("../.env")
load_dotenv(".env")

import requests

api_key = os.getenv("TRUSTLEVEL_API_KEY")

def get_trustlevel_from_content(content: str):
    url = "https://powr86cuh9.execute-api.eu-west-1.amazonaws.com/v1/trustlevels/"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    data = json.dumps({"text": content[:2000]})
    response = requests.post(url, headers=headers, data=data)
    if response.ok:
        response_data = response.json()
        if 'trustlevel' in response_data:
            return response_data['trustlevel']
        else:
            raise ValueError(f"No trust level key found in response. Response: {response_data}")
    else:
        raise ConnectionError(f"Failed to get trust level: {response.reason}, Status Code: {response.status_code}")


if __name__ == "__main__":
    print(get_trustlevel_from_content("""Donald Trump’s campaign is engineering a plan to “make lemonade out of lemons” as a full docket of court appearances are about to swamp his political calendar.

The strategy, the former president's advisers tell NBC News, will involve trying to portray President Joe Biden as someone attempting to “imprison” his political opponents, muddying the waters between Trump’s and Biden’s legal problems, creating counterprogramming events focused on policy and ultimately pushing to delay the trials for as long as possible. 

The unprecedented task of a presidential candidate simultaneously swaying courts of law and public opinion has long loomed in the background. Trump turned his legal travails into primary gold, but repeating that feat in a general election — where swing voters matter — is more challenging.  

The first criminal trial is set to begin March 25, when a Manhattan jury will consider charges that Trump falsified business records to cover up hush money payments to an adult film star during his 2016 campaign. Manhattan District Attorney Alvin Bragg, however, said Thursday he doesn't oppose delaying the start of the trial for 30 days.
Along with the obvious legal pitfalls, the trial will have Trump in courtrooms almost all day at least four days a week as the general election kicks off — a trial that could last eight weeks. It means Trump will, at times, be running for president functionally on a part-time basis, unable to do things such as regularly hold live campaign events or fundraising.

Trump’s criminal legal woes — which include dozens of separate charges across four separate indictments — served as political rocket fuel during the GOP primary among base voters who almost universally, though without evidence, viewed the issue through the lens of Biden using the justice system to go after his top political rival. 

When entering the general election, however, the politics of Trump’s legal predicaments become increasingly murky.

And his team knows it. 

“Indictments are not ideal, we would rather the boss not be in court,” a top Trump adviser said. “But there will be an attempt to make lemonade out of lemons here.”

Another acknowledged that it “clearly presents a scheduling conflict,” but added, “We will work through it.” 

On weekends between trial days, Trump is expected to be doing more policy-focused events, drawing contrasts between his proposals and Biden’s record. The events will be held in specific communities affected by whatever specific policy is being highlighted that day. In addition, on Wednesdays — the one weekday without a court date — Trump is expected to focus on fundraising.

At this point in the campaign, as opposed to the stretch after Labor Day, Trump’s schedule wouldn’t be packed with rallies. But the court dates are likely to lighten his political calendar as long as he is on trial.

To try to fill Trump’s vacuum, the team plans to deploy more top-level campaign surrogates to “have a voice outside of New York City press conferences,” and increase attacks on Biden over issues such as immigration, his mental fitness, crime and the economy, according to one of the Trump advisers. 

They will also place a heavy focus on trying to counter attacks from his political foes that a second Trump term would usher a wannabe dictator into the White House.

“They [Democrats] are going to try and make the campaign about abortion and that we are a threat to democracy,” the Trump adviser said. “Hard to say we are a threat to democracy when you are trying to imprison political opponents.”

Matthew Bartlett, a Republican strategist, said it’s difficult to project the effect of Trump’s trials on the election because “an unprecedented part of American history is now colliding with the unpredictability of electoral politics.”

We do not even really need to win the argument, we just have to neutralize it.

TRUMP ADVISER

“There are serious charges but it is unclear if the American public can right now distinguish each individual case or even the critical details,” he said.

The hush money case in New York is scheduled to be the first Trump indictment to go to trial, but others will likely tether the former president to courtrooms throughout the general election calendar.

He has also been charged in a Florida federal court over his handling of classified documents after his presidency, a case in which prosecutors have requested a trial this calendar year but the judge has not yet set a date after agreeing to delay the original May start time.

He faces another federal trial in Washington, D.C., for charges related to his effort to overturn the 2020 election. That case is on hold while the Supreme Court considers Trump’s claim that he is immune from criminal charges for his actions while he was president. If the high court allows the case to move forward, it could mean Trump’s highest-profile trial will come in the last sprint to Election Day.

Finally, Trump faces separate charges in Georgia over efforts by him and his allies to overturn the state’s 2020 election results. That case has a proposed Aug. 5 trial date, but delays are expected. The judge in that case is currently weighing whether to disqualify prosecutor Fani Willis over alleged misconduct relating to her relationship with a subordinate.

Procedural delays are also a key part of Trump’s legal strategy. 

“What if none of this stuff is heard or settled before the election?” a Trump supporter said. “I mean, what then? What are we talking about here?”

The stunning nature of a former and potentially future president being charged with trying to thwart the smooth transition of power has been the main focus of Democrats, but is also central to the Trump campaign’s strategy while their candidate is stuck in court.

Advisers believe that if they amplify attacks on Biden that attempt to create an equivalency between Trump’s legal problems and Biden’s, they can effectively muddy the water with voters and in the process make the legal issues — including those related to election interference — a less significant issue.

“We do not even really need to win the argument, we just have to neutralize it,” another Trump adviser said. “If we do, the decision-making calculus favors us.”

Key to that strategy will be the report issued by special counsel Robert Hur, a former Trump-era Justice Department official who was appointed last year by Attorney General Merrick Garland to investigate Biden’s handling of classified documents after his time as vice president. 

Hur did not charge Biden, but his report left plenty of ammunition for the president’s political detractors. 

In the report released last month, Hur wrote that he wasn’t recommending charges against Biden, in part, because a jury would find him to be a “sympathetic, well-meaning elderly man with a poor memory,” a description Democrats said was overt partisan politics, while Republicans used it to continue to build a narrative that Biden is in mental decline. The transcript of Hur’s interview was more nuanced, showing the president stumbling over some facts but recalling others clearly.

The Hur report offers the Trump campaign a one-two punch. 

It allows his aides to hit on both his mental acuity, and the idea that there is a weaponized justice system. A key difference in the classified documents case is that Biden cooperated with investigators when it was discovered that he may have retained classified documents, while Trump did not. Still, Republicans say the fact that Biden was not charged and that Trump is facing 37 criminal counts after it was discovered is further evidence of a two-tiered justice system.

“It’s the sort of stuff that can really help us flip the script on this stuff,” the Trump adviser said. “It’s something people will be hearing a lot more about.”

Rob Godfrey, a South Carolina-based Republican strategist, said the value of Trump’s weaponization of government argument is more effective with GOP base voters than it is with persuadable voters in a general election, something backed up by polling data. 

As of February, 21% of Republicans believe Trump “committed serious federal crimes,” a number that jumps to 57% for independent voters, according to a New York Times/Siena tracking poll. NBC News polling in February also found that Trump’s standing would be hurt by a felony conviction. Trump was leading Biden 47%-42% overall, but Biden took a narrow 45%-43% lead when respondents were asked how they feel about Trump if he were convicted of a felony. 

It’s the reason, Godfrey says, Trump’s messaging needs to be two-pronged.

“Let the court cases continue to keep the base supporters solidified behind him, because it’s obviously a motivator for them,” he said. “But when it comes to independent voters, when it comes to softer Republican voters, it’s an open question of how much of a motivator the court cases are.”

“So what the Trump campaign and its allies should do,” Godfrey added, “is make sure those folks are focused on policy differences between the two candidates.”"""[:2500]))