/*
thot package for statistical machine translation
Copyright (C) 2017 Adam Harasimowicz, Daniel Ortiz-Mart\'inez

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
 * @file StlPhraseTable.cc
 *
 * @brief Definitions file for StlPhraseTable.h
 */

//--------------- Include files --------------------------------------

#include "phrase_models/StlPhraseTable.h"

//--------------- Function definitions

//-------------------------
StlPhraseTable::StlPhraseTable(void)
{
}

//-------------------------
StlPhraseTable::SrcTrgKey StlPhraseTable::getSrcTrgKey(const std::vector<WordIndex>& s, const std::vector<WordIndex>& t,
                                                       bool& found)
{
  SrcPhraseInfo::iterator srcIter = srcPhraseInfo.find(s);
  TrgPhraseInfo::iterator trgIter = trgPhraseInfo.find(t);

  // Add missing information to obtain iterator for t phrase
  if (trgIter == trgPhraseInfo.end())
  {
    addTrgInfo(t, 0);
    trgIter = trgPhraseInfo.find(t);
  }

  // Check if s exists in collections
  found = !(srcIter == srcPhraseInfo.end());

  return SrcTrgKey(srcIter, trgIter);
}

//-------------------------
bool StlPhraseTable::getNbestForSrc(const std::vector<WordIndex>& s, NbestTableNode<PhraseTransTableNodeData>& nbt)
{
  StlPhraseTable::TrgTableNode::iterator iter;

  bool found;
  Count s_count;
  StlPhraseTable::TrgTableNode node;
  LgProb lgProb;

  // Make sure that collection does not contain any old elements
  nbt.clear();

  found = getEntriesForSource(s, node);
  s_count = cSrc(s);

  if (found)
  {
    // Generate transTableNode
    for (iter = node.end(); iter != node.begin();)
    {
      iter--;
      std::vector<WordIndex> t = iter->first;
      PhrasePairInfo ppi = (PhrasePairInfo)iter->second;
      float c_st = (float)ppi.second.get_c_st();
      lgProb = log(c_st / (float)s_count);
      nbt.insert(lgProb, t); // Insert pair <log probability, target phrase>
    }

#ifdef DO_STABLE_SORT_ON_NBEST_TABLE
    // Performs stable sort on n-best table, this is done to ensure
    // that the n-best lists generated by cache models and
    // conventional models are identical. However this process is
    // time consuming and must be avoided if possible
    nbt.stableSort();
#endif
    return true;
  }
  else
  {
    // Cannot find the source phrase
    return false;
  }
}
//-------------------------
bool StlPhraseTable::getNbestForTrg(const std::vector<WordIndex>& t, NbestTableNode<PhraseTransTableNodeData>& nbt,
                                    int N)
{
  StlPhraseTable::SrcTableNode::iterator iter;

  bool found;
  Count t_count;
  StlPhraseTable::SrcTableNode node;
  LgProb lgProb;

  // Make sure that collection does not contain any old elements
  nbt.clear();

  found = getEntriesForTarget(t, node);
  t_count = cTrg(t);

  if (found)
  {
    // Generate transTableNode
    for (iter = node.begin(); iter != node.end(); iter++)
    {
      std::vector<WordIndex> s = iter->first;
      PhrasePairInfo ppi = (PhrasePairInfo)iter->second;
      float c_st = (float)ppi.second.get_c_st();
      lgProb = log(c_st / (float)t_count);
      nbt.insert(lgProb, s); // Insert pair <log probability, source phrase>
    }

#ifdef DO_STABLE_SORT_ON_NBEST_TABLE
    // Performs stable sort on n-best table, this is done to ensure
    // that the n-best lists generated by cache models and
    // conventional models are identical. However this process is
    // time consuming and must be avoided if possible
    nbt.stableSort();
#endif

    while (nbt.size() > (unsigned int)N && N >= 0)
    {
      // node contains N inverse translations, remove last element
      nbt.removeLastElement();
    }

    return true;
  }
  else
  {
    // Cannot find the target phrase
    return false;
  }
}

