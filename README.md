# SM3_length_attack
个人完成。

# 代码原理
对任意的r1，进行填充得到r1||padding，

构造h1=SM3(r1||padding,IV),h2=SM3(r1||padding||r2,IV),h3=SM3(r2,iv),其中iv=h1=SM3(r1||padding,IV),

此时只需判断h2和h3是否相等即可，若相等则表明长度扩展攻击成功。

![image](https://user-images.githubusercontent.com/105580300/181866779-a8a11629-25d2-40a2-923d-b25f56bf0d33.png)


# 代码解释
hex_to_bin函数将字符串的十六进制表示转化为进制：

![image](https://user-images.githubusercontent.com/105580300/181905173-077e5591-a9a7-4a16-ab57-75ed2b18ac9b.png)

tianchong函数将明文长度填充为512bit的整数倍，填充方法为：

对于原长为l比特的消息，首先将比特“1”添加到消息末尾，，再添加k个“0”，k是满足l+k+1 = 448 mod 512的最小非负整数。

然后再添加一个64比特的字符串，该字符串是长度l的二进制表示。

![image](https://user-images.githubusercontent.com/105580300/181905205-6eb6c309-b70b-41b0-a6e2-6d022047174d.png)

主函数操作为：

![image](https://user-images.githubusercontent.com/105580300/181905345-1fce120e-5109-4aae-b944-7bc045c3e562.png)

# 代码运行结果
直接点击运行即可。

![image](https://user-images.githubusercontent.com/105580300/181866824-4576c9bc-1706-4160-933f-cab1a677ae01.png)
至此，SM3的长度扩展攻击运行成功！
