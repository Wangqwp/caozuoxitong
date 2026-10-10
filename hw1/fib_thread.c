/*
 * Homework 1 (第一次作业) - Problem 6
 * Generate Fibonacci sequence with a Pthread
 * Usage: ./fib_thread 5
 * The worker thread writes the first n Fibonacci numbers into a shared
 * array fib[]. The parent thread pthread_join()s the worker, then prints.
 * Compile: gcc fib_thread.c -o fib_thread -lpthread
 */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

static long n;          /* count, passed from command line */
static long *fib;       /* shared array: holds the result */

/* Thread routine: fill fib[0..n-1] */
void *runner(void *param)
{
    (void)param;
    long a = 0, b = 1;
    for (long i = 0; i < n; i++) {
        fib[i] = a;
        long next = a + b;
        a = b;
        b = next;
    }
    pthread_exit(NULL);
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <n>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    char *endptr;
    n = strtol(argv[1], &endptr, 10);
    if (*endptr != '\0' || n < 0) {
        fprintf(stderr, "Error: n must be a non-negative integer.\n");
        exit(EXIT_FAILURE);
    }

    fib = malloc(sizeof(long) * (n > 0 ? n : 1));
    if (fib == NULL) {
        perror("malloc failed");
        exit(EXIT_FAILURE);
    }

    pthread_t tid;
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_create(&tid, &attr, runner, NULL);

    /* Wait for the worker thread to finish before printing */
    pthread_join(tid, NULL);

    printf("First %ld Fibonacci numbers: ", n);
    for (long i = 0; i < n; i++) {
        printf("%ld", fib[i]);
        if (i + 1 < n) printf(" ");
    }
    printf("\n");

    free(fib);
    return 0;
}
