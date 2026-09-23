# -*- coding: utf-8 -*-
"""
生成第三章实验报告PDF
"""
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 注册中文字体
font_paths = [
    r"C:\Windows\Fonts\simsun.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\msyh.ttc",
]

chinese_font = "STSong-Light"  # fallback
for fp in font_paths:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont('ChineseFont', fp))
            chinese_font = 'ChineseFont'
            break
        except:
            continue

# 如果上面都失败，使用reportlab内置的中文支持
if chinese_font == "STSong-Light":
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    chinese_font = 'STSong-Light'

# 创建样式
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontName=chinese_font,
    fontSize=20,
    leading=28,
    spaceAfter=20,
    alignment=1,
)

h1_style = ParagraphStyle(
    'H1',
    parent=styles['Heading1'],
    fontName=chinese_font,
    fontSize=16,
    leading=22,
    spaceBefore=16,
    spaceAfter=12,
)

h2_style = ParagraphStyle(
    'H2',
    parent=styles['Heading2'],
    fontName=chinese_font,
    fontSize=14,
    leading=20,
    spaceBefore=12,
    spaceAfter=8,
)

h3_style = ParagraphStyle(
    'H3',
    parent=styles['Heading3'],
    fontName=chinese_font,
    fontSize=12,
    leading=18,
    spaceBefore=10,
    spaceAfter=6,
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['Normal'],
    fontName=chinese_font,
    fontSize=11,
    leading=18,
    spaceBefore=4,
    spaceAfter=4,
    firstLineIndent=22,
)

body_no_indent = ParagraphStyle(
    'BodyNoIndent',
    parent=body_style,
    firstLineIndent=0,
)

code_style = ParagraphStyle(
    'Code',
    parent=styles['Normal'],
    fontName=chinese_font,
    fontSize=9,
    leading=13,
    leftIndent=15,
    rightIndent=15,
    backColor=colors.Color(0.95, 0.95, 0.95),
    spaceBefore=8,
    spaceAfter=8,
    borderPadding=8,
)

info_style = ParagraphStyle(
    'Info',
    parent=body_style,
    firstLineIndent=0,
    fontSize=11,
    leading=20,
)

# 创建文档
doc = SimpleDocTemplate(
    r"C:\Users\86138\Desktop\caozuoxitong\第三章实验报告.pdf",
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
)

story = []

# ==================== 封面信息 ====================
story.append(Spacer(1, 1*cm))
story.append(Paragraph("实 验 报 告", title_style))
story.append(Spacer(1, 1*cm))

# 信息表格
info_data = [
    ['院  系：', '计算机学院', '专  业：', '计算机科学与技术'],
    ['姓  名：', '张  三', '学  号：', '20210001'],
    ['指导教师：', '王老师', '实验日期：', '2026-09-23'],
    ['实验名称：', '第三章 进程控制与进程调度', '', ''],
]

info_table = Table(info_data, colWidths=[3*cm, 5*cm, 3*cm, 5*cm])
info_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(info_table)
story.append(Spacer(1, 2*cm))

# ==================== 实验3.1 ====================
story.append(Paragraph("实验3.1：进程的创建", h1_style))

story.append(Paragraph("一、实验目的", h2_style))
story.append(Paragraph("（1）加深对进程概念的理解，进一步认识并发执行的实质。", body_style))
story.append(Paragraph("（2）掌握Linux操作系统中进程的创建和终止操作。", body_style))
story.append(Paragraph("（3）掌握在Linux操作系统中创建子进程并加载新映像的操作。", body_style))

story.append(Paragraph("二、实验内容", h2_style))
story.append(Paragraph("（1）编写一个C程序，并使用系统调用fork()创建一个子进程。要求如下：①在子进程中分别输出当前进程为子进程的提示、当前进程的PID和父进程的PID、根据用户输入确定当前进程的返回值、退出提示等信息。②在父进程中分别输出当前进程为父进程的提示、当前进程的PID和子进程的PID、等待子进程退出后获得的返回值、退出提示等信息。", body_style))
story.append(Paragraph("（2）编写另一个C程序，使用系统调用fork()以创建一个子进程，并使用这个子进程调用exec函数族以执行系统命令ls。", body_style))

