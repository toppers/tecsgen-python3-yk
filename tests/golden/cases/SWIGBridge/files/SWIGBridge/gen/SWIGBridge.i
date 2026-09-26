%module SWIGBridge
%{
#include <stdint.h>
#include "global_tecsgen.h"
#include "CsTest.hxx"
%}

typedef  int int_t;
typedef  char char_t;
%import stdint.h
%import global_tecsgen.h
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

