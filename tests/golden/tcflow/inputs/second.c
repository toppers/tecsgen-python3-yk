/* second file: calls functions defined in basic.c */
int second_func(void)
{
    fact(3);
    return helper(1, 2) + g_count;
}
