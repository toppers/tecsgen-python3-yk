/* typedef names used as variable and member names */
typedef int size;
typedef struct { int size; } holder;
int make(int count, size n)
{
    holder h;
    int size_local = n;
    h.size = count;
    return h.size + size_local;
}
size g_size;
int by_param(size)
int size;
{
    return size;
}
