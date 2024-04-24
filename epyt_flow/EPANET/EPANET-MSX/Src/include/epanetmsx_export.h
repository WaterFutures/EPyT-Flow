
#ifndef MSXDLLEXPORT_H
#define MSXDLLEXPORT_H

#ifdef SHARED_EXPORTS_BUILT_AS_STATIC
#  define MSXDLLEXPORT
#  define EPANETMSX_NO_EXPORT
#else
#  ifndef MSXDLLEXPORT
#    ifdef epanetmsx_EXPORTS
        /* We are building this library */
#      define MSXDLLEXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define MSXDLLEXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef EPANETMSX_NO_EXPORT
#    define EPANETMSX_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef EPANETMSX_DEPRECATED
#  define EPANETMSX_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef EPANETMSX_DEPRECATED_EXPORT
#  define EPANETMSX_DEPRECATED_EXPORT MSXDLLEXPORT EPANETMSX_DEPRECATED
#endif

#ifndef EPANETMSX_DEPRECATED_NO_EXPORT
#  define EPANETMSX_DEPRECATED_NO_EXPORT EPANETMSX_NO_EXPORT EPANETMSX_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef EPANETMSX_NO_DEPRECATED
#    define EPANETMSX_NO_DEPRECATED
#  endif
#endif

#endif /* MSXDLLEXPORT_H */
