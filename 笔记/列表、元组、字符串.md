

# 列表

首先要知道列表怎么定义的

`列表 = [变量]`，这其中的变量可以用数值也可以用字符，要注意的是字符串要带上引号`""`

```
name = ['ys','GIT','sysu']
print('hello '+name[0].title())
print('hello '+name[1].title())
print('hello '+name[2].title())
```

上述代码的输出为：

~~~python
hello Ys
hello Git
hello Sysu
~~~

### 列表的性质

#### 插入

##### `append`

是将元素插入到列表的尾端，通常用于导入到一个新的列表，举个例子：

```
number = []
for j in range(1, 11):
    a = j ** 2
    number.append(a)
    # number[j - 1] = a试图通过 number[j] 将值分配给列表 number 的索引 j，
    # 但是 number 是一个空列表，没有任何元素。
    # 因此，你需要使用 append() 方法将值添加到列表末尾，而不是尝试直接分配给索引。
    print(f'{j}^{j}={j ** 2}')
print(number)
```

**注意**：这里为什么选择利用`append`函数插入，如果采用直接赋值的方法，会出现错误，因为不能将数值直接赋给索引。

##### `insert`

使用insert插入列表的时候，要注意插入的位置，什么意思呢？就是说`insert`插入元素看的是给定的角标值：

```
visitors = ['mama','baba','sister']
visitors.insert(0,'firest')
visitors.insert(3,'second')
visitors.append('third')
print(visitors)
```

输出结果为：

~~~
['firest', 'mama', 'baba', 'second', 'wuhu', 'third']
~~~

**注意**:`insert`在选择插入的位置时是从***“0”***开始的

#### 删除

##### `del`

`del`语句在使用的时候，用法前提与`insert`一样，即提前知道要操作的数值的索引。



~~~
number = []
for j in range(1, 11):
	a = j**2
	number.append(a)
print(number)
# del number(2)
~~~

以上述代码为例，原本的输出结果为：

~~~
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
~~~

加入相关代码后：

`[1, 4, 16, 25, 36, 49, 64, 81, 100]`

##### `pop`

这个方法默认是用于删除列表最后的元素，区别于`del`的用法，`pop`在删除的时候可以找一变量将删除的值储存起来。

```
#example
moods = ['happy'，'sad','miss her']
mood_pop = moods.pop()
print(moods)
print(mood_pop)
```

结果如下：

```
['happy', 'sad']
miss her
```

这时可以运用这个变量去做其他的事情，而采用`del`的话，会直接将这个变量给删除掉，无法再利用，这也许可以解释为什么`del`在用的时候没有用额外的变量接受删掉的值。

同样的，在使用`pop`函数的时候，如果知道元素的具体索引值，也可以直接在圆括号内填入，将其删除。

##### `remove`

`remove`函数在使用时要求知道要删除元素在列表中具体代表什么。视情况而定，判断需不需要再找一个额外的变量来接收删掉的值。

#### 列表的操作

##### 遍历

对于列表的遍历，通常情况下采用的是`for`循环

~~~
# example
animals = ['pig','wolf','chicken']
for animal in animals:
	print(animal)
~~~

输出结果为：

```
pig
wolf
chicken
```

同理，也可以采用下标索引的方式进行遍历：

```
animals = ['pig','wolf','chicken']
for i in range(3):
	print(animals[i])
```

输出结果与上述结果相同，唯一要注意的是通过下标索引要注意索引值的范围，不能漏也不能少。

###### 切片操作

切片操作，类似于`range()`函数的用法在遍历里面重新讲了一遍，无非就是从某个位置开始，一直取值到特定位置停下。

##### 排序

先介绍一种对于列表元素的读法，正常情况下，我们要读取列表中的元素时要关注索引值是从**0**开始的，如果倒着读呢？诶，这个时候索引就是从**-1**开始的了。

```
#example
animals = ['pig','wolf','chicken']
for i in range(3):
	print(animals[i])
print('-----------')
print(animals[-1])
```

最后一行的输出就只包括`chicken`，采用这种方法可以实现对列表的反序读取。

```
animals = ['pig','wolf','chicken']
for i in range(-1,-4,-1):
	print(animals[i])
```

结果为：

```
chicken
wolf
pig
```

既然提到了反序，实际上python自带的有相关的排序函数：`sort`和`sorted`

###### `sort`

`sort`函数对列表元素的排序是永久性的，即排序完之后，无法再恢复到原来的顺序，用法为`list.sort(#根据需求判断是否要填入reverse=True)`,**注意**：倘若不加圆括号内的代码，则默认为按照升序排列，加上代码则是降序排列。

###### `sorted`

`sorted`对列表的排序是临时的，临时的怎么理解呢？这样说吧，`sorted`可以让你按照一定的顺序去重新排列已有的列表，同时不更改原列表的顺序。

干说无用，来看几个例子吧

