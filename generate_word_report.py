# -*- coding: utf-8 -*-
"""
生成第三章实验报告 Word 版本
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ========== 页面设置 ==========
section = doc.sections[0]
section.top_margin = Cm(2.5)
section.bottom_margin = Cm(2.5)
section.left_margin = Cm(2.5)
section.right_margin = Cm(2.5)

# ========== 样式设置 ==========
style = doc.styles['Normal']
style.font.name = '宋体'
style.font.size = Pt(12)
style._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
style.paragraph_format.line_spacing = 1.5
style.paragraph_format.first_line_indent = Pt(24)

def set_run_font(run, name='宋体', size=12, bold=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if color:
        run.font.color.rgb = color

def add_title(text, level=0):
    """添加标题"""
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    if level == 0:
        set_run_font(run, '黑体', 18, bold=True)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif level == 1:
        set_run_font(run, '黑体', 16, bold=True)
    elif level == 2:
        set_run_font(run, '黑体', 14, bold=True)
    elif level == 3:
        set_run_font(run, '黑体', 12, bold=True)
    return p

def add_body(text, indent=True):
    """添加正文段落"""
    p = doc.add_paragraph()
    if not indent:
        p.paragraph_format.first_line_indent = Pt(0)
    run = p.add_run(text)
    set_run_font(run, '宋体', 12)
    return p

def add_image_placeholder(description):
    """添加图片占位符（醒目标注）"""
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Pt(0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f'【此处插入图片】')
    set_run_font(run, '黑体', 11, bold=True, color=RGBColor(0xC0, 0x00, 0x00))
    run2 = p.add_run(f'  {description}')
    set_run_font(run2, '楷体', 11, color=RGBColor(0xC0, 0x00, 0x00))
    # 添加边框效果（用底纹模拟）
    return p

def add_code_block(code_text):
    """添加代码块（等宽字体，带底纹）"""
    lines = code_text.split('\n')
    for line in lines:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Pt(0)
        p.paragraph_format.left_indent = Cm(1)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(line if line else ' ')
        run.font.name = 'Consolas'
        run.font.size = Pt(9)
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    # 空行
    doc.add_paragraph()

def add_info_table():
    """添加实验信息表"""
    table = doc.add_table(rows=4, cols=4)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    data = [
        ['院  系：', '计算机学院', '专  业：', '计算机科学与技术'],
        ['姓  名：', '张  三', '学  号：', '20210001'],
        ['指导教师：', '王老师', '实验日期：', '2026-09-23'],
        ['实验名称：', '第三章 进程控制与进程调度', '', ''],
    ]

    for i, row_data in enumerate(data):
        row = table.rows[i]
        for j, cell_text in enumerate(row_data):
            cell = row.cells[j]
            cell.text = ''
            p = cell.paragraphs[0]
            p.paragraph_format.first_line_indent = Pt(0)
            run = p.add_run(cell_text)
            set_run_font(run, '宋体', 12)
            # 合并最后一行后两个单元格
            if i == 3 and j == 2:
                cell.merge(row.cells[3])

    doc.add_paragraph()

# ========== 开始生成文档 ==========

# 标题
add_title('实 验 报 告', level=0)
doc.add_paragraph()

# 信息表
add_info_table()

# ==================== 实验3.1 ====================
add_title('实验3.1：进程的创建', level=1)

add_title('一、实验目的', level=2)
add_body('（1）加深对进程概念的理解，进一步认识并发执行的实质。')
add_body('（2）掌握Linux操作系统中进程的创建和终止操作。')
add_body('（3）掌握在Linux操作系统中创建子进程并加载新映像的操作。')

add_title('二、实验内容', level=2)
add_body('（1）编写一个C程序，并使用系统调用fork()创建一个子进程。要求如下：①在子进程中分别输出当前进程为子进程的提示、当前进程的PID和父进程的PID、根据用户输入确定当前进程的返回值、退出提示等信息。②在父进程中分别输出当前进程为父进程的提示、当前进程的PID和子进程的PID、等待子进程退出后获得的返回值、退出提示等信息。')
add_body('（2）编写另一个C程序，使用系统调用fork()以创建一个子进程，并使用这个子进程调用exec函数族以执行系统命令ls。')

add_title('三、实验代码', level=2)

add_title('程序1：fork_demo.c', level=3)
code1 = """#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <errno.h>

