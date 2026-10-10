# 第一次作业 (Homework 1)

操作系统课程第一次作业代码，共两道编程题。

| 文件 | 对应题目 | 说明 | 编译运行 |
|---|---|---|---|
| `fib_fork.c` | 题 5 | 使用 `fork()` 创建子进程生成并打印 Fibonacci 序列，父进程 `wait()` 等待 | Linux/WSL 下编译：`gcc fib_fork.c -o fib_fork && ./fib_fork 5` |
| `fib_thread.c` | 题 6 | 使用 Pthread 创建工作线程，将 Fibonacci 序列写入共享数组，父线程 `pthread_join` 后输出 | `gcc fib_thread.c -o fib_thread -lpthread && ./fib_thread 5` |

> 注：`fib_fork.c` 依赖 `fork()` / `wait()` / `<unistd.h>` / `<sys/wait.h>`，为 POSIX 系统调用，需在 Linux、WSL 或类 Unix 环境下编译；Windows MinGW 原生不支持。
