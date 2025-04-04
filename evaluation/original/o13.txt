#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    void* elems;
    int elem_size;
    int log_len;
    int alloc_len;
}Stack;

void stack_init(Stack* s, int elem_size) {
    s->elem_size = elem_size;
    s->log_len = 0;
    s->alloc_len = 5;
    s->elems = malloc(s->alloc_len * elem_size);
    assert(s->elems != NULL);
}

void stack_dispose(Stack* s) {
    free(s->elems);
}

void stack_push(Stack* s, void* val) {
    if(s->log_len == s->alloc_len) {
        s->alloc_len *= 2;
        s->elems = realloc(s->elems, s->elem_size * s->alloc_len);
        assert(s->elems != NULL);
    }
    void* last_place = (char*)s->elems + s->log_len * s->elem_size;
    memcpy(last_place, val, s->elem_size);
    s->log_len++;
}

void stack_pop(Stack* s, void* dst_ptr) {
    assert(s->log_len > 0);
    s->log_len--;
    void* top_elem = (char*)s->elems + s->log_len * s->elem_size;
    memcpy(dst_ptr, top_elem, s->elem_size);
}

int stack_size(Stack* s) {
    return s->log_len;
}

int main() {
    Stack s;
    stack_init(&s, sizeof(int));
    for(int i = 0; i < 100; i++) {
        stack_push(&s, &i);
    }
    int res;
    for(int i = 0; i < 11; i++) {
        int size = stack_size(&s);
        stack_pop(&s, &res);
        printf("size: %d  ____  elem: %d\n", size, res);
    }
    stack_dispose(&s);

    return 0;
}