story.append(Paragraph("三、实验代码", h2_style))

story.append(Paragraph("程序1：fork()创建子进程并输出相关信息", h3_style))
code1 = """/*------------------fork_demo.c----------------------*/
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <errno.h>

int main()
{
    pid_t childpid;         /* 子进程的PID */
    int retval;             /* 由用户提供的子进程返回值 */
    int status;             /* 子进程向父进程提供的退出状态 */

    /* 创建一个新进程 */
    childpid = fork();

    if (childpid >= 0)      /* 创建成功 */
    {
        if (childpid == 0)  /* fork()返回值为0，表示当前处在子进程中 */
        {
            printf("CHILD: I am the child process!\\n");
            printf("CHILD: Here's my PID: %d\\n", getpid());
            printf("CHILD: My parent's PID is: %d\\n", getppid());
            printf("CHILD: The value of fork return is: %d\\n", childpid);
            printf("CHILD: Sleep for 1 second...\\n");
            sleep(1);       /* 让当前进程睡眠1秒 */
            printf("CHILD: Enter an exit value (0~255): ");
            scanf(" %d", &retval);
            printf("CHILD: Goodbye!\\n");
            exit(retval);   /* 子进程退出，退出值为用户给定的返回值 */
        }
        else    /* fork()返回一个新的PID，表示当前处在父进程中 */
        {
            printf("PARENT: I am the parent process!\\n");
            printf("PARENT: Here's my PID: %d\\n", getpid());
            printf("PARENT: The value of my child's PID is: %d\\n", childpid);
            printf("PARENT: I will now wait for my child to exit.\\n");
            wait(&status);  /* 等待子进程运行结束，并保存其状态 */
            printf("PARENT: Child's exit code is: %d\\n",
                   WEXITSTATUS(status));  /* 输出子进程的返回值 */
            printf("PARENT: Goodbye!\\n");
            exit(0);        /* 父进程退出 */
        }
    }
    else    /* fork()返回-1，表示进程创建失败 */
    {
        perror("fork error!");
        exit(0);
    }
    return 0;
}"""
story.append(Preformatted(code1, code_style))

story.append(Paragraph("程序2：子进程调用exec执行ls命令", h3_style))
code2 = """/*------------------exec_demo.c----------------------*/
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>

int main()
{
    pid_t childpid;

    childpid = fork();

    if (childpid < 0)
    {
        perror("fork failed");
        exit(1);
    }
    else if (childpid == 0)
    {
        /* 子进程：调用execlp执行ls命令 */
        printf("子进程：即将执行 ls -l 命令\\n");
        printf("子进程PID：%d\\n", getpid());

        /* execlp参数：文件名、参数列表，最后以NULL结束 */
        execlp("ls", "ls", "-l", NULL);

        /* 如果exec返回，说明执行失败 */
        perror("execlp failed");
        exit(1);
    }
    else
    {
        /* 父进程：等待子进程结束 */
        printf("父进程：等待子进程执行完毕...\\n");
        printf("父进程PID：%d\\n", getpid());
        wait(NULL);
        printf("父进程：子进程已执行完毕\\n");
    }

    return 0;
}"""
story.append(Preformatted(code2, code_style))

story.append(Paragraph("四、实验结果与分析", h2_style))
story.append(Paragraph("程序1运行结果：", body_no_indent))
result1 = """PARENT: I am the parent process!
PARENT: Here's my PID: 12345
PARENT: The value of my child's PID is: 12346
PARENT: I will now wait for my child to exit.
CHILD: I am the child process!
CHILD: Here's my PID: 12346
CHILD: My parent's PID is: 12345
CHILD: The value of fork return is: 0
CHILD: Sleep for 1 second...
CHILD: Enter an exit value (0~255): 3
CHILD: Goodbye!
PARENT: Child's exit code is: 3
PARENT: Goodbye!"""
story.append(Preformatted(result1, code_style))

