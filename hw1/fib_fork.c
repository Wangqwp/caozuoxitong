/*
 * Homework 1 (第一次作业) - Problem 5
 * Generate Fibonacci sequence using fork()
 * Usage: ./fib_fork 5
 * The child process prints the first n Fibonacci numbers.
 * The parent waits for the child to finish before exiting.
 * Compile on Linux/WSL: gcc fib_fork.c -o fib_fork
 */
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <n>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    /* Error check: n must be a non-negative integer */
    char *endptr;
    long n = strtol(argv[1], &endptr, 10);
    if (*endptr != '\0' || n < 0) {
        fprintf(stderr, "Error: n must be a non-negative integer.\n");
        exit(EXIT_FAILURE);
    }

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork failed");
        exit(EXIT_FAILURE);
    }

    if (pid == 0) {
        /* ---- child: generate and print the first n Fibonacci numbers ---- */
        long a = 0, b = 1;   /* a = fib(k-2), b = fib(k-1) */
        for (long i = 0; i < n; i++) {
            printf("%ld", a);
            if (i + 1 < n) printf(" ");
            long next = a + b;
            a = b;
            b = next;
        }
        printf("\n");
        exit(EXIT_SUCCESS);
    } else {
        /* ---- parent: wait for the child to finish ---- */
        wait(NULL);
        printf("Parent: child has finished printing Fibonacci.\n");
    }

    return 0;
}
