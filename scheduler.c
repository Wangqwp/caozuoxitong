#include <stdio.h>
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
    int finish_time;     /* 完成时间 */
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
    printf("\n");
}

/* ========== FCFS 先来先服务 ========== */
void fcfs() {
    printf("\n===== 先来先服务 FCFS =====\n");
    current_time = 0;
    PCB* p;
    while ((p = dequeue())) {
        printf("时刻 %d: 调度 %s 运行 (需 %d 个时间单位)\n",
               current_time, p->name, p->service_time);
        current_time += p->service_time;
        p->used_time = p->service_time;
        printf("时刻 %d: %s 运行结束, 周转时间 = %d\n\n",
               current_time, p->name, current_time - p->arrive_time);
        free(p);
    }
}

/* ========== RR 时间片轮转 ========== */
void rr() {
    printf("\n===== 时间片轮转 RR (时间片=%d) =====\n", TIME_SLICE);
    current_time = 0;
    int finished = 0;
    PCB* p;
    while (finished < process_count) {
        p = dequeue();
        if (!p) { current_time++; continue; }

        printf("时刻 %d: 调度 %s 运行一个时间片\n", current_time, p->name);
        int run = TIME_SLICE;
        if (p->service_time - p->used_time < TIME_SLICE)
            run = p->service_time - p->used_time;

        current_time += run;
        p->used_time += run;

        if (p->used_time >= p->service_time) {
            printf("时刻 %d: %s 完成! 周转时间 = %d\n\n",
                   current_time, p->name, current_time - p->arrive_time);
            free(p);
            finished++;
        } else {
            /* 回到队尾 */
            p->next = NULL;
            if (!ready_queue) ready_queue = p;
            else {
                PCB* q = ready_queue;
                while (q->next) q = q->next;
                q->next = p;
            }
            printf("时刻 %d: %s 时间片到, 剩余 %d\n",
                   current_time, p->name, p->service_time - p->used_time);
            show_queue();
        }
    }
}

/* ========== 动态优先级调度 ========== */
void priority_sched() {
    printf("\n===== 动态优先级调度 =====\n");
    current_time = 0;
    int finished = 0;
    PCB* p;
    while (finished < process_count) {
        p = dequeue();
        if (!p) { current_time++; continue; }

        printf("时刻 %d: 调度 %s 运行 (优先数=%d)\n",
               current_time, p->name, p->priority);
        current_time++;
        p->used_time++;

        if (p->used_time >= p->service_time) {
            printf("时刻 %d: %s 完成! 周转时间 = %d\n\n",
                   current_time, p->name, current_time - p->arrive_time);
            free(p);
            finished++;
        } else {
            p->priority--;   /* 每运行一次优先数减1 */
            enqueue_priority(p);
            printf("时刻 %d: %s 优先数降为 %d, 重新排队\n",
                   current_time, p->name, p->priority);
            show_queue();
        }
    }
}

/* 初始化测试进程 */
void init() {
    printf("\n创建测试进程: P1(4,3) P2(3,5) P3(5,4) P4(2,2)\n");
    printf("格式: 进程名(服务时间, 初始优先数)\n");
    enqueue_priority(create_pcb("P1", 0, 4, 3));
    enqueue_priority(create_pcb("P2", 0, 3, 5));
    enqueue_priority(create_pcb("P3", 0, 5, 4));
    enqueue_priority(create_pcb("P4", 0, 2, 2));
    show_queue();
}

int main() {
    int choice;
    printf("===== 进程调度模拟 =====\n");
    printf("1. FCFS 先来先服务\n");
    printf("2. RR 时间片轮转\n");
    printf("3. 动态优先级调度\n");
    printf("请选择(1-3): ");
    scanf("%d", &choice);

    init();

    switch (choice) {
        case 1: fcfs(); break;
        case 2: rr(); break;
        case 3: priority_sched(); break;
        default: printf("输入错误!\n");
    }
    return 0;
}
