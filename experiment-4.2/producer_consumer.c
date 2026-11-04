#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <semaphore.h>
#include <errno.h>
#define N 5
#define TOTAL 20
typedef struct { sem_t empty, full, mutex; int a[N], in, out; } Shared;
void P(sem_t *s) { while (sem_wait(s) == -1) { if (errno != EINTR) { perror("sem_wait"); _exit(1); } } }
void V(sem_t *s) { if (sem_post(s) == -1) { perror("sem_post"); _exit(1); } }
int main(void) {
    Shared *s = mmap(NULL,sizeof *s,PROT_READ|PROT_WRITE,MAP_SHARED|MAP_ANONYMOUS,-1,0);
    if (s == MAP_FAILED) { perror("mmap"); return 1; }
    s->in=s->out=0;
    if (sem_init(&s->empty,1,N)||sem_init(&s->full,1,0)||sem_init(&s->mutex,1,1)) { perror("sem_init"); return 1; }
    setbuf(stdout,NULL);
    pid_t p=fork();
    if (p<0) { perror("fork"); return 1; }
    if (p==0) {
        for(int i=1;i<=TOTAL;i++) {
            P(&s->empty); P(&s->mutex);
            s->a[s->in]=i; printf("produce %d at %d\n",i,s->in); s->in=(s->in+1)%N;
            V(&s->mutex); V(&s->full);
        }
        _exit(0);
    }
    for(int i=1;i<=TOTAL;i++) {
        P(&s->full); P(&s->mutex);
        int x=s->a[s->out]; printf("consume %d at %d\n",x,s->out); s->out=(s->out+1)%N;
        V(&s->mutex); V(&s->empty);
        if(x!=i) { fprintf(stderr,"order error\n"); return 1; }
    }
    int status; waitpid(p,&status,0);
    sem_destroy(&s->empty); sem_destroy(&s->full); sem_destroy(&s->mutex); munmap(s,sizeof *s);
    if (!WIFEXITED(status)||WEXITSTATUS(status)) return 1;
    puts("PASS: 20 items consumed in FIFO order"); return 0;
}

