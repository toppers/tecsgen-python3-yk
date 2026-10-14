#include <stddef.h>
size_t g_len;
int uses_stddef(void)
{
    g_len = sizeof(int);
    return 0;
}
