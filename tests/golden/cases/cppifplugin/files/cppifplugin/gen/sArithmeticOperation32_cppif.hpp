#ifndef SARITHMETICOPERATION32_CPPIF_HPP
#define SARITHMETICOPERATION32_CPPIF_HPP
/*
 * C++ interface code
 *   This class comes from signature 'sArithmeticOperation32'.
 *   All functions are pure virtual. These are defined in celltype class.
 */
 
 /* */
 class sArithmeticOperation32 {
    public:
    virtual int32_t add( int32_t x, int32_t y ) = 0;
    virtual int32_t sub( int32_t x, int32_t y ) = 0;
    virtual int32_t mul( int32_t x, int32_t y ) = 0;
    virtual int32_t div( int32_t x, int32_t y ) = 0;
    virtual int32_t rem( int32_t x, int32_t y ) = 0;
};

#endif /* SARITHMETICOPERATION32_CPPIF_HPP */
