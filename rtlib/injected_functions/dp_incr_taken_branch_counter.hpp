/*
 * This file is part of the DiscoPoP software
 * (http://www.discopop.tu-darmstadt.de)
 *
 * Copyright (c) 2020, Technische Universitaet Darmstadt, Germany
 *
 * This software may be modified and distributed under the terms of
 * the 3-Clause BSD License. See the LICENSE file in the package base
 * directory for details.
 *
 */

#pragma once

#include "../DPTypes.hpp"

namespace __dp {

/******* Instrumentation function *******/
extern "C" {

void __dp_incr_taken_branch_counter(char *source_and_target, int cmp_res, int active_on);

}

} // namespace __dp
