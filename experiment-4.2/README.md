# 实验 4.2：Linux 交接

当前程序与报告草稿尚未在 Linux 实测。请在 Linux 终端执行：

```bash
cd caozuoxitong/experiment-4.2
gcc -std=c11 -Wall -Wextra -O2 producer_consumer.c -pthread -o pc
./pc
```

检查生产、消费各 20 次，消费顺序为 1 至 20，最后输出 PASS；保存真实运行截图，在 report-draft.pdf 中补充实际运行环境、结果分析和截图。并发输出顺序可能不同。不得将预期结果写成实测结果。报告中的读者—写者问题目前为伪代码。