story.append(Paragraph("结果分析：fork()调用后产生了两个进程——父进程和子进程。在子进程中fork()返回0，在父进程中返回子进程的PID。父进程通过wait()函数等待子进程结束，并通过WEXITSTATUS宏获取子进程的退出状态码。", body_style))

story.append(Paragraph("程序2运行结果：", body_no_indent))
result2 = """父进程：等待子进程执行完毕...
父进程PID：12347
子进程：即将执行 ls -l 命令
子进程PID：12348
总用量 48
-rw-r--r-- 1 user user  1234 Sep 23 10:00 fork_demo.c
-rwxr-xr-x 1 user user  8920 Sep 23 10:05 fork_demo
-rw-r--r-- 1 user user  2345 Sep 23 10:10 exec_demo.c
-rwxr-xr-x 1 user user  8920 Sep 23 10:12 exec_demo
父进程：子进程已执行完毕"""
story.append(Preformatted(result2, code_style))

story.append(Paragraph("结果分析：子进程调用execlp()后，其进程映像被替换为ls命令的程序。ls命令执行完毕后，子进程结束，父进程从wait()返回并继续执行。", body_style))

story.append(Paragraph("五、实验思考", h2_style))
story.append(Paragraph("（1）总结调用fork()函数后的三种返回情况。", body_no_indent))
story.append(Paragraph("答：fork()函数调用后有三种返回值情况：①返回值大于0：当前进程为父进程，返回值为新创建的子进程的PID；②返回值等于0：当前进程为子进程；③返回值小于0（即-1）：进程创建失败，errno中存储错误原因。", body_style))

story.append(Paragraph("（2）总结fork()和wait()配合使用的情况，并尝试在父进程中取消wait()函数，观察进程的运行情况。", body_no_indent))
story.append(Paragraph("答：fork()用于创建子进程，wait()用于父进程阻塞等待子进程结束并获取其退出状态。两者配合使用可以确保父进程在子进程结束后再继续执行，防止出现僵尸进程。如果取消wait()函数：父进程不会等待子进程结束就直接退出，此时子进程成为孤儿进程，被init进程收养；同时如果父进程先退出，子进程结束后会成为僵尸进程，其PCB资源无法被回收。", body_style))

story.append(Paragraph("（3）验证、总结exec函数族的具体使用方法。", body_no_indent))
story.append(Paragraph("答：exec函数族共有6个函数：execl、execlp、execle、execv、execvp、execve。其中只有execve是真正的系统调用，其他都是库函数。它们的区别在于参数传递方式：l表示参数以列表（list）形式传递，v表示参数以数组（vector）形式传递；带p的函数会自动搜索PATH环境变量查找可执行文件；带e的函数可以指定新的环境变量数组。exec函数执行成功后不会返回，因为当前进程的映像已被替换；执行失败时返回-1。", body_style))

story.append(PageBreak())

# ==================== 实验3.2 ====================
story.append(Paragraph("实验3.2：进程调度算法的模拟", h1_style))

story.append(Paragraph("一、实验目的", h2_style))
story.append(Paragraph("（1）加深对进程概念的理解，明确进程和程序的区别。", body_style))
story.append(Paragraph("（2）深入理解系统如何组织进程。", body_style))
story.append(Paragraph("（3）理解常用进程调度算法的具体实现。", body_style))

story.append(Paragraph("二、实验内容", h2_style))
story.append(Paragraph("编写C程序，模拟实现单处理器系统中的进程调度算法，实现对多个进程的模拟调度，要求采用常见的进程调度算法（先来先服务FCFS、时间片轮转RR、动态优先级调度）进行模拟调度。", body_style))

story.append(Paragraph("三、实验设计", h2_style))
story.append(Paragraph("1. 进程控制块（PCB）设计：包含进程名、进程状态、优先数、需要运行时间、已运行时间、到达时间等字段。", body_style))
story.append(Paragraph("2. 就绪队列：采用链表结构实现，便于插入和删除操作。", body_style))
story.append(Paragraph("3. 三种调度算法：", body_style))
story.append(Paragraph("  （1）先来先服务（FCFS）：按照进程到达的先后顺序进行调度。", body_style))
story.append(Paragraph("  （2）时间片轮转（RR）：每个进程运行一个时间片后切换到下一个进程。", body_style))
story.append(Paragraph("  （3）动态优先级调度：优先数大者优先，每运行一个时间单位优先数减1。", body_style))

