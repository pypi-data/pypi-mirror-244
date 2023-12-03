# ao - Hey Oh!

_"Hey oh! What is france?"_

[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/tomhea/ao)](https://github.com/tomhea/ao)
[![GitHub](https://img.shields.io/github/license/tomhea/ao)](LICENSE)
[![PyPI - Version](https://img.shields.io/pypi/v/ao)](https://pypi.org/project/ao/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ao)](https://pypi.org/project/ao/)

Import the wikipedia entry summary.  
As simple as that.

```python
from ao import industrial_revolution
print(industrial_revolution)
```
That prints:  
> The Industrial Revolution, also known as the First Industrial Revolution, was a period of global transition of human economy towards more widespread, efficient and stable manufacturing processes that succeeded the Agricultural Revolution, starting from Great Britain, continental Europe, and the United States, that occurred during the period from around 1760 to about 1820–1840. This transition included going from hand production methods to machines; new chemical manufacturing and iron production processes; the increasing use of water power and steam power; the development of machine tools; and the rise of the mechanized factory system. Output greatly increased, and the result was an unprecedented rise in population and the rate of population growth. The textile industry was the first to use modern production methods, and textiles became the dominant industry in terms of employment, value of output, and capital invested.

## Examples & IPython

It's also useful in ipython:

```python
In [1]: import ao

In [2]: ao.basketball
Out[2]: "Basketball is a team sport in which two teams, most commonly of five players each, opposing one another on a rectangular court, compete with the primary objective of shooting a basketball through the defender's hoop, while preventing the opposing team from shooting through their own hoop. A field goal is worth two points, unless made from behind the three-point line, when it is worth three. After a foul, timed play stops and the player fouled or designated to shoot a technical foul is given one, two or three one-point free throws. The team with the most points at the end of the game wins, but if regulation play expires with the score tied, an additional period of play (overtime) is mandated."

In [3]: ao._1929
Out[3]: '1929 (MCMXXIX) was a common year starting on Tuesday of the Gregorian calendar, the 1929th year of the Common Era (CE) and Anno Domini (AD) designations, the 929th year of the 2nd\xa0millennium, the 29th year of the 20th\xa0century, and the 10th and last year of the 1920s decade.'

In [4]: ao.apple, ao.banana, ao.coconut
Out[4]:
('An apple is a round, edible fruit produced by an apple tree. Apple trees are cultivated worldwide and are the most widely grown species in the genus Malus. The tree originated in Central Asia, where its wild ancestor, Malus sieversii, is still found. Apples have been grown for thousands of years in Asia and Europe and were introduced to North America by European colonists. Apples have religious and mythological significance in many cultures, including Norse, Greek, and European Christian tradition.',
 'A banana is an elongated, edible fruit – botanically a berry – produced by several kinds of large herbaceous flowering plants in the genus Musa. In some countries, bananas used for cooking may be called "plantains", distinguishing them from dessert bananas. The fruit is variable in size, color, and firmness, but is usually elongated and curved, with soft flesh rich in starch covered with a rind, which may be green, yellow, red, purple, or brown when ripe. The fruits grow upward in clusters near the top of the plant. Almost all modern edible seedless (parthenocarp) bananas come from two wild species\xa0– Musa acuminata and Musa balbisiana. The scientific names of most cultivated bananas are Musa acuminata, Musa balbisiana, and Musa × paradisiaca for the hybrid Musa acuminata × M.\xa0balbisiana, depending on their genomic constitution. The old scientific name for this hybrid, Musa sapientum, is no longer used.',
 'The coconut tree is a member of the palm tree family (Arecaceae) and the only living species of the genus Cocos. The term "coconut" can refer to the whole coconut palm, the seed, or the fruit, which botanically is a drupe, not a nut. The name comes from the old Portuguese word coco, meaning "head" or "skull", after the three indentations on the coconut shell that resemble facial features. They are ubiquitous in coastal tropical regions and are a cultural icon of the tropics.')
```
