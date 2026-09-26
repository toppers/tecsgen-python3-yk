#ifndef SARITHMETICOPERATION64_CPPIF_HPP
#define SARITHMETICOPERATION64_CPPIF_HPP
/*
 * C++ interface code
 *   This class comes from signature 'sArithmeticOperation64'.
 *   All functions are pure virtual. These are defined in celltype class.
 */
 
 /* */
 class sArithmeticOperation64 {
    public:
    virtual int64_t add( int64_t x, int64_t y ) = 0;
    virtual int64_t sub( int64_t x, int64_t y ) = 0;
    virtual int64_t mul( int64_t x, int64_t y ) = 0;
    virtual int64_t div( int64_t x, int64_t y ) = 0;
    virtual int64_t rem( int64_t x, int64_t y ) = 0;
};

#endif /* SARITHMETICOPERATION64_CPPIF_HPP */
