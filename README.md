## Why you need FIRE
Ask yourself, what is FIRE? Generally, if someone have successfully reached FIRE, it means that he/she doesn't have to work anymore but still has enough money covering all expenditure in her/his life. According to this defination, it is not hard to reach out the pros and cons of being FIRE:
 - Pros: Have free time to do the things that you really wish to do as surviving in society doesn't bother you anymore. It could be your hobby, your dream job that doesn't earn a lot, or just staying at a Sydney's beach everyday without doing anything.
 - Cons: ?

Factor Determination:
Some factors are not deterministic. They are dynamic variables that depend on individuals. For thoes who don't like traveling, total spendings would be relatively small, whereas more amount of asset to support getting enough passive income would be needed for thoes who travels to new places each year.
 - How much do you spend monthly? This should include your spendings on meal, housing, entertainment, hobby, insurence, anything that takes money away from your wallet. Remember that you won't accomplish FIRE if you lie to yourself.
 - How much do you earn monthly by paying your workforce? A vital signal to determine whether the money you earned belongs to this category is ask youself this question: Have you spent your time or workforce as chips on that trade?
 - How much passive income do you earn monthly? Earning passive income is the core of the FIRE plan. The way to earn passive income might be achieved by investing through stock market, real estates, government bonds, trust products, pension insurance, etc.

 Artifacts:
- When you live on 4% of your total asset, congratulations, you've achieved FIRE.

## Psychological Level
- How many percentage of the total asset is acceptable for you to invest? Saving in banks VS Transforming into other asset forms
- Are you fear of investing something?
- Do you feel calm if save money in banks?

## How to achieve FIRE

The formula of FIRE:

$$
\text{Monthly Spending} = 4\% \times \text{Total Asset}
$$

Consume that you split monthly spendings from your monthly income in advance. Given monthly income (MI), monthly spendings (MS), monthly rate of return (MROR), total asset (TA), percentage of TA acceptable for investment (POTAAFI), your next monthly total asset (NMTA) would be:

$$
NMTA = (\text{TA} \times \text{POTAAFI}) \times (\text{MROR} + 1) + (\text{TA} \times (1 - \text{POTAAFI}) + \text{MI} - \text{MS})
$$

$$
MS = \text{Food Expenditure} + \text{Housing Expenditure} + \text{Entertainment Expenditure}
$$

$$
MI = \text{Monthly Income} + \text{Part-time Job Income}
$$

$$
MROR = \text{Stock} + \text{Real Estates} + \text{Government Bonds} + \text{TODO}
$$

$$
\text{Stock} = \text{Hedging (TODO)}
$$

$$
\text{Deflation Rate} = \text{TODO}
$$

This system should have mechanisms to handle the unexpected expenditure and income. Let them be UE and UI, then we have:

$$
\text{UE} = \text{Prepared for health care} + \text{TODO}
$$

$$
\text{TA} = \text{TA} - \text{UE} + \text{UI}
$$

## FIRE Estimation Program

Program variables:
 - Unchanged variables:
1. The total asset when start the FIRE plan
2. Percentage of TA acceptable for investment
3. Monthly Food Costs
4. Monthly Housing Costs
5. Monthly Entertainment Costs
6. Monthly Transportation Costs
6. Monthly Income
7. Monthly rate of return

 - Changeable variables:
1. Expenditure: Every single cost such as food, housing, entertainment, transportation.
2. Income: Every single income such as salary and part-time job income.

Program functions:
1. Given fixed variables, calculate how many months needed to achieve FIRE.
2. Recalculate needed number of months on every expenditure and income update.

Consume that monthly spendings are fixed, you spend the same money on every single month. We can write an algorithm to calculate the number of months required to achieve FIRE:
1. Check if MS = 4% * TA
2. If returns yes: Congratulations
3. If returns no: Required number of months adds 1, TA = NMTA
4. Repeat 1 to 3

