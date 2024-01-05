def mylog(type):
    def decorator(func):
        def infunc(*args,**kwargs):
            if type=="文件": 
                print("文件中:日志纪录")
            else: 
                print("控制台:日志纪录")
            return func(*args,**kwargs)
        return infunc
    return decorator
@mylog("文件") 
def func(a,b):
    print("使用功能2",a,b)
if __name__ == '__main__':
    func(100,200)