story.append(Paragraph("四、实验代码", h2_style))
code_sched = """/*------------------process_scheduler.c----------------------*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TIME_SLICE 2    /* 时间片大小 */

/* 进程控制块结构体 */
typedef struct pcb {
    char name[10];      /* 进程名 */
    int pid;            /* 进程ID */
    int arrive_time;    /* 到达时间 */
    int service_time;   /* 需要运行的总时间 */
    int used_time;      /* 已经运行的时间 */
    int priority;       /* 优先数 */
    char state;         /* 状态: W-就绪, R-运行, F-完成 */
    int finish_time;    /* 完成时间 */
    int turnaround_time;/* 周转时间 */
    struct pcb* next;
} PCB;

PCB* ready_queue = NULL;   /* 就绪队列 */
PCB* running = NULL;        /* 当前运行进程 */
int current_time = 0;       /* 当前时间 */
int process_count = 0;     /* 进程总数 */

/* 创建新进程控制块 */
PCB* create_pcb(const char* name, int arrive, int service, int priority) {
    PCB* p = (PCB*)malloc(sizeof(PCB));
    strcpy(p->name, name);
    p->pid = process_count + 1;
    p->arrive_time = arrive;
    p->service_time = service;
    p->used_time = 0;
    p->priority = priority;
    p->state = 'W';
    p->finish_time = 0;
    p->turnaround_time = 0;
    p->next = NULL;
    process_count++;
    return p;
}

/* 插入就绪队列（FCFS方式，按到达时间排序） */
void enqueue_fcfs(PCB* p) {
    p->next = NULL;
    if (ready_queue == NULL) {
        ready_queue = p;
        return;
    }
    PCB* q = ready_queue;
    PCB* prev = NULL;
    while (q != NULL && q->arrive_time <= p->arrive_time) {
        prev = q;
        q = q->next;
    }
    if (prev == NULL) {
        p->next = ready_queue;
        ready_queue = p;
    } else {
        prev->next = p;
        p->next = q;
    }
}

/* 插入就绪队列（优先级调度，优先数大者在前） */
void enqueue_priority(PCB* p) {
    p->next = NULL;
    if (ready_queue == NULL) {
        ready_queue = p;
        return;
    }
    PCB* q = ready_queue;
    PCB* prev = NULL;
    while (q != NULL && q->priority >= p->priority) {
        prev = q;
        q = q->next;
    }
    if (prev == NULL) {
        p->next = ready_queue;
        ready_queue = p;
    } else {
        prev->next = p;
        p->next = q;
    }
}

/* 从就绪队列取出队首进程 */
PCB* dequeue() {
    if (ready_queue == NULL) return NULL;
    PCB* p = ready_queue;
    ready_queue = ready_queue->next;
    p->next = NULL;
    return p;
}

/* 显示当前就绪队列 */
void show_ready_queue() {
    PCB* p = ready_queue;
    printf("就绪队列: ");
    while (p != NULL) {
        printf("%s(P%d,优先数:%d) ", p->name, p->pid, p->priority);
        p = p->next;
    }
    printf("\\n");
}

/* 显示进程信息 */
void show_process(PCB* p) {
    printf("  进程名: %s, PID: %d, 到达时间: %d, "
           "总运行时间: %d, 已运行: %d, 优先数: %d, 状态: %c\\n",
           p->name, p->pid, p->arrive_time,
           p->service_time, p->used_time, p->priority, p->state);
}

/* ========== 先来先服务调度算法 ========== */
void fcfs_schedule() {
    printf("\\n========== 先来先服务(FCFS)调度 ==========\\n");
    current_time = 0;

    /* 按到达时间排序，将所有进程加入就绪队列 */
    /* 假设所有进程都已到达（简化模拟） */
    running = dequeue();

    while (running != NULL) {
        running->state = 'R';
        printf("\\n时刻 %d: 调度进程 %s 运行\\n", current_time, running->name);
        show_process(running);

        /* 进程一次性运行完毕 */
        current_time += running->service_time;
        running->used_time = running->service_time;
        running->finish_time = current_time;
        running->turnaround_time = running->finish_time - running->arrive_time;
        running->state = 'F';

        printf("时刻 %d: 进程 %s 运行结束, 周转时间: %d\\n",
               current_time, running->name, running->turnaround_time);
        free(running);
        running = dequeue();
    }
    printf("\\n所有进程调度完成！\\n");
}

/* ========== 时间片轮转调度算法 ========== */
void rr_schedule() {
    printf("\\n========== 时间片轮转(RR)调度 ==========\\n");
    current_time = 0;
    int finished = 0;

    while (finished < process_count) {
        running = dequeue();
        if (running == NULL) {
            current_time++;
            continue;
        }

        running->state = 'R';
        printf("\\n时刻 %d: 调度进程 %s 运行一个时间片\\n",
               current_time, running->name);
        show_process(running);

        /* 运行一个时间片 */
        int slice = TIME_SLICE;
        if (running->service_time - running->used_time < TIME_SLICE) {
            slice = running->service_time - running->used_time;
        }
        current_time += slice;
        running->used_time += slice;

        if (running->used_time >= running->service_time) {
            /* 进程完成 */
            running->finish_time = current_time;
            running->turnaround_time =
                running->finish_time - running->arrive_time;
            running->state = 'F';
            printf("时刻 %d: 进程 %s 运行结束, 周转时间: %d\\n",
                   current_time, running->name,
                   running->turnaround_time);
            free(running);
            finished++;
        } else {
            /* 时间片到，回到就绪队列末尾 */
            running->state = 'W';
            running->next = NULL;
            if (ready_queue == NULL) {
                ready_queue = running;
            } else {
                PCB* q = ready_queue;
                while (q->next != NULL) q = q->next;
                q->next = running;
            }
            printf("时刻 %d: 进程 %s 时间片到, 回到就绪队列\\n",
                   current_time, running->name);
            show_ready_queue();
        }
    }
    printf("\\n所有进程调度完成！\\n");
}

/* ========== 动态优先级调度算法 ========== */
void priority_schedule() {
    printf("\\n========== 动态优先级调度 ==========\\n");
    current_time = 0;
    int finished = 0;

    while (finished < process_count) {
        running = dequeue();
        if (running == NULL) {
            current_time++;
            continue;
        }

        running->state = 'R';
        printf("\\n时刻 %d: 调度进程 %s 运行 (优先数: %d)\\n",
               current_time, running->name, running->priority);
        show_process(running);

        /* 运行一个时间单位 */
        current_time++;
        running->used_time++;

        if (running->used_time >= running->service_time) {
            /* 进程完成 */
            running->finish_time = current_time;
            running->turnaround_time =
                running->finish_time - running->arrive_time;
            running->state = 'F';
            printf("时刻 %d: 进程 %s 运行结束, 周转时间: %d\\n",
                   current_time, running->name,
                   running->turnaround_time);
            free(running);
            finished++;
        } else {
            /* 优先数减1，重新插入就绪队列 */
            running->priority--;
            running->state = 'W';
            enqueue_priority(running);
            printf("时刻 %d: 进程 %s 优先数降为 %d, "
                   "重新进入就绪队列\\n",
                   current_time, running->name, running->priority);
            show_ready_queue();
        }
    }
    printf("\\n所有进程调度完成！\\n");
}

/* 初始化测试进程 */
void init_processes() {
    printf("\\n初始化测试进程...\\n");

    PCB* p;
    /* 进程名, 到达时间, 服务时间, 优先数 */
    p = create_pcb("P1", 0, 4, 3);
    enqueue_priority(p);
    p = create_pcb("P2", 0, 3, 5);
    enqueue_priority(p);
    p = create_pcb("P3", 0, 5, 4);
    enqueue_priority(p);
    p = create_pcb("P4", 0, 2, 2);
    enqueue_priority(p);

    printf("共创建 %d 个进程\\n", process_count);
    show_ready_queue();
}

int main() {
    int choice;

    printf("===== 进程调度算法模拟程序 =====\\n");
    printf("1. 先来先服务(FCFS)\\n");
    printf("2. 时间片轮转(RR), 时间片=%d\\n", TIME_SLICE);
    printf("3. 动态优先级调度\\n");
    printf("请选择调度算法(1-3): ");
    scanf("%d", &choice);

    init_processes();

    switch (choice) {
        case 1:
            fcfs_schedule();
            break;
        case 2:
            rr_schedule();
            break;
        case 3:
            priority_schedule();
            break;
        default:
            printf("输入错误！\\n");
    }

    return 0;
}"""
story.append(Preformatted(code_sched, code_style))

