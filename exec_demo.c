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
        /* 子进程：执行 ls -l 命令 */
        printf("[Child] Ready to run 'ls -l', my PID = %d\n", getpid());

        execlp("ls", "ls", "-l", NULL);

        /* 只有exec失败时才会走到这里 */
        perror("execlp failed");
        exit(1);
    }
    else
    {
        /* 父进程：等待子进程结束 */
        printf("[Parent] Waiting for child, my PID = %d\n", getpid());
        wait(NULL);
        printf("[Parent] Child finished.\n");
    }

    return 0;
}