//-------------------------
void StlPhraseTable::addTableEntry(const std::vector<WordIndex>& s, const std::vector<WordIndex>& t, PhrasePairInfo inf)
{
  Count t_count = cTrg(t);

  addSrcInfo(s, inf.first.get_c_s()); // src
  // Values for target are not summed with the old one thus they have to aggregated here
  addTrgInfo(t, (t_count + inf.second).get_c_s()); // trg
  addSrcTrgInfo(s, t, inf.second.get_c_st());      // (src, trg)
}

//-------------------------
void StlPhraseTable::addSrcInfo(const std::vector<WordIndex>& s, Count s_inf)
{
  SrcPhraseInfo::iterator iter = srcPhraseInfo.find(s);

  if (iter == srcPhraseInfo.end()) // Check if s exists in collection
  {
    srcPhraseInfo.insert(std::make_pair(s, s_inf));
  }
  else
  {
    iter->second = s_inf;
  }
}

//-------------------------
void StlPhraseTable::addTrgInfo(const std::vector<WordIndex>& t, Count t_inf)
{
  TrgPhraseInfo::iterator iter = trgPhraseInfo.find(t);

  if (iter == trgPhraseInfo.end()) // Check if t exists in collection
  {
    trgPhraseInfo.insert(std::make_pair(t, t_inf));
  }
  else
  {
    iter->second = t_inf;
  }
}

//-------------------------
void StlPhraseTable::addSrcTrgInfo(const std::vector<WordIndex>& s, const std::vector<WordIndex>& t, Count st_inf)
{
  bool found;
  SrcTrgKey srcTrgKey = getSrcTrgKey(s, t, found);

  if (!found)
  {
    std::cerr << "Unexpected behaviour: some (s, t) key parts cannot be found" << std::endl;

    // Add empty source if missing
    getSrcInfo(s, found);
    if (!found)
    {
      std::cerr << "Cannot find s part" << std::endl;
      addSrcInfo(s, Count(0));
    }

    // Add empty target if missing
    getTrgInfo(t, found);
    if (!found)
    {
      std::cerr << "Cannot find t part" << std::endl;
      addTrgInfo(t, Count(0));
    }

    std::cerr << "Make sure that entries for s phrase and t phrase are added before adding (s, t) entry" << std::endl;
    std::cerr << "Missing parts have been added with count 0" << std::endl;
  }

  // Update entry value
  SrcTrgPhraseInfo::iterator iter = srcTrgPhraseInfo.find(srcTrgKey);

  if (iter == srcTrgPhraseInfo.end()) // Check if (s, t) exists in collection
  {
    srcTrgPhraseInfo.insert(std::make_pair(srcTrgKey, st_inf));
  }
  else
  {
    iter->second = st_inf;
  }
}

//-------------------------
void StlPhraseTable::incrCountsOfEntry(const std::vector<WordIndex>& s, const std::vector<WordIndex>& t, Count c)
{
  // Retrieve previous states
  Count s_count = cSrc(s);
  Count t_count = cTrg(t);
  Count src_trg_count = cSrcTrg(s, t);

  // Update counts
  addSrcInfo(s, s_count + c);                          // src
  addTrgInfo(t, t_count + c);                          // trg
  addSrcTrgInfo(s, t, (src_trg_count + c).get_c_st()); // (src, trg)
}

//-------------------------
PhrasePairInfo StlPhraseTable::infSrcTrg(const std::vector<WordIndex>& s, const std::vector<WordIndex>& t, bool& found)
{
  PhrasePairInfo ppi;

  ppi.first = getSrcInfo(s, found);
  if (!found)
  {
    ppi.second = 0;
    return ppi;
  }
  else
  {
    ppi.second = getSrcTrgInfo(s, t, found);
    return ppi;
  }
}

