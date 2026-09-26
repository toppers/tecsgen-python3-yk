#include  <stdlib.h>
#include  <memory.h>
#include  <stdio.h>
#include  "tSWIGsTestBridge_tecsgen.h"
#include  "CsTest.hxx"

char    CELL_RubyTest[] = "RubyTest";
struct tagName2ID { char *name; ID id; } Name2ID[] = {
    { CELL_RubyTest, 1 },
    { (char*)0, 0 }
};

CsTest *
CsTest::join( const char *CellName )
{
	CsTest *cell = new CsTest( CellName );
	return cell;
}

CsTest::CsTest( const char *CellName )
{
    m_CellName = (char *)malloc( strlen( CellName ) + 1 );
    if( m_CellName )
       strcpy( m_CellName, CellName );
    else
       m_CellName = 0;

    int   i;
    for( i = 0; Name2ID[i].name; i++ )
        if( strcmp( CellName, Name2ID[i].name ) == 0 )
             break;

    if( Name2ID[i].name )
         m_id = Name2ID[i].id;
    else
         m_id = 0;
}
	
CsTest::~CsTest()
{
    if( m_CellName )
        free( m_CellName );
    m_CellName = 0;
    m_id = 0;
}

void
CsTest::test( int input )
{
    if( ! VALID_IDX( m_id ) )
         return ;
    CELLCB *p_cellcb = (CELLCB*)GET_CELLCB( m_id );
	cTECS_test( input );
}

int32_t
CsTest::test4( const char* input,  int32_t len )
{
	int32_t	retval;
    if( ! VALID_IDX( m_id ) )
         return 0;
    CELLCB *p_cellcb = (CELLCB*)GET_CELLCB( m_id );
	retval = cTECS_test4( input, len );
	return	retval;
}

