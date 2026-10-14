/* features: many syntax elements */
#include <stdio.h>
#define SQUARE(x) ((x)*(x))
# 20 "virtual_header.h"
struct point { int x; int y; };
union u { int i; float f; };
enum color { RED, GREEN = 2, BLUE, };
typedef struct point point_t;
typedef int (*callback_t)(int);
struct flags { unsigned a : 1; unsigned b : 3; };
static const volatile int g_const = 0x1F;
unsigned long g_ul = 10UL;
float g_f = 1.5e3f;
double g_d = .25;
int g_oct = 0755;
char g_c = 'a';
char *g_s = "string with \"quote\" and ; semicolon";
int g_arr[3] = { 1, 2, 3 };
point_t g_pt;
callback_t g_cb;

/* multi-line
   comment with ; and { inside */
int use_struct(point_t *p, struct point q)
{
    int sum;
    sum = p->x + q.y;     // line comment with ; inside
    g_pt.x += sum;
    g_pt.y -= 1;
    p->x <<= 2;
    g_arr[1] |= 8;
    return sum;
}

int use_control(int n)
{
    int i;
    for (i = 0; i < n; i++) {
        if (i % 2) continue;
        else break;
    }
    for (int j = 0; j < 3; j++) { g_oct += j; }
    while (n > 0) { n--; }
    do { n++; } while (n < 3);
    switch (n) {
    case 1: g_oct = 1; break;
    default: g_oct = 2;
    }
    goto done;
done:
    return (int)(n * sizeof(int)) + sizeof(point_t);
}

int use_pointer_call(int v)
{
    g_cb(v);
    (*g_cb)(v);
    return ((callback_t)0)(v);
}

int kr_style(a, b)
int a;
char *b;
{
    return a;
}

untyped_func()
{
    return 0;
}

int with_asm(void)
{
    __asm__ ("nop");
    return 1;
}

int __cdecl with_cdecl(int a)
{
    return a;
}

__declspec(dllexport) int with_declspec(void)
{
    return 2;
}

int caller_of_all(void)
{
    use_struct(&g_pt, g_pt);
    use_control(3);
    use_pointer_call(1);
    kr_style(1, "x");
    untyped_func();
    return with_asm() + with_cdecl(1) + with_declspec();
}