//-------------------------
Count StlPhraseTable::getSrcInfo(const std::vector<WordIndex>& s, bool& found)
{
  SrcPhraseInfo::iterator iter = srcPhraseInfo.find(s);

  if (iter == srcPhraseInfo.end()) // Check if s exists in collection
  {
    found = false;
    return 0;
  }
  else
  {
    found = true;
    return iter->second;
  }
}

//-------------------------
Count StlPhraseTable::getTrgInfo(const std::vector<WordIndex>& t, bool& found)
{
  TrgPhraseInfo::iterator iter = trgPhraseInfo.find(t);

  if (iter == trgPhraseInfo.end()) // Check if t exists in collection
  {
    found = false;
    return 0;
  }
  else
  {
    found = true;
    return iter->second;
  }
}

//-------------------------
Count StlPhraseTable::getSrcTrgInfo(const std::vector<WordIndex>& s, const std::vector<WordIndex>& t, bool& found)
{
  SrcTrgKey srcTrgKey = getSrcTrgKey(s, t, found);
  if (!found)
    return 0;

  SrcTrgPhraseInfo::iterator srcTrgIter = srcTrgPhraseInfo.find(srcTrgKey);

  // Check if entry for (s, t) pair exists
  if (srcTrgIter == srcTrgPhraseInfo.end())
  {
    found = false;
    return 0;
  }
  else
  {
    found = true;
    return srcTrgIter->second;
  }
}

//-------------------------
Prob StlPhraseTable::pTrgGivenSrc(const std::vector<WordIndex>& s, const std::vector<WordIndex>& t)
{
  // p(s|t) = count(s,t) / count(t)
  Count st_count = cSrcTrg(s, t);
  if ((float)st_count > 0)
  {
    Count s_count = cSrc(s);
    if ((float)s_count > 0)
      return ((float)st_count) / ((float)s_count);
    else
      return PHRASE_PROB_SMOOTH;
  }
  else
    return PHRASE_PROB_SMOOTH;
}

//-------------------------
LgProb StlPhraseTable::logpTrgGivenSrc(const std::vector<WordIndex>& s, const std::vector<WordIndex>& t)
{
  return log((double)pTrgGivenSrc(s, t));
}

//-------------------------
Prob StlPhraseTable::pSrcGivenTrg(const std::vector<WordIndex>& s, const std::vector<WordIndex>& t)
{
  Count count_s_t_ = cSrcTrg(s, t);
  if ((float)count_s_t_ > 0)
  {
    Count count_t_ = cTrg(t);
    if ((float)count_t_ > 0)
    {
      return (float)count_s_t_ / (float)count_t_;
    }
    else
      return PHRASE_PROB_SMOOTH;
  }
  else
    return PHRASE_PROB_SMOOTH;
}

//-------------------------
LgProb StlPhraseTable::logpSrcGivenTrg(const std::vector<WordIndex>& s, const std::vector<WordIndex>& t)
{
  return log((double)pSrcGivenTrg(s, t));
}

//-------------------------
bool StlPhraseTable::getEntriesForTarget(const std::vector<WordIndex>& t, StlPhraseTable::SrcTableNode& srctn)
{
  bool found;
  srctn.clear(); // Make sure that structure does not keep old values

  // Prepare iterators
  SrcTrgKey srcTrgBegin = getSrcTrgKey(srcPhraseInfo.begin()->first, t, found);
  if (!found)
    return false;

  SrcTrgKey srcTrgEnd = getSrcTrgKey(srcPhraseInfo.rbegin()->first, t, found); // Maybe use rbegin
  if (!found)
    return false;

  // Define border elements for searched source phrases
  SrcTrgPhraseInfo::iterator srcTrgIterBegin = srcTrgPhraseInfo.lower_bound(srcTrgBegin);
  SrcTrgPhraseInfo::iterator srcTrgIterEnd = srcTrgPhraseInfo.upper_bound(srcTrgEnd);

  for (SrcTrgPhraseInfo::iterator srcTrgIter = srcTrgIterBegin; srcTrgIter != srcTrgIterEnd; srcTrgIter++)
  {
    SrcPhraseInfo::iterator srcIter = srcTrgIter->first.first; // First element of the pair of iterators (s, t)
    std::vector<WordIndex> s = srcIter->first;
    PhrasePairInfo ppi;
    ppi.first = srcIter->second;     // s count
    ppi.second = srcTrgIter->second; // (s, t) count

    if (fabs(ppi.first.get_c_s()) < EPSILON || fabs(ppi.second.get_c_s()) < EPSILON)
      continue;

    srctn.insert(std::pair<std::vector<WordIndex>, PhrasePairInfo>(s, ppi));
  }

  return srctn.size();
}

