# 面向对象-类

## 类(class)：具有相同属性和方法的对象集合

> 可以尝试用函数的方法去理解，函数是根据选择的函数名称重复执行特定的操作
>
> 不过类针对的是变量本身的属性，函数侧重于执行的操作。

```
class ClassName:
	info.....			
```

看着像==c语言==里面的结构体。不同的是，`class`可以被继承，而`struct`没有这种属性。

在类里面可以封装函数，例如：

```
class food:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def printFood(self):
        print(f"{self.name}、{self.price}")


if __name__ == '__main__':
    food1 = food('apple',14)
    food1.printFood()
    food2 = food('banana',15)
    food2.printFood()
```

> 代码解释：
>
> 1. 在这串代码中，定义了一个`food`类，利用`_init_()`将两个属性`name`和`price`进行捆绑，这样操作使得后续用`food`命名的变量会拥有这两个属性，如`food1`和`food2`，在进行赋值的时候就要一一对应的配值。
> 2. `self`指代的是实例(food)本身，因此在类的封装中，可以直接用`self.name`和`self.price`来代表即将操作的变量。`self`不需要额外的赋值，python编译器会自己将`self`识别出来。
> 3. 类中函数的定义与一般的函数定义有所区别，即必须要包括`self`实例，这个值一般为默认值，不需要进行更改。

### 继承

继承，顾名思义就是从一个类那里把类所具备的属性继承过来

```
class 子代(父代)：
	// 基本属性（选）
	// 从父代那里调用
	父代名.__init__(self,父代属性)
```

借用上面的例子

```
class food:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class taste(food):
    def __init__(self, name, price, tasting):
        food.__init__(self, name, price)
        self.tasting = tasting

    def printFood(self):
        print(f"{self.name}的价格是{self.price}，吃起来感觉{self.tasting}")

if __name__ == '__main__':
    food1 = taste('apple',14,'good')
    food1.printFood()
    food2 = taste('banana',15,'bad')
    food2.printFood()
```

得到的结果是：

![image-20241013152006981](/Users/yangsai/Downloads/Markdown/笔记用图/image-20241013152006981.png)

由此扩展，python中对于类的扩展不仅仅表现为单继承，还能够从多个要素类中继承需要的属性。如果父代中提供的方法（函数）不能满足当下的需求，那么在子代中就可以重新将这一函数重新编写，即使拥有相同的变量名也不会影响。

### 私有化

类的私有化包括两个方面：属性私有化和类的私有方法。

私有化，即属性和方法只能在类的内部使用，不能从外部直接访问。

前者可以看作将要素私有化，后者则是将函数私有化。

方法都是相同的，在要素/函数前面加上双下划线`__`

```
class message:
    def __init__(self,name,message):
        self.__name = name
        self.message = message

    def printMessage(self):
        print(self.__name, self.message)
if __name__ == '__main__':
		 publicMessage = message('noname','往后余生')
     publicMessage.printMessage()
     print(publicMessage.__name, publicMessage.message)
```

输出的结果为：

```
noname 往后余生
print(publicMessage.__name, publicMessage.message)
          ^^^^^^^^^^^^^^^^^^^^
AttributeError: 'message' object has no attribute '__name'
```

> 代码解释：
>
> 可以看出调用类的内部输出函数`printMessage`可以将`name`属性完整的输出，但是从外部尝试进行打印操作`print`的时候发现无法访问。