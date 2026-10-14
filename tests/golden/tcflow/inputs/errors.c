/* syntax errors and recovery */
int ok_before(void)
{
    return 1;
}
int broken(void)
{
    int x = ;
    return x
}
int ok_after(void)
{
    ok_before();
    return 2;
}
void bad_param(int a, , int b) { }
int ok_last(void) { return ok_after(); }
