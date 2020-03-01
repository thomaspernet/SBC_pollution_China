# Documentation

Add any documentation useful for the project here

## Papers Interested

| Project                                         | Theme        | PaperName                                                                                                                      | GoogleDoc                                                              | LinkWeava                                                                                                                      | Profile                                        |
|-------------------------------------------------|--------------|--------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| Soft Budget Constraint and pollution in China 👀 | Pollution    | Environmental policy and exports: Evidence from Chinese cities                                                                 | https://drive.google.com/file/d/1-SXSlRoS_2ZW7CK6XMhcXpJDPxAEF1xG/view | Environmental policy and exports: Evidence from Chinese cities                                                                 | https://dynalist.io/d/XKfJQeiB0Ca0jwkuezQ0tPv7 |
| Soft Budget Constraint and pollution in China 👀 | Pollution    | The impact of environmental regulation on Chinese spatial development                                                          | https://docs.google.com/file/d/1JguCKTBU_WDh8HzYbY-V8QzCNgqzYlN9/edit  | The impact of environmental regulation on Chinese spatial development                                                          |                                                |
| Soft Budget Constraint and pollution in China 👀 | Pollution    | Does environmental regulation drive away inbound foreign direct investment? Evidence from a quasi-natural experiment in China  |                                                                        | Does environmental regulation drive away inbound foreign direct investment? Evidence from a quasi-natural experiment in China  | https://dynalist.io/d/NoN72svhJGwmeD_FB8--rvgv |
| Soft Budget Constraint and pollution in China 👀 | Pollution    | The consequences of spatially differentiated water pollution regulation in China                                               | https://drive.google.com/file/d/15HDYRf07DPy27nHRjjlEYPkNAsBjSl5m/view | The consequences of spatially differentiated water pollution regulation in China                                               | https://dynalist.io/d/V31BAFi9NSfx1rqIccNVgRIa |
| Soft Budget Constraint and pollution in China 👀 | TCZ          | Can Environmental Regulations Drive Firms Innovation? Evidence from Two Policies in China                                      | https://docs.google.com/file/d/1_BgizwKFNaWa96yUt03KY1Ju08volXGy/edit  | Can Environmental Regulations Drive Firms Innovation? Evidence from Two Policies in China                                      |                                                |
| Soft Budget Constraint and pollution in China 👀 | TCZ          | Career concerns and multitasking local bureaucrats: Evidence of a target-based performance evaluation system in China          | https://docs.google.com/file/d/1fO46H7ZAmrUokwokCIPDvnsr4kJWGjGM/edit  | Career concerns and multitasking local bureaucrats: Evidence of a target-based performance evaluation system in China          |                                                |
| Soft Budget Constraint and pollution in China 👀 | TCZ          | Does environmental regulation drive away inbound foreign direct investment? Evidence from a quasi-natural experiment in China$ | https://docs.google.com/file/d/1pnyVlTOF5XZvQ2WQ7-X4IJD1XOoZfYlH/edit  | Does environmental regulation drive away inbound foreign direct investment? Evidence from a quasi-natural experiment in China$ | https://dynalist.io/d/NoN72svhJGwmeD_FB8--rvgv |
| Soft Budget Constraint and pollution in China 👀 | TCZ          | Pollution control and foreign firms’ exit behavior in China                                                                    | https://docs.google.com/file/d/1rKKu16tu9UewsK4HSVzk7lsL7k8rOfXp/edit  | Pollution control and foreign firms’ exit behavior in China                                                                    |                                                |
| Soft Budget Constraint and pollution in China 👀 | Productivity | The impact of environmental regulation on Chinese spatial development                                                          | https://docs.google.com/file/d/1JguCKTBU_WDh8HzYbY-V8QzCNgqzYlN9/edit  | The impact of environmental regulation on Chinese spatial development                                                          |                                                |

# Strategy for Soft Budget Constraint and pollution in China 👀


![](https://drive.google.com/uc?export=view&id=1Qvz56UwL8aHGaP5J1dbIdPX6qfG7wz39)

## Objective
* Demonstrate that SOE are not influenced by the environmental policy 

Strategy: DD

* Difference-In-Difference Model (DID) is an efficient and convenient way to analyze the influence of policies
* Especially with policies like AQCZ or TCZ which vary with the time and regions and result in two groups: experimental group and control group
  * due to the specific target and goal of the environmental policies and regulations, in this paper, we make one more difference
  * Both in two groups, there are before and after policy observations.
* The goal of this paper is to compare the before and after effect of these two policies with the placebo during the same period
* The political background shows us that the whole Chinese cities are divided into two groups:one is under the environmental regulations and the other no
* due to the centralized political system in China, two environmental regulations mentioned above were both implemented around the country at the same time
* This just makes our dataset a treatment group and a control group at two different time periods: one time period before ”treatment” and one time period after ”treatment”
* This condition actually satisfies requirements of Difference-in-Difference(DID) model, where $$\overline{y_{11}}-\overline{y_{21}}$$ represents horizontal difference between treatment group and control group before regulations were launched;
* $$\overline{y_{12}}-\overline{y_{22}}$$ represents horizontal difference be-tween treatment group and control group after regulations
* $$(\overline{y_{11}}-\overline{y_{21}})-(\overline{y_{12}}-\overline{y_{22}})$$ then can be interpreted as the regulation effec
Flaws DD
* Nevertheless, here comes a concern with DID model.
* First, the more polluting firms maybe more heavily influenced by the regulations
* What is more, not only can environmental regulations influence firms, but also firms can exert influence on policies making to some extent
* Lobby groups competing with policy makersis an important source of internalization of economic externalities

Strategy: DDD

* we are going to accompany the policies testing functions with pollutions intensity and adopt Difference-in-Difference-in-Difference (DIDID) model
* we consider three factors: regions (policies implemented or not), time (before and after policies implemented) and industries (heavy polluting and comparatively less polluting)
* The DIDID method helps us to control more factors. Here, we control province-year, year-industry and industry-province fixed effects
  * $$\sigma_{i t}$$ captures the province-year effects of a firm.
  * We used province-year level, because first same province firms show amount of common features like tax-deductible, lowest salary requirement and etc
  * By controlling industry-province effects, we allow for industries vary across different provinces.
    * This is unquestionably important. Although power centralized China often choosesto implement a policy across the country at the same time regardless the regional difference butit is the provincial government who choose to implement the policy
* Combining the variation in pollution reduction targets across cities and the before-and-after change,
  * we can estimate the impact of environmental regulations on industry emission of pollution using a difference-in-differences (DID) strategy
* Potential endogeneity
  * some time-varying provincial characteristics may be correlated with the outcome variable and the regressor at the same time, leading to bias in our estimates
  * we exploit the fact that industries that have different credit vulnerability are affected differently, and carry out a difference-in-difference-in-differences (DDD) strategy
* we combine three types of variation:
  * the time variation (i.e., before and after the start of the eleventh Five-Year Plan),
  * the cities variation (i.e., cities with high pollution reduction targets versus cities with low targets),
  * the industrial credit variation (i.e., more dependent vs less dependent)
* We identify the effect of stricter environmental policies from the differential effect of the city reduction mandate policy across cities, where the effect depends on the sector's intrinsic exposure to the new regulations.
