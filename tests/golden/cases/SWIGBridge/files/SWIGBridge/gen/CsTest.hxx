class CsTest {
public:
    static CsTest *join( const char *CellName );
    void test( int input );
    int32_t test4( const char* input,  int32_t len );

private:
    CsTest( const char *CellName );
    CsTest();
    ~CsTest();

    ID    m_id;
    char  *m_CellName;
};