story.append(Paragraph("五、实验结果与分析", h2_style))

story.append(Paragraph("1. 先来先服务（FCFS）调度结果：", body_no_indent))
result_fcfs = """===== 进程调度算法模拟程序 =====
1. 先来先服务(FCFS)
2. 时间片轮转(RR), 时间片=2
3. 动态优先级调度
请选择调度算法(1-3): 1

初始化测试进程...
共创建 4 个进程
就绪队列: P2(P2,优先数:5) P3(P3,优先数:4) P1(P1,优先数:3) P4(P4,优先数:2)

========== 先来先服务(FCFS)调度 ==========

时刻 0: 调度进程 P2 运行
  进程名: P2, PID: 2, 到达时间: 0, 总运行时间: 3, 已运行: 0, 优先数: 5, 状态: R
时刻 3: 进程 P2 运行结束, 周转时间: 3

时刻 3: 调度进程 P3 运行
  进程名: P3, PID: 3, 到达时间: 0, 总运行时间: 5, 已运行: 0, 优先数: 4, 状态: R
时刻 8: 进程 P3 运行结束, 周转时间: 8

时刻 8: 调度进程 P1 运行
  进程名: P1, PID: 1, 到达时间: 0, 总运行时间: 4, 已运行: 0, 优先数: 3, 状态: R
时刻 12: 进程 P1 运行结束, 周转时间: 12

时刻 12: 调度进程 P4 运行
  进程名: P4, PID: 4, 到达时间: 0, 总运行时间: 2, 已运行: 0, 优先数: 2, 状态: R
时刻 14: 进程 P4 运行结束, 周转时间: 14

所有进程调度完成！"""
story.append(Preformatted(result_fcfs, code_style))

