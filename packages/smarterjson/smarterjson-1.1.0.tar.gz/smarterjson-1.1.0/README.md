# Smarterjson智能json

a python package, **smarter than python's json**\
一个python包，**比python的json更加智能**

code show\
代码演示
```python
import smarterjson

smarterjson.write({"python": "hello"}, fp="smarterjson.json")
smarterjson.read(("python",), fp="smarterjson.json", return_type=str)
smarterjson.append({"C++": "world"}, fp="smarterjson.json")
smarterjson.exist("C++", fp="smarterjson.json")
smarterjson.revise(("C++",), "good", fp="smarterjson.json")

smarterjson.father("hello", fp="smarterjson.json")
smarterjson.parent("good", fp="smarterjson.json")
```