```
#example
moods = ['sad','happy','excellent','missed']
moods.sort()
print(moods)
moods = ['sad','happy','excellent','missed']
print(sorted(moods))
print(moods)
```

上述代码的输出为

![image-20240605003451755](/Users/yangsai/Library/Application Support/typora-user-images/image-20240605003451755.png)

可以看到，再经过`moods.sort()`处理后，`moods`原有的元素被改变，而对于`sorted()`处理后，`moods`的元素照旧。

这里需要注意的是，如果在4，5之间加上代码`print(moods.sort())`,系统会打印出`None`，这是为什么？

> `sort()` 方法是 **原地修改** 的方法，这意味着它直接修改原始列表，而不是创建一个新的副本。`sort()` 方法**不**返回任何值。它只是修改原始列表，不会创建新的列表。

##### 列表解析

这是一种语法，用一行代码包含几行代码，从而达到简化代码的目的，具体的格式为：

> 变量名称 = [某一变量进行的操作 具体操作]

这里要注意***“操作”***和***“具体操作”***之间要留有空格

```
#example
scores = [score**2 for score in range(9,12)]
print(scores)
```

输出结果为

```
[81, 100, 121]
```

显然这种语法可以在一定程度上缩减代码的复杂程度。

##### 总结一下

经过上述的学习，很难发现不了一些规律吧。

> 部分函数的用法都与函数的性质有关，比如说，类似于`moods.sort()`、`moods.pop()`等,这些直接在变量名后面加上`.+Name`的操作会直接修改列表的原有属性，而如果不新设置一个变量去承接修改的值，那么这个值就会消失。

## 附录（常见的函数及操作）

| 方法                    | 功能                                     |
| :---------------------- | ---------------------------------------- |
| list.append(obj)        | 在列表末尾添加新的对象                   |
| list.extend(seq)        | 在列表末尾一次性追加另一个序列中的多个值 |
| list.insert(index, obj) | 将对象插入列表                           |
| list.index(obj)         | 从列表中找出某个值第一个匹配项的索引位置 |
| list.count(obj)         | 统计某个元素在列表中出现的次数           |
| list.remove(obj)        | 移除列表中某个值的第一个匹配项           |
| list.pop(obj=list[-1])  | 移除列表中的一个元素，并返回该元素的值   |
| sort()                  | 对原列表进行排序                         |
| reverse()               | 反向存放列表元素                         |
| cmp(list1,  list2)      | 比较两个列表的元素                       |
| len(list)               | 求列表元素个数                           |
| max(list)               | 返回列表元素的最大值                     |
| min(list)               | 返回列表元素的最小值                     |
| list(seq)               | 将元组转换为列表                         |
| sum(list)               | 对数值型列表元素求和                     |

# 元组

## 定义

元组与列表的明显的区别在于元组的定义用的是圆括号`()`而不是中括号`[]`

> 实际上，对元组的定义离不开的是——“**，**”，可以对下面的代码进行操作，尝试一下。

并且元组里面的元素是不可修改的，但是并不意味着承载元组的变量不可以重新赋值

```
#example
moods = ('sad','happy','angry')
print(moods)
moods = ('sadness','happinese','anger')
print(moods)
# 尝试修改元组里面的元素
# moods(1) = 'unhappy'
```

输出结果为：

```
('sad', 'happy', 'angry')
('sadness', 'happinese', 'anger')
# moods(1) = 'unhappy'
    ^^^^^^^^
SyntaxError: cannot assign to function call here.
```

可以看出，倘若我们尝试去修改元组里面的自带的元素，编译器会阻止这一行为，但是，如果我们直接对承接元组的变量重新定义，则不会有丝毫影响。

正如定义中所说的，如果我们不带上`()`,输出的结果也是一样的。

## 读取与切片

元组的读取与切片均与列表类似，只是形式不同而已。

## 元素的检索

1. 使用`index()`函数，来获取指定元素在元组中首次出现的下标。

   ```
   #example
   numbers = 2,3,4,5,6,3,4,7,8,6
   print(numbers.index(6))
   ```

​	上述代码的输出结果为`4`,为什么是4？是因为元组的索引也是从0开始的，而`6`首次出现的位置在`numbers`中属于第五个，5-1 = 4.因此输出的是`4`.

2. 使用`count`函数来统计元组中指定元素的出现次数

   ```
   #example
   print(numbers.count(6))
   ```

   显然上述代码的输出结果为`2`,编译器跑出来也是的。

3. 使用`in`运算符检索元组中是否存在某个元素

   ```
   #example
   sum = 0
   for i in range(7):
   	if (i in numbers):
   		print(f'{i} in  numbers')
   	sum += i
   print(sum)
   ```

   上述代码的输出结果为：

   ```
   2 in  numbers
   3 in  numbers
   4 in  numbers
   5 in  numbers
   6 in  numbers
   21
   ```

   实际上，如果只对单个元素是否在元组中，例如`1 in numbers `,编译器返回的是`False`,如果在的话，返回的就是`True`。