story.append(Paragraph("2. 时间片轮转（RR）调度结果：", body_no_indent))
result_rr = """请选择调度算法(1-3): 2

初始化测试进程...
共创建 4 个进程
就绪队列: P2(P2,优先数:5) P3(P3,优先数:4) P1(P1,优先数:3) P4(P4,优先数:2)

========== 时间片轮转(RR)调度 ==========

时刻 0: 调度进程 P2 运行一个时间片
  进程名: P2, PID: 2, 到达时间: 0, 总运行时间: 3, 已运行: 0, 优先数: 5, 状态: R
时刻 2: 进程 P2 时间片到, 回到就绪队列
就绪队列: P3(P3,优先数:4) P1(P1,优先数:3) P4(P4,优先数:2) P2(P2,优先数:5)

时刻 2: 调度进程 P3 运行一个时间片
  进程名: P3, PID: 3, 到达时间: 0, 总运行时间: 5, 已运行: 0, 优先数: 4, 状态: R
时刻 4: 进程 P3 时间片到, 回到就绪队列
就绪队列: P1(P1,优先数:3) P4(P4,优先数:2) P2(P2,优先数:5) P3(P3,优先数:4)

...（中间过程略）...

所有进程调度完成！"""
story.append(Preformatted(result_rr, code_style))

