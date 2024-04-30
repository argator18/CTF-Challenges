// gcc -O0 -g main.c -o main
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define MAX_TASKS 25
#define TASK_NAME 0x90

typedef struct Task
{
    char name[TASK_NAME];
} task_t;

task_t *tasks[MAX_TASKS];

long read_long()
{
    char buf[1024];
    char *end;
    long ret;

    if (!fgets(buf, sizeof(buf), stdin))
    {
        puts("error reading stdin");
        exit(1);
    }
    ret = strtol(buf, &end, 10);
    if(end == buf){
        puts("not a number");
        exit(1);
    }
    return ret;
}

void add_task()
{
    char *last_n;

    for (int i = 0; i < MAX_TASKS; i++)
    {
        if (tasks[i])
        {
            continue;
        }
        tasks[i] = malloc(sizeof(task_t));
        printf("name? ");
        read(0, tasks[i]->name, TASK_NAME);
        last_n = strrchr(tasks[i]->name, '\n');
        if (last_n)
        {
            *last_n = 0;
        }
        return;
    }
    puts("too many tasks :(");
}

void delete_task()
{
    long id;

    printf("id? ");
    id = read_long();
    if (id >= MAX_TASKS)
    {
        puts("invalid id");
        return;
    }
    if (!tasks[id])
    {
        puts("task does not exist");
        return;
    }
    free(tasks[id]);
}

void list_tasks()
{
    for (int i = 0; i < MAX_TASKS; i++)
    {
        if (!tasks[i])
        {
            continue;
        }
        printf("[%02d] %s\n", i, tasks[i]->name);
    }
}

void execute()
{
    long address;

    printf("address? ");
    address = read_long();
    printf("jumping to %p\n", (void *)address);
    ((void (*)(char *))address)("cat /flag");
}

int menu()
{
    long choice;
    puts("---menu---");
    puts("[0] exit");
    puts("[1] add task");
    puts("[2] delete task");
    puts("[3] list tasks");
    puts("[4] execute");

    printf("choice? ");
    choice = read_long();
    return choice;
}

int main(int argc, char **argv)
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);
    while (1)
    {
        switch (menu())
        {
        case 0:
            return 0;
        case 1:
            add_task();
            break;
        case 2:
            delete_task();
            break;
        case 3:
            list_tasks();
            break;
        case 4:
            execute();
            break;
        default:
            puts("choose wisely");
        }
    }
}