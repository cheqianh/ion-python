// Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License").
// You may not use this file except in compliance with the License.
// A copy of the License is located at:
//
//    http://aws.amazon.com/apache2.0/
//
// or in the "license" file accompanying this file. This file is
// distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
// OF ANY KIND, either express or implied. See the License for the
// specific language governing permissions and limitations under the
// License.

#ifndef _IONCMODULE_H_
#define _IONCMODULE_H_

#include "structmember.h"
#include "decimal128.h"
#include "ion.h"

PyObject* ionc_init_module(void);
iERR _ionc_write(PyObject* obj, PyObject* tuple_as_sexp, hWRITER writer);
PyObject* ionc_read(PyObject* self, PyObject *args, PyObject *kwds);
iERR ionc_read_all(hREADER hreader, PyObject* container, BOOL in_struct, BOOL emit_bare_values);

#endif