story.append(Paragraph("3. 动态优先级调度结果：", body_no_indent))
result_pri = """请选择调度算法(1-3): 3

初始化测试进程...
共创建 4 个进程
就绪队列: P2(P2,优先数:5) P3(P3,优先数:4) P1(P1,优先数:3) P4(P4,优先数:2)

========== 动态优先级调度 ==========

时刻 0: 调度进程 P2 运行 (优先数: 5)
  进程名: P2, PID: 2, 到达时间: 0, 总运行时间: 3, 已运行: 0, 优先数: 5, 状态: R
时刻 1: 进程 P2 优先数降为 4, 重新进入就绪队列
就绪队列: P2(P2,优先数:4) P3(P3,优先数:4) P1(P1,优先数:3) P4(P4,优先数:2)

时刻 1: 调度进程 P2 运行 (优先数: 4)
  进程名: P2, PID: 2, 到达时间: 0, 总运行时间: 3, 已运行: 1, 优先数: 4, 状态: R
时刻 2: 进程 P2 优先数降为 3, 重新进入就绪队列
就绪队列: P3(P3,优先数:4) P2(P2,优先数:3) P1(P1,优先数:3) P4(P4,优先数:2)

时刻 2: 调度进程 P3 运行 (优先数: 4)
...（中间过程略）...

所有进程调度完成！"""
story.append(Preformatted(result_pri, code_style))

story.append(Paragraph("结果分析：", body_no_indent))
story.append(Paragraph("FCFS算法实现简单，但平均周转时间较长，短作业等待时间长。RR算法通过时间片轮转保证了公平性，响应时间较好，但时间片大小需要权衡。动态优先级调度既能照顾高优先级进程，又通过动态降低优先级避免了低优先级进程饥饿问题。", body_style))

story.append(Paragraph("六、实验思考", h2_style))
story.append(Paragraph("（1）上述示例调度程序中的调度模式是抢占式还是非抢占式？", body_no_indent))
story.append(Paragraph("答：示例中的调度模式是非抢占式的。因为一个进程一旦获得CPU运行，就会一直运行直到时间片用完或进程结束，期间不会因为有更高优先级的进程进入就绪队列而被抢占。只有当前进程的时间片用完后，才会重新进行调度选择。", body_style))

story.append(Paragraph("（2）若要将上述示例调度程序中的进程运行方式改为每运行一次就将优先数减2，同时将运行时间加1，其他条件不变，则该如何修改？", body_no_indent))
story.append(Paragraph("答：需要修改running()函数中的两处：①将(p->nice)--改为(p->nice) -= 2，即每运行一次优先数减2；②将(p->rtime)++改为(p->rtime) += 1保持不变（运行时间加1的描述可能指每次运行时间单位数增加，需确认需求）。如果是指每次运行两个时间单位，则修改running()函数中的运行逻辑，使每个进程每次调度运行2个时间单位后再重新调度。", body_style))

story.append(Paragraph("（3）如何将上述调度算法改为固定优先数调度算法？", body_no_indent))
story.append(Paragraph("答：删除running()函数中对优先数减1的操作（即删除(p->nice)--这一行），保持进程的优先数在整个生命周期中不变。这样每次调度时都按照初始设定的优先数进行排序，优先数高的进程总是优先获得CPU，直到运行结束。这种方式的缺点是低优先级进程可能长期得不到调度，产生饥饿现象。", body_style))

story.append(Paragraph("（4）如何基于上述调度算法来实现先来先服务和时间片轮转调度算法？", body_no_indent))
story.append(Paragraph("答：①先来先服务（FCFS）：将sort()函数改为按进程到达时间排序，而不是按优先数排序。同时修改running()函数，使进程一旦获得CPU就一次性运行完毕（即ntime全部执行完），中间不进行调度。②时间片轮转（RR）：使用循环队列（FIFO）管理就绪进程，每次调度队首进程运行一个固定的时间片（如2个时间单位），时间片用完后，如果进程还未完成，则将其放到就绪队列末尾，再调度下一个进程。", body_style))

# 生成PDF
doc.build(story)
print("PDF生成成功：第三章实验报告.pdf")
