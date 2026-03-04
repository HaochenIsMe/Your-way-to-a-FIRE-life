## Why you need FIRE
Ask yourself, what is FIRE? Generally, if someone have successfully reached FIRE, it means that he/she doesn't have to work anymore but still has enough money covering all expenditure in her/his life. According to this defination, it is not hard to reach out the pros and cons of being FIRE:
 - Pros: Have free time to do the things that you really wish to do as surviving in society doesn't bother you anymore. It could be your hobby, your dream job that doesn't earn a lot, or just staying at a Sydney's beach everyday without doing anything.
 - Cons: ?

Factor Determination:
Some factors are not deterministic. They are dynamic variables that depend on individuals. For thoes who don't like traveling, total spendings would be relatively small, whereas more amount of asset to support getting enough passive income would be needed for thoes who travels to new places each year.
 - How much do you spend annually? This should include your spendings on meal, housing, entertainment, hobby, insurence, anything that takes money away from your wallet. Remember that you won't accomplish FIRE if you lie to yourself.
 - How much do you earn annually by paying your workforce? A vital signal to determine whether the money you earned belongs to this category is ask youself this question: Have you spent your time or workforce as chips on that trade?
 - How much passive income do you earn annually? Earning passive income is the core of the FIRE plan. The way to earn passive income might be achieved by investing through stock market, real estates, government bonds, trust products, pension insurance, etc.

 Artifacts:
- When you live on 4% of your total asset, congratulations, you've achieved FIRE.

## Psychological Level
- How many percentage of the total asset is acceptable for you to invest? Saving in banks VS Transforming into other asset forms
- Are you fear of investing something?
- Do you feel calm if save money in banks?

## How to achieve FIRE

The formula of FIRE:

- **Annual Spending** = 4% × COI

We have to quantify the following elements to concretely come up with the time needed to achieve financial independence:

- Risk Tolerance Rate: The rate of asset used for investment
- Monthly Salary
- MROI (Monthly Return of Investment)
- COI (Cost of Investment)

The simulation runs month by month. At the start of each month:

- **Cash Earned This Month** = Monthly Salary × (1 - Risk Tolerance Rate)
- **Total Cash** = Remaining Cash + Cash Earned This Month
- **COI Appended This Month** = Monthly Salary × Risk Tolerance Rate
- **COI** = Current COI × (1 + MROI) + COI Appended This Month
- **Monthly Expenditure** = Rent Costs + Utilities + Internet Costs + Food Costs + Transportation Costs + Mobile Phone Plan
- **Remaining Cash** = Total Cash − Monthly Expenditure
- **Total Assets** = COI + Remaining Cash

This system should have mechanisms to handle the unexpected expenditure and income. 

## Time to the FIRE Estimation

Program variables:
 - Unchanged variables:
1. Initial Cash Amount
2. Initial COI
3. Risk Tolerance Rate
3. Monthly Salary
4. MROI
5. Rent Costs
6. Utilities
7. Internet Costs
8. Food Costs
9. Transportation Costs
10. Mobile Phone Plan

 - Changeable variables:
1. Unexpected Expenditure
2. Unexpected Income

Program functions:
1. Estimate the current Annual Total Assets and how many years and months needed to achieve the FIRE.
2. Re-estimate Annual Total Assets on every single UE and UI update.
3. Plot a curve of years to FIRE vs AROI, visualising how different annual return rates affect the time to financial independence.

# 向着AROI 10%前进
注：
1. 受限于语言能力，本篇以中文起稿，确保逻辑自洽后再进行英语本地化。
2. 这里假设我们的AROI目标为10%。量化框架完成后，可以任意修改这一数字。

我认真地思考了，试图全力捕捉到“年化收益率10%”与“实际股市操作”之间的违和感。我发现，如果将这两件事比喻成齿轮，它们好比一个是方的，一个是圆的，无法咬合。差在了哪里？将他们之间的差距语言化出来极其重要！我们来语言化他们之间的违和感：
1. 年化收益率，是指从第T年看，相对于第T-1年，你的资产之比是多少。
2. 股市，是反应了投资人对未来的预期。
一个在往后看，一个在往前看，它们没有站在同一个时间点上。这就是最本质的问题。但不可否认，股票是帮助一般人达成财富自由非常厉害的工具。为了让这一工具为己所用，首先我们要量化股票投资是什么，并引入期望值的概念，好让一个未来的概念服务于现在。

什么是股票投资，我们定义一次股票投资是指：
1. 在Start Time点买入的
2. 有固定COI的 (具体指 n股 x Start Time时的单价)
3. 预计在End Time时卖出的
4. 在End Time达到Expected Price的
5. 在End Time达到Expected Price的概率为Probability的
一次朝向AROI 10%努力的投入
期望值公式：
E()