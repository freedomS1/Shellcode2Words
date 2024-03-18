# Shellcode2Words

------

This project was inspired by Shhhloader(https://github.com/icyguider/Shhhloader).I extracted the function points from the project to facilitate shellcode conversion.

We can use any dictionary to randomly convert shellcode.You can customize the number of NOPs you want to add to the shellcode header.

![image-20240318201426359](C:\Users\j\AppData\Roaming\Typora\typora-user-images\image-20240318201426359.png)

```
python3 main.py beacon.bin -nop n 
```

