#ifndef _IONCMODULE_H_
#define _IONCMODULE_H_

#include "structmember.h"
#include "decimal128.h"
#include "ion.h"

PyObject* ionc_init_module(void);
iERR ionc_write_value(hWRITER writer, PyObject* obj, PyObject* tuple_as_sexp);
PyObject* ionc_read(PyObject* self, PyObject *args, PyObject *kwds);
iERR ionc_read_all(hREADER hreader, PyObject* container, BOOL in_struct, BOOL emit_bare_values);
iERR ionc_read_value(hREADER hreader, ION_TYPE t, PyObject* container, BOOL in_struct, BOOL emit_bare_values);


#endif
