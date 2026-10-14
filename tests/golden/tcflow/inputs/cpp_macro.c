#define VALUE 3
#define ADD(a, b) ((a) + (b))
#ifdef __GNUC__
int gnuc_only(void) { return ADD(VALUE, 1); }
#endif
int g_attr __attribute__((unused));
int with_attr(void) __attribute__((noinline));
int with_attr(void)
{
    return gnuc_only();
}