int main()
{
    pid_t childpid;         /* 子进程的PID */
    int retval;             /* 子进程返回值 */
    int status;              /* 子进程退出状态 */

    childpid = fork();       /* 创建新进程 */

    if (childpid >= 0)       /* 创建成功 */
    {
        if (childpid == 0)   /* 返回0 = 子进程 */
        {
            printf("CHILD: I am the child process!\\n");
            printf("CHILD: My PID: %d\\n", getpid());
            printf("CHILD: My parent's PID: %d\\n", getppid());
            printf("CHILD: fork returned: %d\\n", childpid);
            printf("CHILD: Sleep for 1 second...\\n");
            sleep(1);
            printf("CHILD: Enter exit value (0~255): ");
            scanf(" %d", &retval);
            printf("CHILD: Goodbye!\\n");
            exit(retval);
        }
        else                  /* 返回>0 = 父进程 */
        {
            printf("PARENT: I am the parent process!\\n");
            printf("PARENT: My PID: %d\\n", getpid());
            printf("PARENT: My child's PID: %d\\n", childpid);
            printf("PARENT: Waiting for child...\\n");
            wait(&status);
            printf("PARENT: Child exit code: %d\\n",
                   WEXITSTATUS(status));
            printf("PARENT: Goodbye!\\n");
            exit(0);
        }
    }
    else                       /* 返回-1 = 创建失败 */
    {
        perror("fork error!");
        exit(1);
    }
    return 0;
}"""
add_code_block(code1)

add_title('程序2：exec_demo.c', level=3)
code2 = """#include <stdio.h>
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
        /* 子进程：执行 ls -l 命令 */
        printf("[Child] Ready to run 'ls -l', PID = %d\\n", getpid());
        execlp("ls", "ls", "-l", NULL);
        perror("execlp failed");
        exit(1);
    }
    else
    {
        /* 父进程：等待子进程结束 */
        printf("[Parent] Waiting for child, PID = %d\\n", getpid());
        wait(NULL);
        printf("[Parent] Child finished.\\n");
    }
    return 0;
}"""
add_code_block(code2)

add_title('四、实验结果', level=2)

add_body('程序1编译运行：', indent=False)
add_body('编译命令：gcc fork_demo.c -o fork_demo', indent=False)
add_body('运行命令：./fork_demo', indent=False)

add_image_placeholder('插入 fork_demo.c 运行结果截图（包含父子进程输出、输入退出值3的完整终端截图）')

add_body('结果说明：fork()调用后产生父子两个进程。子进程中fork()返回0，父进程返回子进程PID。父进程通过wait()等待子进程结束，并用WEXITSTATUS获取子进程退出码。', indent=False)

doc.add_paragraph()

add_body('程序2编译运行：', indent=False)
add_body('编译命令：gcc exec_demo.c -o exec_demo', indent=False)
add_body('运行命令：./exec_demo', indent=False)

add_image_placeholder('插入 exec_demo.c 运行结果截图（包含父进程等待提示和子进程执行ls -l的文件列表输出）')

add_body('结果说明：子进程调用execlp()后，其进程映像被替换为ls命令程序。ls执行完毕后子进程结束，父进程从wait()返回继续执行。', indent=False)

add_title('五、实验思考', level=2)

add_body('（1）总结调用fork()函数后的三种返回情况。', indent=False)
add_body('答：fork()函数调用后有三种返回值情况：①返回值大于0：当前进程为父进程，返回值为新创建的子进程PID；②返回值等于0：当前进程为子进程；③返回值小于0（即-1）：进程创建失败，errno中存储错误原因。')

add_body('（2）总结fork()和wait()配合使用的情况，并尝试在父进程中取消wait()函数，观察进程的运行情况。', indent=False)
add_body('答：fork()用于创建子进程，wait()用于父进程阻塞等待子进程结束并获取其退出状态。两者配合使用可以确保父进程在子进程结束后再继续执行，防止出现僵尸进程。如果取消wait()函数：父进程不会等待子进程结束就直接退出，此时子进程成为孤儿进程被init进程收养；同时子进程结束后会成为僵尸进程，其PCB资源无法被及时回收。')

add_image_placeholder('插入取消wait()后的运行结果对比截图（可在fork_demo.c中注释掉wait()行，重新编译运行，观察输出顺序变化和僵尸进程现象）')

add_body('（3）验证、总结exec函数族的具体使用方法。', indent=False)
add_body('答：exec函数族共有6个函数：execl、execlp、execle、execv、execvp、execve。其中只有execve是真正的系统调用，其他都是库函数。它们的区别在于参数传递方式：l表示参数以列表（list）形式传递，v表示参数以数组（vector）形式传递；带p的函数会自动搜索PATH环境变量查找可执行文件；带e的函数可以指定新的环境变量数组。exec函数执行成功后不会返回，因为当前进程的映像已被替换；执行失败时返回-1。')

doc.add_page_break()

# ==================== 实验3.2 ====================
add_title('实验3.2：进程调度算法的模拟', level=1)

add_title('一、实验目的', level=2)
add_body('（1）加深对进程概念的理解，明确进程和程序的区别。')
add_body('（2）深入理解系统如何组织进程。')
add_body('（3）理解常用进程调度算法的具体实现。')

add_title('二、实验内容', level=2)
add_body('编写C程序，模拟实现单处理器系统中的进程调度算法，实现对多个进程的模拟调度，要求采用常见的进程调度算法（先来先服务FCFS、时间片轮转RR、动态优先级调度）进行模拟调度。')

add_title('三、实验设计', level=2)
add_body('1. 进程控制块（PCB）设计：包含进程名、PID、到达时间、服务时间、已运行时间、优先数、状态等字段。')
add_body('2. 就绪队列：采用链表结构实现，便于插入和删除操作。')
add_body('3. 三种调度算法：')
add_body('  （1）先来先服务（FCFS）：按照进程到达的先后顺序进行调度。')
add_body('  （2）时间片轮转（RR）：每个进程运行一个时间片后切换到下一个进程。')
add_body('  （3）动态优先级调度：优先数大者优先，每运行一个时间单位优先数减1。')

add_title('四、实验代码', level=2)

code_sched = """#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TIME_SLICE 2    /* 时间片大小（RR算法用） */

