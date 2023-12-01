/*
thot package for statistical machine translation
Copyright (C) 2013 Daniel Ortiz-Mart\'inez

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; If not, see <http://www.gnu.org/licenses/>.
*/

/**
 * @file PhrScoreInfo.cc
 *
 * @brief Definitions file for PhrScoreInfo.h
 */

//--------------- Include files --------------------------------------

#include "stack_dec/PhrScoreInfo.h"

//--------------- PhrScoreInfo class functions

Score PhrScoreInfo::getScore(void) const
{
  return score;
}

//---------------------------------
void PhrScoreInfo::addHeuristic(Score h)
{
  score = score + h;
}

//---------------------------------
void PhrScoreInfo::subtractHeuristic(Score h)
{
  score = score - h;
}