//-------------------------
bool StlPhraseTable::getEntriesForSource(const std::vector<WordIndex>& s, StlPhraseTable::TrgTableNode& trgtn)
{
  trgtn.clear(); // Make sure that structure does not keep old values

  // Scan (s, t) collection to find matching elements for a given s

  for (SrcTrgPhraseInfo::iterator srcTrgIter = srcTrgPhraseInfo.begin(); srcTrgIter != srcTrgPhraseInfo.end();
       srcTrgIter++)
  {
    SrcPhraseInfo::iterator srcIter = srcTrgIter->first.first; // First element of the pair of iterators (s, t)
    std::vector<WordIndex> sPhrase = srcIter->first;

    if (sPhrase == s)
    {
      std::vector<WordIndex> tPhrase = srcTrgIter->first.second->first;
      Count tCount = srcTrgIter->first.second->second;

      PhrasePairInfo ppi;
      ppi.first = tCount;              // t count
      ppi.second = srcTrgIter->second; // (s, t) count

      if (fabs(ppi.first.get_c_s()) < EPSILON || fabs(ppi.second.get_c_s()) < EPSILON)
        continue;

      trgtn.insert(std::pair<std::vector<WordIndex>, PhrasePairInfo>(tPhrase, ppi));
    }
  }

  return trgtn.size();
}

//-------------------------
Count StlPhraseTable::cSrcTrg(const std::vector<WordIndex>& s, const std::vector<WordIndex>& t)
{
  bool found;
  return getSrcTrgInfo(s, t, found).get_c_st();
}

//-------------------------
Count StlPhraseTable::cSrc(const std::vector<WordIndex>& s)
{
  bool found;
  return getSrcInfo(s, found).get_c_s();
}

//-------------------------
Count StlPhraseTable::cTrg(const std::vector<WordIndex>& t)
{
  bool found;
  return getTrgInfo(t, found).get_c_st();
}

//-------------------------
void StlPhraseTable::print(void)
{
  for (StlPhraseTable::const_iterator iter = begin(); iter != end(); iter++)
  {
    // Extract information about phrase
    PhraseInfoElement elem = *iter;
    std::vector<WordIndex> s = elem.first.first;
    std::vector<WordIndex> t = elem.first.second;
    Count c = elem.second;
    // Print on standard output
    printVector(s);
    std::cout << " ||| ";
    printVector(t);
    std::cout << " ||| ";
    std::cout << c.get_c_s() << std::endl;
  }
}

//-------------------------
void StlPhraseTable::printVector(const std::vector<WordIndex>& vec) const
{
  for (size_t i = 0; i < vec.size(); i++)
  {
    std::cout << vec[i] << " ";
  }
}

//-------------------------
size_t StlPhraseTable::size(void)
{
  size_t srcSize = srcPhraseInfo.size();
  size_t trgSize = trgPhraseInfo.size();
  size_t srcTrgSize = srcTrgPhraseInfo.size();

  return srcSize + trgSize + srcTrgSize;
}
//-------------------------
void StlPhraseTable::clear(void)
{
  srcPhraseInfo.clear();
  trgPhraseInfo.clear();
  srcTrgPhraseInfo.clear();
}