/* 进程控制块 PCB */
typedef struct pcb {
    char name[10];
    int pid;
    int arrive_time;     /* 到达时间 */
    int service_time;   /* 需要运行的总时间 */
    int used_time;       /* 已运行时间 */
    int priority;        /* 优先数 */
    char state;          /* W=就绪, R=运行, F=完成 */
    struct pcb* next;
} PCB;

PCB* ready_queue = NULL;
int current_time = 0;
int process_count = 0;

/* 创建进程 */
PCB* create_pcb(const char* name, int arrive, int service, int prio) {
    PCB* p = (PCB*)malloc(sizeof(PCB));
    strcpy(p->name, name);
    p->pid = ++process_count;
    p->arrive_time = arrive;
    p->service_time = service;
    p->used_time = 0;
    p->priority = prio;
    p->state = 'W';
    p->next = NULL;
    return p;
}

/* 按优先数降序插入就绪队列 */
void enqueue_priority(PCB* p) {
    p->next = NULL;
    if (!ready_queue || p->priority > ready_queue->priority) {
        p->next = ready_queue;
        ready_queue = p;
        return;
    }
    PCB* q = ready_queue;
    while (q->next && q->next->priority >= p->priority)
        q = q->next;
    p->next = q->next;
    q->next = p;
}

