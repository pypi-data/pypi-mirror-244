/*
 * Copyright 2009-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at:
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

/**@file */

#ifndef IONC_ION_FLOAT_H
#define IONC_ION_FLOAT_H

#include "ion_types.h"

#ifdef __cplusplus
extern "C" {
#endif

ION_API_EXPORT BOOL ion_float_is_negative_zero(double value);

#ifdef __cplusplus
}
#endif

#endif //IONC_ION_FLOAT_H
