# 操作系统实验 - 第三章 进程控制与进程调度

## 实验内容

### 实验3.1：进程的创建

| 文件 | 说明 |
|------|------|
| `fork_demo.c` | 使用 fork() 创建子进程，父子进程分别输出 PID、PPID 及退出状态 |
| `exec_demo.c` | 子进程调用 exec 函数族执行系统命令 ls |

### 实验3.2：进程调度算法的模拟

| 文件 | 说明 |
|------|------|
| `scheduler.c` | 模拟三种进程调度算法：FCFS、时间片轮转(RR)、动态优先级调度 |

## 编译运行

```bash
# 实验3.1 - 程序1
gcc fork_demo.c -o fork_demo
./fork_demo

# 实验3.1 - 程序2
gcc exec_demo.c -o exec_demo
./exec_demo

# 实验3.2 - 调度算法模拟
gcc scheduler.c -o scheduler
./scheduler
```

## 实验环境

- Linux 操作系统
- GCC 编译器
- VS Code 编辑器

## 作者

- 姓名：张三
- 学号：20210001
- 指导教师：王老师