/* 从队首取进程 */
PCB* dequeue() {
    if (!ready_queue) return NULL;
    PCB* p = ready_queue;
    ready_queue = ready_queue->next;
    p->next = NULL;
    return p;
}

/* 显示就绪队列 */
void show_queue() {
    PCB* p = ready_queue;
    printf("就绪队列: ");
    while (p) {
        printf("%s(优先数:%d) ", p->name, p->priority);
        p = p->next;
    }
    printf("\\n");
}

/* ========== FCFS 先来先服务 ========== */
void fcfs() {
    printf("\\n===== 先来先服务 FCFS =====\\n");
    current_time = 0;
    PCB* p;
    while ((p = dequeue())) {
        printf("时刻 %d: 调度 %s 运行 (需 %d)\\n",
               current_time, p->name, p->service_time);
        current_time += p->service_time;
        printf("时刻 %d: %s 结束, 周转时间=%d\\n\\n",
               current_time, p->name, current_time - p->arrive_time);
        free(p);
    }
}

/* ========== RR 时间片轮转 ========== */
void rr() {
    printf("\\n===== 时间片轮转 RR (时间片=%d) =====\\n", TIME_SLICE);
    current_time = 0;
    int finished = 0;
    PCB* p;
    while (finished < process_count) {
        p = dequeue();
        if (!p) { current_time++; continue; }
        printf("时刻 %d: 调度 %s 运行一个时间片\\n", current_time, p->name);
        int run = TIME_SLICE;
        if (p->service_time - p->used_time < TIME_SLICE)
            run = p->service_time - p->used_time;
        current_time += run;
        p->used_time += run;
        if (p->used_time >= p->service_time) {
            printf("时刻 %d: %s 完成! 周转时间=%d\\n\\n",
                   current_time, p->name, current_time - p->arrive_time);
            free(p);
            finished++;
        } else {
            p->next = NULL;
            if (!ready_queue) ready_queue = p;
            else {
                PCB* q = ready_queue;
                while (q->next) q = q->next;
                q->next = p;
            }
            printf("时刻 %d: %s 时间片到, 剩余 %d\\n",
                   current_time, p->name, p->service_time - p->used_time);
            show_queue();
        }
    }
}

/* ========== 动态优先级调度 ========== */
void priority_sched() {
    printf("\\n===== 动态优先级调度 =====\\n");
    current_time = 0;
    int finished = 0;
    PCB* p;
    while (finished < process_count) {
        p = dequeue();
        if (!p) { current_time++; continue; }
        printf("时刻 %d: 调度 %s 运行 (优先数=%d)\\n",
               current_time, p->name, p->priority);
        current_time++;
        p->used_time++;
        if (p->used_time >= p->service_time) {
            printf("时刻 %d: %s 完成! 周转时间=%d\\n\\n",
                   current_time, p->name, current_time - p->arrive_time);
            free(p);
            finished++;
        } else {
            p->priority--;
            enqueue_priority(p);
            printf("时刻 %d: %s 优先数降为 %d, 重新排队\\n",
                   current_time, p->name, p->priority);
            show_queue();
        }
    }
}

/* 初始化测试进程 */
void init() {
    printf("\\n测试进程: P1(4,3) P2(3,5) P3(5,4) P4(2,2)\\n");
    enqueue_priority(create_pcb("P1", 0, 4, 3));
    enqueue_priority(create_pcb("P2", 0, 3, 5));
    enqueue_priority(create_pcb("P3", 0, 5, 4));
    enqueue_priority(create_pcb("P4", 0, 2, 2));
    show_queue();
}

