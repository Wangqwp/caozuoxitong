#include <stdio.h>
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
            printf("CHILD: I am the child process!\n");
            printf("CHILD: My PID: %d\n", getpid());
            printf("CHILD: My parent's PID: %d\n", getppid());
            printf("CHILD: fork returned: %d\n", childpid);
            printf("CHILD: Sleep for 1 second...\n");
            sleep(1);
            printf("CHILD: Enter exit value (0~255): ");
            scanf(" %d", &retval);
            printf("CHILD: Goodbye!\n");
            exit(retval);
        }
        else                  /* 返回>0 = 父进程 */
        {
            printf("PARENT: I am the parent process!\n");
            printf("PARENT: My PID: %d\n", getpid());
            printf("PARENT: My child's PID: %d\n", childpid);
            printf("PARENT: Waiting for child...\n");
            wait(&status);
            printf("PARENT: Child exit code: %d\n", WEXITSTATUS(status));
            printf("PARENT: Goodbye!\n");
            exit(0);
        }
    }
    else                       /* 返回-1 = 创建失败 */
    {
        perror("fork error!");
        exit(1);
    }
    return 0;
}
