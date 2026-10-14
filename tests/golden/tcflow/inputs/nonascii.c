/* 日本語のコメント */
char *g_msg = "日本語";
int kanji(void)
{
    g_msg = "あいう"; return 1;
}
/* sjis: ���� */
int after_sjis(void) { return kanji(); }