//-------------------------
StlPhraseTable::~StlPhraseTable(void)
{
}

//-------------------------
StlPhraseTable::TrgPhraseInfo::const_iterator StlPhraseTable::beginTrg(void) const
{
  return trgPhraseInfo.begin();
}
//-------------------------
StlPhraseTable::TrgPhraseInfo::const_iterator StlPhraseTable::endTrg(void) const
{
  return trgPhraseInfo.end();
}

//-------------------------
StlPhraseTable::const_iterator StlPhraseTable::begin(void) const
{
  StlPhraseTable::const_iterator iter(this, srcPhraseInfo.begin(), trgPhraseInfo.begin(), srcTrgPhraseInfo.begin());

  return iter;
}
//-------------------------
StlPhraseTable::const_iterator StlPhraseTable::end(void) const
{
  StlPhraseTable::const_iterator iter(this, srcPhraseInfo.end(), trgPhraseInfo.end(), srcTrgPhraseInfo.end());

  return iter;
}

// const_iterator function definitions
//--------------------------
bool StlPhraseTable::const_iterator::operator++(void) // prefix
{
  if (ptPtr != NULL)
  {
    if (srcIter != ptPtr->srcPhraseInfo.end())
    {
      srcIter++;
      // Check if there are elements in other collections when reached end
      return !( // Not
          srcIter == ptPtr->srcPhraseInfo.end() && ptPtr->trgPhraseInfo.empty() && ptPtr->srcTrgPhraseInfo.empty());
    }
    else if (trgIter != ptPtr->trgPhraseInfo.end())
    {
      trgIter++;
      // Check if there are elements in other collections when reached end
      return !(trgIter == ptPtr->trgPhraseInfo.end() && ptPtr->srcTrgPhraseInfo.empty());
    }
    else if (srcTrgIter != ptPtr->srcTrgPhraseInfo.end())
    {
      srcTrgIter++;
      // Check if reached end of the last collection
      return srcTrgIter != ptPtr->srcTrgPhraseInfo.end();
    }
    else
    {
      return false;
    }
  }
  else
  {
    return false;
  }
}
//--------------------------
bool StlPhraseTable::const_iterator::operator++(int) // postfix
{
  return operator++();
}
//--------------------------
int StlPhraseTable::const_iterator::operator==(const const_iterator& right)
{
  return (ptPtr == right.ptPtr && srcIter == right.srcIter && trgIter == right.trgIter
          && srcTrgIter == right.srcTrgIter);
}
//--------------------------
int StlPhraseTable::const_iterator::operator!=(const const_iterator& right)
{
  return !((*this) == right);
}

//--------------------------
StlPhraseTable::PhraseInfoElement StlPhraseTable::const_iterator::operator*(void)
{
  return *operator->();
}

//--------------------------
const StlPhraseTable::PhraseInfoElement* StlPhraseTable::const_iterator::operator->(void)
{
  std::vector<WordIndex> s;
  std::vector<WordIndex> t;
  int c = 0;

  if (ptPtr != NULL)
  {
    if (srcIter != ptPtr->srcPhraseInfo.end())
    {
      s = srcIter->first;
      c = srcIter->second.get_c_s();
    }
    else if (trgIter != ptPtr->trgPhraseInfo.end())
    {
      t = trgIter->first;
      c = trgIter->second.get_c_s();
    }
    else if (srcTrgIter != ptPtr->srcTrgPhraseInfo.end())
    {
      SrcPhraseInfo::iterator _srcIter = srcTrgIter->first.first; // First element of the pair of iterators (s, t)
      s = _srcIter->first;

      TrgPhraseInfo::iterator _trgIter = srcTrgIter->first.second; // Second element of the pair of iterators (s, t)
      t = _trgIter->first;

      c = srcTrgIter->second.get_c_st();
    }
  }

  dataItem.first = std::make_pair(s, t);
  dataItem.second = c;

  return &dataItem;
}

//-------------------------