int main() {
    int choice;
    printf("===== 进程调度模拟 =====\\n");
    printf("1. FCFS 先来先服务\\n");
    printf("2. RR 时间片轮转\\n");
    printf("3. 动态优先级调度\\n");
    printf("请选择(1-3): ");
    scanf("%d", &choice);
    init();
    switch (choice) {
        case 1: fcfs(); break;
        case 2: rr(); break;
        case 3: priority_sched(); break;
        default: printf("输入错误!\\n");
    }
    return 0;
}"""
add_code_block(code_sched)

add_title('五、实验结果', level=2)

add_body('编译命令：gcc scheduler.c -o scheduler', indent=False)
add_body('运行命令：./scheduler', indent=False)

doc.add_paragraph()
add_body('1. 先来先服务（FCFS）调度结果：', indent=False)
add_image_placeholder('插入 FCFS 调度运行截图（运行程序后输入1，显示四个进程按顺序调度的完整输出，包含周转时间）')

doc.add_paragraph()
add_body('2. 时间片轮转（RR）调度结果：', indent=False)
add_image_placeholder('插入 RR 时间片轮转调度运行截图（运行程序后输入2，显示进程来回切换、时间片用完重新排队的过程）')

doc.add_paragraph()
add_body('3. 动态优先级调度结果：', indent=False)
add_image_placeholder('插入动态优先级调度运行截图（运行程序后输入3，显示优先数动态变化、进程重新排队的完整过程）')

add_body('结果分析：', indent=False)
add_body('FCFS算法实现简单，但平均周转时间较长，短作业等待时间长。RR算法通过时间片轮转保证了公平性，响应时间较好，但时间片大小需要权衡。动态优先级调度既能照顾高优先级进程，又通过动态降低优先级避免了低优先级进程饥饿问题。')

add_title('六、实验思考', level=2)

add_body('（1）上述示例调度程序中的调度模式是抢占式还是非抢占式？', indent=False)
add_body('答：示例中的调度模式是非抢占式的。因为一个进程一旦获得CPU运行，就会一直运行直到时间片用完或进程结束，期间不会因为有更高优先级的进程进入就绪队列而被抢占。只有当前进程的时间片用完后，才会重新进行调度选择。')

add_body('（2）若要将上述示例调度程序中的进程运行方式改为每运行一次就将优先数减2，同时将运行时间加1，其他条件不变，则该如何修改？', indent=False)
add_body('答：需要修改running()函数中的两处：①将(p->nice)--改为(p->nice) -= 2，即每运行一次优先数减2；②保持运行时间加1的逻辑不变。如果是指每次运行两个时间单位，则修改运行逻辑，使每个进程每次调度运行2个时间单位后再重新调度。')

add_body('（3）如何将上述调度算法改为固定优先数调度算法？', indent=False)
add_body('答：删除running()函数中对优先数减1的操作（即删除(p->nice)--这一行），保持进程的优先数在整个生命周期中不变。这样每次调度时都按照初始设定的优先数进行排序，优先数高的进程总是优先获得CPU，直到运行结束。这种方式的缺点是低优先级进程可能长期得不到调度，产生饥饿现象。')

add_body('（4）如何基于上述调度算法来实现先来先服务和时间片轮转调度算法？', indent=False)
add_body('答：①先来先服务（FCFS）：将sort()函数改为按进程到达时间排序，而不是按优先数排序。同时修改running()函数，使进程一旦获得CPU就一次性运行完毕（即ntime全部执行完），中间不进行调度。②时间片轮转（RR）：使用循环队列（FIFO）管理就绪进程，每次调度队首进程运行一个固定的时间片（如2个时间单位），时间片用完后，如果进程还未完成，则将其放到就绪队列末尾，再调度下一个进程。')

# ========== 保存 ==========
output_path = r'C:\Users\86138\Desktop\caozuoxitong\第三章实验报告.docx'
doc.save(output_path)
print(f'Word文档已生成：{output_path}')