## 元素的删除

参考列表执行`del`语句

由于元组不支持对原有的元素进行改动，因此只能对整个元组进行操作，换句话说就是“不能同年同月同日生，但求同年同月同日死”。

# 字符串

在python中，字符串是由单引号`‘’`和双引号`“”`括起来的，但是效果是类似的。

```
#example
print('python')
print("python")
```

输出的结果都是`python`,这时候很难不去想如果是三个单引号呢？

尝试一下`print('''python''')`,在我手上这个编译器(***python.3.12***)里，输出依然是`python`。

## 字符串的相关操作

### 修改大小写

1. 对于只改变首字母的大小写，这个简单，其实就是属性值`title()`

```
#example
names = 'ys'
print(names.title())
#output Ys
```

看到这，我想尝试一下能不能对元组中的元素进行类似的操作，看元组是否真的是“不可改变的”

```
#example
names = 'lx','ys','cf'
for name in names:
    print(name.title(),end=',')
```

输出结果为：

```
Lx,Ys,C,
```

看来`title()`对元素的操作是在将元素提取出来之后进行的。

2. 如果想要改变字符串所有字母的大小写呢？这个时候要用到的函数是`upper`,相对应的，如果想全部改成小写呢？这个时候用到的是`lower`.

### 使用字符串

#### 认识常用的字符——“f”

如果我们要在变量中使用字符串就可以借助``f``的用法来实现这一目的。

```
#example
mood = 'sad'
name = 'ys'
print(f'{name.title()} is {mood}')
```

输出结果为：

<img src="/Users/yangsai/Library/Application Support/typora-user-images/image-20240606233404122.png" alt="image-20240606233404122" style="zoom:50%;" />

这种写法的好处是不需要再加一些修饰，例如`+`之类的，而且好记（实不相瞒我只对这一种输出方式比较熟悉）。

> 查看资料，这种语法好像是3.6版本才开始引入的，更新者真是天才！

### 一般操作

#### 分片

这种说法其实就是将字符串中的每个字符都遍历一遍或者进行所谓的切片操作。

```
#example
name = '为中华之崛起而读书'
print(name[1:3])
print(name[:])
print(name[-1:-9:-1])
```

输出结果为：

<img src="/Users/yangsai/Library/Application Support/typora-user-images/image-20240606234114781.png" alt="image-20240606234114781" style="zoom:50%;" />

看着有点眼熟，不确定再看一眼。这种方法很难不让人联想到`range`函数吧，完全就是`range`函数再就业嘛。

#### 连接字符

最常见也最简单的就是用`+`进行连接

```
print('hello '+'world')
#在hello后面加了一个空格，目的是为了美观，如果不加空格，那么两个字符会连在一起输出。
```

#### 重复`*`

说白了就是将这个字符串/字符重复多少次

````
#example
print('hello'*3)
````

### 关系运算

单字符间的比较

> 单个字符/字符串进行的比较是按照字符的ACSII码值进行的比较

````
#example
print('a' == 'a')
print('a' == 'A')
print('0' > '1')
````

输出结果为：

<img src="/Users/yangsai/Library/Application Support/typora-user-images/image-20240606235604108.png" alt="image-20240606235604108" style="zoom:50%;" />

可见字符/字符串间的比较只会返回布尔值。

### 成员运算

1. `in`和`not in`

其实就是判断字符串之间是否存在包含的关系

[参考](元素的删除)

2. `find`查找

   当我们需要在茫茫字符海中找到我们想要的ta时，不经遍漫漫长道，未识千人千面，怎知ta是对的人。

   `find`就是这样一个苦情的函数，它会将字符串中的每一个字符看过一遍，确定符合我们要求的字符。

   ````
   #example
   s1="beijing xi'an tianjin beijing chongqing"
   s1.find("beijing")
   s1.find("beijing",3)
   s1.find("beijing",3,20)
   
   ````

   输出结果为：

   <img src="/Users/yangsai/Library/Application Support/typora-user-images/image-20240607001218127.png" alt="image-20240607001218127" style="zoom:50 %;" />

   诶，这输出的都是什么牛马？别急，哼，白马，定叫他有来无回！

   > 代码 `sl.find("beijing")` 会查找字符串 `sl` 中子串 "beijing" 第一次出现的位置。由于 "beijing" 出现在开头，所以函数会返回 `0`。
   >
   > 代码 `sl.find("beijing", 3)` 指定了额外的参数 `3`，代表从字符串的第 3 个字符 (索引为 2) 开始查找。因此，函数会找到第二个 "beijing" ，并返回它的位置，也就是 `22` (索引为 21)。
   >
   > 代码 `sl.find("beijing", 3, 20)` 不仅指定了子串，还限定了搜索的范围。函数只会在索引为 3 到 19 (一共 17 个字符) 的范围内查找 "beijing"。由于 "beijing" 不在这个范围内，所以函数会返回 `-1` 表示没找到。
