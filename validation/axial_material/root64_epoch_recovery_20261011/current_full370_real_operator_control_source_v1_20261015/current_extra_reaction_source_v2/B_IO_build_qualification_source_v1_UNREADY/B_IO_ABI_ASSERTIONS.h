#ifndef AXMAT_B_IO_ABI_ASSERTIONS_H
#define AXMAT_B_IO_ABI_ASSERTIONS_H
#if !defined(__APPLE__) || !(defined(__arm64__) || defined(__aarch64__)) || !defined(__LP64__)
#error "B IO build requires the declared Darwin arm64 LP64 ABI"
#endif
#if !defined(Linux) || !defined(Unix) || defined(HDF5_LIB) || defined(OPENMP) || defined(MPI)
#error "B IO build must retain the declared Ganlib preprocessor configuration"
#endif
/* ganlib.h binds int_32=int under LP64, float_32=float, double_64=double.
 * It and cle2000.h have no whole-file include guard: do not force-include
 * either API header twice into the retained translation units. */
_Static_assert(sizeof(int)==4, "Ganlib LP64 integer ABI");
_Static_assert(sizeof(float)==4, "Ganlib real32 ABI");
_Static_assert(sizeof(double)==8, "Ganlib real64 ABI");
_Static_assert(sizeof(void*)==8 && sizeof(long)==8, "Ganlib LP64 pointer ABI");
#if __BYTE_ORDER__ != __ORDER_LITTLE_ENDIAN__
#error "B IO build requires the declared native little endian byte order"
#endif
#endif
