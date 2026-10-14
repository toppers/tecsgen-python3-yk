/* basic: globals, calls, undefined and recursive functions */
typedef int myint;
int g_count;
int g_table[4];
static int helper(int x, myint y)
{
    g_count = g_count + x;
    return y;
}
void func_a(void)
{
    int local = 0;
    g_count++;
    helper(1, 2);
    other_undefined();
}
int fact(int n)
{
    if (n <= 1) return 1;
    return n * fact(n - 1);
}
int even(int n);
int odd(int n)
{
    return n == 0 ? 0 : even(n - 1);
}
int even(int n)
{
    return n == 0 ? 1 : odd(n - 1);
}
int main(int argc, char **argv)
{
    func_a();
    helper(argc, 3);
    g_table[argc] = fact(5);
    if (g_count > 0) { g_count = 0; }
    return 0;
}
